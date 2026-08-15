from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from .schemas import (
    BSRS_ITEM_DEFINITIONS,
    BSRS_REPORT_SCHEMA,
    CORE_DIMENSIONS,
    DISTRESS_BANDS,
    PROMPT_VERSION,
    SCHEMA_VERSION,
    SCORE_LABELS,
    SUPPLEMENTAL_DIMENSION,
    instrument_template,
)


def build_bsrs_prompt(
    deidentified_transcript: str,
    voice_emotion: dict | None,
    *,
    session_id: str = "demo-001",
    language: str = "zh-TW",
    generated_at: str | None = None,
    model_name: str = "<model-name>",
) -> list[dict[str, str]]:
    emotion_json = json.dumps(voice_emotion or {}, ensure_ascii=False, indent=2)
    item_json = json.dumps(BSRS_ITEM_DEFINITIONS, ensure_ascii=False, indent=2)
    core_dimensions_json = json.dumps(CORE_DIMENSIONS, ensure_ascii=False, indent=2)
    distress_bands_json = json.dumps(DISTRESS_BANDS, ensure_ascii=False, indent=2)
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    return [
        {
            "role": "system",
            "content": (
                "你是協助醫療專業人員進行情緒困擾篩檢的臨床助理。"
                "請輸出 schema_version 1.1.0 的 BSRS-5 心情溫度計 AI 輔助評估草稿。"
                "這不是診斷；所有分數都需要醫療專業人員確認。"
                "若對話資訊不足，estimated_score 必須是 null，assessment_status 應為 needs_direct_confirmation 或 not_assessed。"
                "不要把沒有提及的症狀推論為完全沒有。"
                "自殺想法是第 6 題附加題，獨立評分，不納入五題總分。"
            ),
        },
        {
            "role": "user",
            "content": (
                "請使用以下固定 metadata：\n"
                f"- schema_version: {SCHEMA_VERSION}\n"
                f"- session.session_id: {session_id}\n"
                f"- session.language: {language}\n"
                "- session.status: completed\n"
                "- session.assessment_window: type=past_7_days, days=7, display_label=最近一星期，包括今天\n"
                f"- analysis_metadata.model_name: {model_name}\n"
                f"- analysis_metadata.model_version: {model_name}\n"
                f"- analysis_metadata.prompt_version: {PROMPT_VERSION}\n"
                f"- analysis_metadata.generated_at: {generated_at}\n\n"
                "BSRS-5 題目定義與 dimension_code：\n"
                f"{item_json}\n\n"
                "核心五題固定順序如下；core_items 必須剛好五個，並使用這些 item_id、item_number、dimension_code、display_label：\n"
                f"{core_dimensions_json}\n\n"
                "第六題附加題固定如下：\n"
                f"{json.dumps(SUPPLEMENTAL_DIMENSION, ensure_ascii=False, indent=2)}\n\n"
                "分數定義：0=完全沒有，1=輕微，2=中等程度，3=厲害，4=非常厲害。"
                "value.score_label 必須和 estimated_score 對應；若 estimated_score 為 null，score_label 也必須是 null。\n"
                "value.model_confidence 是 AI 信心，不是量表分數；可為 null。\n"
                "core_result.total_score 只能加總五個核心題目。只有五題 estimated_score 都不是 null 時，calculation_status 才能是 complete。\n"
                "五題總分分級如下：\n"
                f"{distress_bands_json}\n\n"
                "自殺想法附加題：若 estimated_score >= 1，derived_presence=true；0 則 false；null 則 null。"
                "若專業確認 confirmed_score 達 alert_threshold=2，alert_triggered 應為 true；尚未確認時 alert_triggered 為 null。"
                "如果逐字稿未直接詢問或回答自殺想法，請設定 requires_direct_confirmation=true，assessment_status=needs_direct_confirmation。\n\n"
                "去識別化逐字稿：\n"
                f"{deidentified_transcript}\n\n"
                "本地語音情緒模型輸出：\n"
                f"{emotion_json}"
            ),
        },
    ]


def infer_bsrs_json(
    *,
    deidentified_transcript: str,
    voice_emotion: dict | None,
    model: str,
    session_id: str = "demo-001",
    language: str = "zh-TW",
    max_output_tokens: int = 1800,
) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY. Add it to .env or the environment before running the BSRS step.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Missing OpenAI SDK. Install requirements.txt before calling the OpenAI API.") from exc

    client = OpenAI()
    generated_at = datetime.now(timezone.utc).isoformat()
    response = client.responses.create(
        model=model,
        input=build_bsrs_prompt(
            deidentified_transcript,
            voice_emotion,
            session_id=session_id,
            language=language,
            generated_at=generated_at,
            model_name=model,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "bsrs_scale_report",
                "schema": BSRS_REPORT_SCHEMA,
                "strict": True,
            }
        },
        max_output_tokens=max_output_tokens,
    )
    report = json.loads(_response_text(response))
    return normalize_bsrs_report(report, session_id=session_id, language=language, model=model, generated_at=generated_at)


