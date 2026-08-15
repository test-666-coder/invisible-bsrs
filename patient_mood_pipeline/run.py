from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .config import default_output_path, load_config
from .local_models import analyze_voice_emotion, deidentify_with_local_ner, transcribe_audio
from .openai_bsrs import infer_bsrs_json


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = load_config()

    if not args.audio and not args.transcript_file:
        raise SystemExit("請提供 --audio 或 --transcript-file。")

    audio_path = Path(args.audio).expanduser().resolve() if args.audio else None
    transcript_source = "transcript_file" if args.transcript_file else "local_asr"

    asr_result = None
    if args.transcript_file:
        transcript = Path(args.transcript_file).read_text(encoding="utf-8").strip()
    else:
        asr_result = transcribe_audio(audio_path, config)
        transcript = asr_result["text"]

    deid_result = deidentify_with_local_ner(transcript, config)
    voice_emotion = analyze_voice_emotion(audio_path, config) if audio_path else None

    bsrs_report = None
    if not args.local_only:
        bsrs_report = infer_bsrs_json(
            deidentified_transcript=deid_result.text,
            voice_emotion=voice_emotion,
            model=args.openai_model or config.openai_model,
            session_id=args.session_id,
            language=args.language,
        )

    debug_output = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": "0.2.0",
        "transcript_source": transcript_source,
        "models": config.to_dict(),
        "audio_file": str(audio_path) if audio_path else None,
        "asr": asr_result,
        "deidentification": deid_result.to_dict(),
        "voice_emotion": voice_emotion,
        "bsrs_report": bsrs_report,
    }
    if args.include_raw:
        debug_output["raw_transcript"] = transcript

    output = debug_output if args.local_only or args.debug_envelope else bsrs_report

    output_path = Path(args.output or default_output_path()).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a clinical conversation audio file into BSRS JSON.")
    parser.add_argument("--audio", help="Path to conversation audio file, e.g. wav/mp3/m4a.")
    parser.add_argument("--transcript-file", help="Use an existing transcript instead of local ASR.")
    parser.add_argument("--output", help="Output JSON path.", default=str(default_output_path()))
    parser.add_argument("--openai-model", help="Override OPENAI_BSRS_MODEL for the BSRS JSON step.")
    parser.add_argument("--session-id", default="demo-001", help="Session id written into the final BSRS JSON.")
    parser.add_argument("--language", default="zh-TW", help="Session language written into the final BSRS JSON.")
    parser.add_argument("--local-only", action="store_true", help="Skip OpenAI and write local intermediate outputs only.")
    parser.add_argument("--debug-envelope", action="store_true", help="Wrap the final report with local pipeline intermediates.")
    parser.add_argument("--include-raw", action="store_true", help="Store raw transcript in output JSON. Off by default.")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
