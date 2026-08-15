from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    asr_model_id: str
    ner_model_id: str
    emotion_model_id: str
    openai_model: str
    transcript_correction_model: str
    asr_language: str
    hf_device: str
    hf_cache_dir: str | None
    ner_chunk_chars: int

    def to_dict(self) -> dict:
        return asdict(self)


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def load_config() -> PipelineConfig:
    try:
        from dotenv import load_dotenv

        load_dotenv(override=True)
    except ImportError:
        pass

    openai_model = os.getenv("OPENAI_BSRS_MODEL", "gpt-4o-mini")

    return PipelineConfig(
        asr_model_id=os.getenv("ASR_MODEL_ID", "openai/whisper-small"),
        ner_model_id=os.getenv("NER_MODEL_ID", "ckiplab/albert-tiny-chinese-ner"),
        emotion_model_id=os.getenv("EMOTION_MODEL_ID", "Dpngtm/wav2vec2-emotion-recognition"),
        openai_model=openai_model,
        transcript_correction_model=os.getenv("OPENAI_TRANSCRIPT_MODEL", openai_model),
        asr_language=os.getenv("ASR_LANGUAGE", "zh"),
        hf_device=os.getenv("HF_DEVICE", "auto"),
        hf_cache_dir=os.getenv("HF_HOME") or os.getenv("TRANSFORMERS_CACHE"),
        ner_chunk_chars=_env_int("NER_CHUNK_CHARS", 450),
    )


def default_output_path() -> Path:
    return Path("outputs") / "bsrs_result.json"