def normalize_bsrs_report(
    report: dict[str, Any],
    *,
    session_id: str,
    language: str,
    model: str,
    generated_at: str,
) -> dict[str, Any]:
    normalized = deepcopy(report)
    normalized["schema_version"] = SCHEMA_VERSION
    normalized["session"] = {
        "session_id": session_id,
        "status": "completed",
        "language": language,
        "assessment_window": {
            "type": "past_7_days",
            "days": 7,
            "display_label": "最近一星期，包括今天",
        },
    }
    normalized["instrument"] = instrument_template()
    normalized["analysis_metadata"] = {
        "model_name": model,
        "model_version": model,
        "prompt_version": PROMPT_VERSION,
        "generated_at": generated_at,
    }
    _normalize_scores(normalized)
    return normalized


def _normalize_scores(report: dict[str, Any]) -> None:
    assessment = report.get("assessment", {})
    core_items = assessment.get("core_items", [])
    for expected, item in zip(CORE_DIMENSIONS, core_items):
        item["item_id"] = expected["item_id"]
        item["scale_mapping"] = {
            "item_number": expected["item_number"],
            "dimension_code": expected["dimension_code"],
            "display_label": expected["display_label"],
            "included_in_core_total": True,
        }
        _apply_score_label(item.get("value", {}))
        item.setdefault("clinician_confirmation", {"status": "pending", "confirmed_score": None, "note": None})

    scores = [item.get("value", {}).get("estimated_score") for item in core_items]
    all_scored = len(scores) == 5 and all(isinstance(score, int) for score in scores)
    core_result = assessment.setdefault("core_result", {})
    core_result["required_item_count"] = 5
    core_result["maximum_score"] = 20
    core_result["answered_item_count"] = sum(isinstance(score, int) for score in scores)
    core_result["calculation_status"] = "complete" if all_scored else "incomplete"
    if all_scored:
        total = int(sum(scores))
        core_result["total_score"] = total
        core_result["distress_level"] = _distress_band(total)
    else:
        core_result["total_score"] = None
        core_result["distress_level"] = {"code": None, "label": None, "min_score": None, "max_score": None}

    supplemental = assessment.get("supplemental_item", {})
    supplemental["item_id"] = SUPPLEMENTAL_DIMENSION["item_id"]
    supplemental["scale_mapping"] = {
        "item_number": SUPPLEMENTAL_DIMENSION["item_number"],
        "dimension_code": SUPPLEMENTAL_DIMENSION["dimension_code"],
        "display_label": SUPPLEMENTAL_DIMENSION["display_label"],
        "is_supplemental_item": True,
        "included_in_core_total": False,
    }
    value = supplemental.setdefault("value", {})
    _apply_score_label(value)
    score = value.get("estimated_score")
    value["derived_presence"] = None if score is None else bool(score >= 1)
    confirmation = supplemental.setdefault("clinician_confirmation", {})
    confirmation["alert_threshold"] = SUPPLEMENTAL_DIMENSION["alert_threshold"]
    confirmed_score = confirmation.get("confirmed_score")
    confirmation["derived_presence"] = None if confirmed_score is None else bool(confirmed_score >= 1)
    confirmation["alert_triggered"] = None if confirmed_score is None else bool(confirmed_score >= SUPPLEMENTAL_DIMENSION["alert_threshold"])


def _apply_score_label(value: dict[str, Any]) -> None:
    score = value.get("estimated_score")
    value["score_label"] = SCORE_LABELS.get(score) if isinstance(score, int) else None


def _distress_band(total: int) -> dict[str, Any]:
    for band in DISTRESS_BANDS:
        if band["min_score"] <= total <= band["max_score"]:
            return dict(band)
    return {"code": None, "label": None, "min_score": None, "max_score": None}


def _response_text(response) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    output = getattr(response, "output", None) or []
    chunks: list[str] = []
    for item in output:
        for content in getattr(item, "content", []) or []:
            value = getattr(content, "text", None)
            if value:
                chunks.append(value)
    if chunks:
        return "".join(chunks)
    raise RuntimeError("OpenAI response did not contain output_text.")
