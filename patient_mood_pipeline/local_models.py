from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .deidentify import DeidentificationResult, redact_text


class LocalModelError(RuntimeError):
    pass


def transcribe_audio(audio_path: str | Path, config: PipelineConfig) -> dict:
    pipe = _pipeline(
        "automatic-speech-recognition",
        config.asr_model_id,
        config,
        chunk_length_s=30,
        stride_length_s=5,
    )
    path = str(audio_path)
    try:
        result = pipe(
            path,
            return_timestamps=True,
            generate_kwargs={"language": config.asr_language, "task": "transcribe"},
        )
    except TypeError:
        result = pipe(path, return_timestamps=True)

    text = result.get("text", "") if isinstance(result, dict) else str(result)
    return {
        "text": text.strip(),
        "segments": result.get("chunks", []) if isinstance(result, dict) else [],
        "model_id": config.asr_model_id,
    }


def analyze_voice_emotion(audio_path: str | Path, config: PipelineConfig) -> dict:
    pipe = _pipeline("audio-classification", config.emotion_model_id, config)
    raw = pipe(str(audio_path), top_k=None)
    scores = _normalize_scores(raw)
    dominant = max(scores, key=lambda item: item["score"]) if scores else {"label": "unknown", "score": 0}
    interpreted = _interpret_emotion_label(str(dominant["label"]))
    return {
        "model_id": config.emotion_model_id,
        "dominant_label": dominant["label"],
        "dominant_score": float(dominant["score"]),
        "arousal": interpreted["arousal"],
        "valence": interpreted["valence"],
        "clinical_hint": interpreted["clinical_hint"],
        "scores": scores,
    }


def deidentify_with_local_ner(text: str, config: PipelineConfig) -> DeidentificationResult:
    entities: list[dict[str, Any]] = []
    warnings: list[str] = []
    try:
        ner = _pipeline("token-classification", config.ner_model_id, config, aggregation_strategy="simple")
        entities = _run_ner_in_chunks(text, ner, config.ner_chunk_chars)
    except Exception as exc:
        warnings.append(f"NER model unavailable; regex redaction fallback used: {exc}")

    result = redact_text(text, entities, warnings=warnings)
    return result


def _pipeline(task: str, model_id: str, config: PipelineConfig, **kwargs):
    try:
        import torch
        from transformers import pipeline
    except ImportError as exc:
        raise LocalModelError(
            "Missing local model dependencies. Install requirements.txt before running the model pipeline."
        ) from exc

    device = _resolve_device(config.hf_device)
    pipe_kwargs = {
        "task": task,
        "model": model_id,
        "device": device,
        **kwargs,
    }
    if config.hf_cache_dir:
        pipe_kwargs["cache_dir"] = config.hf_cache_dir
    if device != -1 and task == "automatic-speech-recognition":
        pipe_kwargs["torch_dtype"] = torch.float16
    return pipeline(**pipe_kwargs)


def _resolve_device(value: str) -> int:
    setting = (value or "auto").lower()
    if setting == "cpu":
        return -1
    if setting == "auto":
        try:
            import torch

            return 0 if torch.cuda.is_available() else -1
        except ImportError:
            return -1
    if setting.startswith("cuda"):
        match = re.search(r":(\d+)$", setting)
        return int(match.group(1)) if match else 0
    try:
        return int(setting)
    except ValueError:
        return -1


def _run_ner_in_chunks(text: str, ner, chunk_chars: int) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for chunk, offset in _iter_chunks(text, chunk_chars):
        for entity in ner(chunk):
            if "start" in entity and "end" in entity:
                entity = dict(entity)
                entity["start"] = int(entity["start"]) + offset
                entity["end"] = int(entity["end"]) + offset
                entities.append(entity)
    return entities


def _iter_chunks(text: str, chunk_chars: int):
    max_chars = max(160, chunk_chars)
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            boundary = max(text.rfind("\n", start, end), text.rfind("。", start, end), text.rfind("，", start, end))
            if boundary > start + 80:
                end = boundary + 1
        yield text[start:end], start
        start = end


def _normalize_scores(raw) -> list[dict]:
    if isinstance(raw, dict):
        raw = [raw]
    if raw and isinstance(raw[0], list):
        raw = raw[0]
    return [
        {
            "label": str(item.get("label", "")),
            "score": float(item.get("score", 0)),
        }
        for item in (raw or [])
    ]


def _interpret_emotion_label(label: str) -> dict:
    normalized = label.lower()
    if any(term in normalized for term in ["angry", "anger", "fear", "disgust", "frustrat", "焦慮", "害怕", "生氣"]):
        return {"arousal": "高", "valence": "負向", "clinical_hint": "語音模型偵測到高喚起負向情緒。"}
    if any(term in normalized for term in ["sad", "depress", "悲", "低落", "難過"]):
        return {"arousal": "低", "valence": "負向", "clinical_hint": "語音模型偵測到低落或悲傷情緒。"}
    if any(term in normalized for term in ["happy", "joy", "surprise", "開心"]):
        return {"arousal": "中", "valence": "正向", "clinical_hint": "語音模型偵測到偏正向情緒。"}
    if any(term in normalized for term in ["calm", "neutral", "平靜", "中性"]):
        return {"arousal": "低", "valence": "中性", "clinical_hint": "語音模型偵測到平穩或中性情緒。"}
    return {"arousal": "未知", "valence": "未知", "clinical_hint": "語音模型標籤未映射到臨床情緒類別。"}
