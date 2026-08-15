from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    asr_backend: str
    asr_model_id: str
    ner_model_id: str
    emotion_model_id: str
    openai_model: str
    transcript_correction_model: str
    openai_reasoning_effort: str | None
    bsrs_system_prompt_file: str | None
    bsrs_system_prompt_inline: bool
    asr_language: str
    asr_num_beams: int
    asr_chunk_length_s: int
    asr_stride_length_s: int
    asr_compute_type: str
    asr_cpu_compute_type: str
    asr_vad_filter: bool
    asr_condition_on_previous_text: bool
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


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> PipelineConfig:
    try:
        from dotenv import load_dotenv

        load_dotenv(override=True)
    except ImportError:
        pass

    openai_model = os.getenv("OPENAI_BSRS_MODEL", "gpt-5.6-sol")
    system_prompt_inline = os.getenv("BSRS_SYSTEM_PROMPT")

    return PipelineConfig(
        asr_backend=os.getenv("ASR_BACKEND", "faster-whisper"),
        asr_model_id=os.getenv("ASR_MODEL_ID", "Systran/faster-whisper-medium"),
        ner_model_id=os.getenv("NER_MODEL_ID", "ckiplab/albert-tiny-chinese-ner"),
        emotion_model_id=os.getenv("EMOTION_MODEL_ID", "Dpngtm/wav2vec2-emotion-recognition"),
        openai_model=openai_model,
        transcript_correction_model=os.getenv("OPENAI_TRANSCRIPT_MODEL", "gpt-4o-mini"),
        openai_reasoning_effort=_env_str("OPENAI_BSRS_REASONING_EFFORT"),
        bsrs_system_prompt_file=_env_str("BSRS_SYSTEM_PROMPT_FILE"),
        bsrs_system_prompt_inline=bool(system_prompt_inline and system_prompt_inline.strip()),
        asr_language=os.getenv("ASR_LANGUAGE", "zh"),
        asr_num_beams=_env_int("ASR_NUM_BEAMS", 5),
        asr_chunk_length_s=_env_int("ASR_CHUNK_LENGTH_S", 30),
        asr_stride_length_s=_env_int("ASR_STRIDE_LENGTH_S", 5),
        asr_compute_type=os.getenv("ASR_COMPUTE_TYPE", "int8_float16"),
        asr_cpu_compute_type=os.getenv("ASR_CPU_COMPUTE_TYPE", "int8"),
        asr_vad_filter=_env_bool("ASR_VAD_FILTER", True),
        asr_condition_on_previous_text=_env_bool("ASR_CONDITION_ON_PREVIOUS_TEXT", False),
        hf_device=os.getenv("HF_DEVICE", "auto"),
        hf_cache_dir=os.getenv("HF_HOME") or os.getenv("TRANSFORMERS_CACHE"),
        ner_chunk_chars=_env_int("NER_CHUNK_CHARS", 450),
    )


def default_output_path() -> Path:
    return Path("outputs") / "bsrs_result.json"


def load_bsrs_system_prompt(config: PipelineConfig | None = None) -> str | None:
    config = config or load_config()

    inline_prompt = os.getenv("BSRS_SYSTEM_PROMPT")
    if inline_prompt and inline_prompt.strip():
        return inline_prompt.strip()

    if not config.bsrs_system_prompt_file:
        return None

    prompt_path = Path(config.bsrs_system_prompt_file).expanduser()
    if not prompt_path.is_absolute():
        prompt_path = Path.cwd() / prompt_path
    return prompt_path.read_text(encoding="utf-8").strip()


def _env_str(name: str) -> str | None:
    raw = os.getenv(name)
    if raw is None:
        return None
    value = raw.strip()
    return value or None
