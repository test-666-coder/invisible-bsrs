from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local audio pipeline steps with timing output.")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--asr-model", default=None)
    args = parser.parse_args()

    load_dotenv()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    if args.asr_model:
        os.environ["ASR_MODEL_ID"] = args.asr_model

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

    from patient_mood_pipeline.config import load_config
    from patient_mood_pipeline.local_models import analyze_voice_emotion, deidentify_with_local_ner, transcribe_audio

    config = load_config()
    audio_path = Path(args.audio)

    print(f"ASR model: {config.asr_model_id}", flush=True)
    print(f"NER model: {config.ner_model_id}", flush=True)
    print(f"Emotion model: {config.emotion_model_id}", flush=True)

    started = time.perf_counter()
    print("STEP asr:start", flush=True)
    asr = transcribe_audio(audio_path, config)
    print(f"STEP asr:done {time.perf_counter() - started:.1f}s", flush=True)
    print(asr["text"], flush=True)

    started = time.perf_counter()
    print("STEP deid:start", flush=True)
    deid = deidentify_with_local_ner(asr["text"], config)
    print(f"STEP deid:done {time.perf_counter() - started:.1f}s warnings={len(deid.warnings)}", flush=True)
    print(deid.text, flush=True)

    started = time.perf_counter()
    print("STEP emotion:start", flush=True)
    emotion = analyze_voice_emotion(audio_path, config)
    print(f"STEP emotion:done {time.perf_counter() - started:.1f}s", flush=True)
    print(emotion, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
