from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .deidentify import DeidentificationResult, redact_text


class LocalModelError(RuntimeError):
    pass


EMOTION_LABEL_DETAILS = {
    "angry": {
        "zh_label": "煩躁/生氣",
        "family": "irritability_agitation",
        "valence": "負向",
        "arousal": "高",
        "valence_value": -0.9,
        "arousal_value": 0.85,
        "clinical_note": "語音呈現高喚起負向情緒，可能反映煩躁、壓力或防衛感。",
    },
    "fearful": {
        "zh_label": "害怕/焦慮",
        "family": "anxiety_fear",
        "valence": "負向",
        "arousal": "高",
        "valence_value": -0.85,
        "arousal_value": 0.75,
        "clinical_note": "語音呈現高喚起負向情緒，可能反映緊張、擔心或不安全感。",
    },
    "disgust": {
        "zh_label": "厭惡/抗拒",
        "family": "aversion_resistance",
        "valence": "負向",
        "arousal": "中高",
        "valence_value": -0.75,
        "arousal_value": 0.55,
        "clinical_note": "語音可能帶有抗拒、挫折或不耐感。",
    },
    "sad": {
        "zh_label": "悲傷/低落",
        "family": "low_mood",
        "valence": "負向",
        "arousal": "低",
        "valence_value": -0.8,
        "arousal_value": -0.45,
        "clinical_note": "語音可能反映低落、疲憊或退縮感。",
    },
    "surprised": {
        "zh_label": "驚訝/警覺",
        "family": "heightened_alert",
        "valence": "混合",
        "arousal": "高",
        "valence_value": -0.1,
        "arousal_value": 0.65,
        "clinical_note": "語音可能有警覺、緊繃或突發反應。",
    },
    "calm": {
        "zh_label": "平靜/穩定",
        "family": "calm_neutral",
        "valence": "中性",
        "arousal": "低",
        "valence_value": 0.05,
        "arousal_value": -0.55,
        "clinical_note": "語音較平穩或中性。",
    },
    "happy": {
        "zh_label": "愉悅/正向",
        "family": "positive_affect",
        "valence": "正向",
        "arousal": "中",
        "valence_value": 0.8,
        "arousal_value": 0.25,
        "clinical_note": "語音偏正向；仍需結合逐字稿判讀。",
    },
}


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
    profile = summarize_emotion_scores(scores)
    interpreted = profile["dominant_emotion"]
    return {
        "model_id": config.emotion_model_id,
        "dominant_label": dominant["label"],
        "dominant_score": float(dominant["score"]),
        "arousal": interpreted["arousal"],
        "valence": interpreted["valence"],
        "clinical_hint": profile["clinical_summary"],
        "emotion_profile": profile,
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
    if device != -1 and task == "automatic-speech-recognition":
        pipe_kwargs["dtype"] = torch.float16
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
    scores = [
        {
            "label": str(item.get("label", "")),
            "score": float(item.get("score", 0)),
        }
        for item in (raw or [])
    ]
    return sorted(scores, key=lambda item: item["score"], reverse=True)


def summarize_emotion_scores(scores: list[dict]) -> dict:
    enriched = []
    for item in scores:
        detail = _emotion_detail(str(item.get("label", "")))
        score = float(item.get("score", 0))
        enriched.append(
            {
                "label": str(item.get("label", "")),
                "zh_label": detail["zh_label"],
                "family": detail["family"],
                "score": score,
                "valence": detail["valence"],
                "arousal": detail["arousal"],
                "clinical_note": detail["clinical_note"],
            }
        )

    dominant = enriched[0] if enriched else _unknown_emotion_detail()
    valence_score = sum(float(item.get("score", 0)) * _emotion_detail(str(item.get("label", "")))["valence_value"] for item in scores)
    arousal_score = sum(float(item.get("score", 0)) * _emotion_detail(str(item.get("label", "")))["arousal_value"] for item in scores)
    negative_affect_score = sum(
        float(item.get("score", 0))
        for item in scores
        if _emotion_detail(str(item.get("label", "")))["valence_value"] < -0.2
    )
    agitation_score = sum(
        float(item.get("score", 0))
        for item in scores
        if _emotion_detail(str(item.get("label", "")))["family"] in {"irritability_agitation", "anxiety_fear", "aversion_resistance"}
    )
    low_mood_score = sum(
        float(item.get("score", 0))
        for item in scores
        if _emotion_detail(str(item.get("label", "")))["family"] == "low_mood"
    )

    return {
        "dominant_emotion": {
            "label": dominant["label"],
            "zh_label": dominant["zh_label"],
            "family": dominant["family"],
            "score": dominant["score"],
            "valence": dominant["valence"],
            "arousal": dominant["arousal"],
            "clinical_note": dominant["clinical_note"],
        },
        "top_emotions": enriched[:3],
        "dimensional_scores": {
            "valence_score": round(valence_score, 4),
            "valence_label": _valence_label(valence_score),
            "arousal_score": round(arousal_score, 4),
            "arousal_label": _arousal_label(arousal_score),
            "negative_affect_score": round(negative_affect_score, 4),
            "agitation_score": round(agitation_score, 4),
            "low_mood_score": round(low_mood_score, 4),
        },
        "clinical_summary": _emotion_clinical_summary(dominant, valence_score, arousal_score, negative_affect_score),
        "interpretation_note": "語音情緒僅反映聲學特徵，不能單獨作為量表分數；需與逐字稿和醫師確認合併判讀。",
    }


def _interpret_emotion_label(label: str) -> dict:
    detail = _emotion_detail(label)
    return {
        "arousal": detail["arousal"],
        "valence": detail["valence"],
        "clinical_hint": detail["clinical_note"],
    }


def _emotion_detail(label: str) -> dict:
    normalized = label.lower()
    for key, detail in EMOTION_LABEL_DETAILS.items():
        if key in normalized:
            return detail
    if any(term in normalized for term in ["anger", "frustrat", "焦慮", "害怕", "生氣"]):
        return EMOTION_LABEL_DETAILS["angry"]
    if any(term in normalized for term in ["fear"]):
        return EMOTION_LABEL_DETAILS["fearful"]
    if any(term in normalized for term in ["depress", "悲", "低落", "難過"]):
        return EMOTION_LABEL_DETAILS["sad"]
    if any(term in normalized for term in ["joy", "開心"]):
        return EMOTION_LABEL_DETAILS["happy"]
    if any(term in normalized for term in ["neutral", "平靜", "中性"]):
        return EMOTION_LABEL_DETAILS["calm"]
    return {
        "zh_label": "未知",
        "family": "unknown",
        "valence": "未知",
        "arousal": "未知",
        "valence_value": 0.0,
        "arousal_value": 0.0,
        "clinical_note": "語音模型標籤未映射到細分類。",
    }


def _unknown_emotion_detail() -> dict:
    return {
        "label": "unknown",
        "zh_label": "未知",
        "family": "unknown",
        "score": 0.0,
        "valence": "未知",
        "arousal": "未知",
        "clinical_note": "沒有可用的語音情緒分數。",
    }


def _valence_label(value: float) -> str:
    if value <= -0.35:
        return "負向"
    if value >= 0.35:
        return "正向"
    return "中性或混合"


def _arousal_label(value: float) -> str:
    if value >= 0.45:
        return "高"
    if value <= -0.2:
        return "低"
    return "中"


def _emotion_clinical_summary(dominant: dict, valence_score: float, arousal_score: float, negative_affect_score: float) -> str:
    valence = _valence_label(valence_score)
    arousal = _arousal_label(arousal_score)
    if negative_affect_score >= 0.65:
        return f"語音整體偏{valence}、{arousal}喚起，主要落在「{dominant['zh_label']}」；建議結合逐字稿確認是焦慮、煩躁、低落或防衛語氣。"
    return f"語音整體為{valence}、{arousal}喚起，主要聲學分類為「{dominant['zh_label']}」；此結果需與逐字稿合併判讀。"
