from __future__ import annotations

import asyncio
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .config import load_config
from .run import run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "outputs" / "ui_runs"
UPLOAD_ROOT = PROJECT_ROOT / "outputs" / "ui_uploads"

SIDECAR_FILES = {
    "asr_transcript": "_asr_transcript.txt",
    "asr_json": "_asr.json",
    "deidentified_before_correction": "_deidentified_transcript_before_correction.txt",
    "transcript_correction": "_transcript_correction.json",
    "corrected_transcript": "_corrected_transcript.txt",
    "deidentified_transcript": "_deidentified_transcript.txt",
    "deidentification_json": "_deidentification.json",
    "voice_emotion": "_voice_emotion.json",
    "local_debug": "_local.json",
    "bsrs_json": "_bsrs.json",
}

app = FastAPI(title="Invisible BSRS Local Pipeline API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    config = load_config()
    return {
        "status": "ok",
        "models": config.to_dict(),
    }


@app.get("/api/latest-result")
def latest_result() -> dict:
    result_files = sorted(OUTPUT_ROOT.glob("*_bsrs.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not result_files:
        raise HTTPException(status_code=404, detail="目前沒有可載入的量表結果。")

    output_path = result_files[0]
    try:
        result = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"最新量表 JSON 無法讀取：{exc}") from exc

    run_id = output_path.name.removesuffix("_bsrs.json")
    intermediate_prefix = OUTPUT_ROOT / run_id
    upload_matches = sorted(UPLOAD_ROOT.glob(f"{run_id}.*"), key=lambda path: path.stat().st_mtime, reverse=True)
    upload_path = upload_matches[0] if upload_matches else UPLOAD_ROOT / f"{run_id}.wav"

    return {
        "status": "completed",
        "session_id": result.get("session", {}).get("session_id", run_id),
        "result": result,
        "files": _artifact_paths(upload_path, output_path, intermediate_prefix),
    }


@app.post("/api/analyze-audio")
async def analyze_audio(
    audio: UploadFile = File(...),
    session_id: str | None = Form(None),
    language: str = Form("zh-TW"),
    skip_transcript_correction: bool = Form(False),
) -> dict:
    if not audio.filename:
        raise HTTPException(status_code=400, detail="請上傳音檔。")

    safe_session_id = _safe_id(session_id or Path(audio.filename).stem or "ui-audio")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{safe_session_id}-{stamp}"
    suffix = Path(audio.filename).suffix.lower() or ".wav"

    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    upload_path = UPLOAD_ROOT / f"{run_id}{suffix}"
    output_path = OUTPUT_ROOT / f"{run_id}_bsrs.json"
    intermediate_prefix = OUTPUT_ROOT / run_id

    try:
        with upload_path.open("wb") as handle:
            shutil.copyfileobj(audio.file, handle)
    finally:
        await audio.close()

    try:
        run_result = await asyncio.to_thread(
            run_pipeline,
            audio=upload_path,
            output=output_path,
            session_id=run_id,
            language=language,
            skip_transcript_correction=skip_transcript_correction,
            intermediate_prefix=intermediate_prefix,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"模型分析失敗：{exc}") from exc

    return {
        "status": "completed",
        "session_id": run_id,
        "result": run_result["bsrs_report"],
        "files": _artifact_paths(upload_path, output_path, intermediate_prefix),
    }


def _safe_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    normalized = normalized.strip(".-")
    return (normalized or "ui-audio")[:80]


def _artifact_paths(upload_path: Path, output_path: Path, intermediate_prefix: Path) -> dict[str, str]:
    files = {
        "uploaded_audio": _display_path(upload_path),
        "result_json": _display_path(output_path),
    }
    for name, suffix in SIDECAR_FILES.items():
        path = intermediate_prefix.with_name(f"{intermediate_prefix.name}{suffix}")
        if path.exists():
            files[name] = _display_path(path)
    return files


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)
