from __future__ import annotations

import json
import os
import re
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


DEFAULT_BSRS_SYSTEM_PROMPT = (
    "你是協助醫療專業人員進行情緒困擾篩檢的臨床助理。"
    "請輸出 schema_version 1.1.0 的 BSRS-5 心情溫度計 AI 輔助評估草稿。"
    "這不是診斷；所有分數都需要醫療專業人員確認。"
    "所有可自由生成的中文欄位請使用繁體中文與台灣用語，不要輸出簡體字。"
    "若對話資訊不足，estimated_score 必須是 null，assessment_status 應為 needs_direct_confirmation 或 not_assessed。"
    "不要把沒有提及的症狀推論為完全沒有。"
    "臨床訪談中患者常會淡化、合理化或否認症狀；評分時請優先看具體生活證據、睡眠變化、功能受損、家人觀察、行為反應與安全語句。"
    "不需要患者直接說出量表題目名稱；若有足夠間接證據，仍可估分，並在 model_confidence 與 rationale_summary 說明患者有淡化或否認。"
    "只有完全沒有相關線索、ASR 內容無法判讀，或證據互相矛盾到無法估計時，核心五題才使用 null。"
    "自殺想法是第 6 題附加題，獨立評分，不納入五題總分。"
)


def build_bsrs_prompt(
    deidentified_transcript: str,
    voice_emotion: dict | None,
    *,
    session_id: str = "demo-001",
    language: str = "zh-TW",
    generated_at: str | None = None,
    model_name: str = "<model-name>",
    system_prompt: str | None = None,
) -> list[dict[str, str]]:
    emotion_json = json.dumps(voice_emotion or {}, ensure_ascii=False, indent=2)
    item_json = json.dumps(BSRS_ITEM_DEFINITIONS, ensure_ascii=False, indent=2)
    core_dimensions_json = json.dumps(CORE_DIMENSIONS, ensure_ascii=False, indent=2)
    distress_bands_json = json.dumps(DISTRESS_BANDS, ensure_ascii=False, indent=2)
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    system_content = (system_prompt or DEFAULT_BSRS_SYSTEM_PROMPT).strip()
    return [
        {
            "role": "system",
            "content": system_content,
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
                "間接證據評分規則：患者說「還好、只是累、沒那麼嚴重、不是憂鬱」不可直接視為 0 分；"
                "若同段對話同時有反覆失眠、緊繃、功能下降、家人觀察、易衝動反應、自責或不想醒來等具體例子，"
                "請依具體例子的頻率與影響估分，並將 evidence_sufficiency 設為 sufficient 或 partial。\n"
                "低嚴重度與保護因子規則：若患者描述的是偶發、短暫、可自行調節、未造成明顯功能受損，"
                "且仍能工作、運動、社交、維持家庭互動或期待未來，核心題目通常應評為 0 或 1。"
                "不要把「偶爾急一下但能察覺並修正」、「專案前一天較晚睡但不是每天」、「看到同事升遷會想更努力但不持續否定自己」"
                "放大成 2 分以上；除非有反覆、持續、失控、明顯困擾或功能下降的證據。\n"
                "core_result.total_score 只能加總五個核心題目。只有五題 estimated_score 都不是 null 時，calculation_status 才能是 complete。\n"
                "五題總分分級如下：\n"
                f"{distress_bands_json}\n\n"
                "自殺想法附加題：若 estimated_score >= 1，derived_presence=true；0 則 false；null 則 null。"
                "若專業確認 confirmed_score 達 alert_threshold=2，alert_triggered 應為 true；尚未確認時 alert_triggered 為 null。"
                "如果逐字稿未直接詢問或回答自殺想法，請設定 requires_direct_confirmation=true，assessment_status=needs_direct_confirmation。"
                "如果醫師已直接詢問不想活、想傷害自己、希望消失、自殺或輕生等安全問題，且患者明確回答沒有或完全沒有，"
                "estimated_score 應為 0、score_label 應為「完全沒有」、derived_presence=false、"
                "assessment_status=estimated、requires_direct_confirmation=false，並引用該否認語句作為 evidence。\n\n"
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
    max_output_tokens: int = 6000,
    system_prompt: str | None = None,
    reasoning_effort: str | None = None,
) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY. Add it to .env or the environment before running the BSRS step.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Missing OpenAI SDK. Install requirements.txt before calling the OpenAI API.") from exc

    client = OpenAI()
    generated_at = datetime.now(timezone.utc).isoformat()
    request: dict[str, Any] = {
        "model": model,
        "input": build_bsrs_prompt(
            deidentified_transcript,
            voice_emotion,
            session_id=session_id,
            language=language,
            generated_at=generated_at,
            model_name=model,
            system_prompt=system_prompt,
        ),
        "text": {
            "format": {
                "type": "json_schema",
                "name": "bsrs_scale_report",
                "schema": BSRS_REPORT_SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
    }
    if reasoning_effort:
        request["reasoning"] = {"effort": reasoning_effort}

    response = client.responses.create(**request)
    report = json.loads(_response_text(response))
    return normalize_bsrs_report(
        report,
        session_id=session_id,
        language=language,
        model=model,
        generated_at=generated_at,
        deidentified_transcript=deidentified_transcript,
    )


def normalize_bsrs_report(
    report: dict[str, Any],
    *,
    session_id: str,
    language: str,
    model: str,
    generated_at: str,
    deidentified_transcript: str | None = None,
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
    if deidentified_transcript:
        _normalize_direct_safety_denial(normalized, deidentified_transcript)
    _normalize_summary(normalized)
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
    if score == 0:
        value["assessment_status"] = "estimated"
        supplemental["requires_direct_confirmation"] = False
    elif isinstance(score, int):
        value["assessment_status"] = "estimated"
        supplemental["requires_direct_confirmation"] = True
    else:
        supplemental["requires_direct_confirmation"] = True
    confirmation = supplemental.setdefault("clinician_confirmation", {})
    confirmation["alert_threshold"] = SUPPLEMENTAL_DIMENSION["alert_threshold"]
    confirmed_score = confirmation.get("confirmed_score")
    confirmation["derived_presence"] = None if confirmed_score is None else bool(confirmed_score >= 1)
    confirmation["alert_triggered"] = None if confirmed_score is None else bool(confirmed_score >= SUPPLEMENTAL_DIMENSION["alert_threshold"])


def _normalize_direct_safety_denial(report: dict[str, Any], transcript: str) -> None:
    quote = _direct_safety_denial_quote(transcript)
    if not quote:
        return

    supplemental = report.get("assessment", {}).get("supplemental_item", {})
    value = supplemental.setdefault("value", {})
    current_score = value.get("estimated_score")
    if isinstance(current_score, int) and current_score >= 1:
        return

    value["estimated_score"] = 0
    value["score_label"] = SCORE_LABELS[0]
    value["derived_presence"] = False
    value["model_confidence"] = value.get("model_confidence") or 0.9
    value["evidence_sufficiency"] = "sufficient"
    value["assessment_status"] = "estimated"
    supplemental["requires_direct_confirmation"] = False
    supplemental["rationale_summary"] = "醫師已直接詢問自傷或不想活相關安全問題，患者明確否認。"
    if not supplemental.get("evidence"):
        supplemental["evidence"] = [
            {
                "evidence_id": "ev-suicide-denial-001",
                "transcript_segment_id": "safety-denial",
                "speaker": "patient",
                "quote": quote,
            }
        ]


def _direct_safety_denial_quote(transcript: str) -> str | None:
    normalized = re.sub(r"\s+", "", transcript or "")
    safety_pattern = re.compile(r"(不想活|傷害自己|希望自己消失|自殺|輕生|想死)")
    denial_pattern = re.compile(r"(患者|病患|個案|當事人)?[，,。？?：:、]*(沒有|完全沒有|沒有這個|沒有這種|否認|不會)")
    positive_pattern = re.compile(r"(想死|不想活|傷害自己|自殺|輕生|活不下去|不想醒來)")
    for match in safety_pattern.finditer(normalized):
        window = normalized[match.end() : match.end() + 100]
        denial = denial_pattern.search(window)
        if not denial:
            continue
        before = normalized[max(0, match.start() - 80) : match.start()]
        if re.search(r"(患者|病患|個案|當事人)[^。？?]{0,40}" + positive_pattern.pattern, before):
            continue
        return denial.group(0).strip("，,。？?：:、") or "沒有，這個完全沒有。"
    return None


def _normalize_summary(report: dict[str, Any]) -> None:
    assessment = report.setdefault("assessment", {})
    summary = assessment.setdefault("summary", {})
    core_result = assessment.get("core_result", {})
    distress_level = core_result.get("distress_level") or {}
    summary["distress_level"] = distress_level.get("code")

    supplemental = assessment.get("supplemental_item", {})
    score = supplemental.get("value", {}).get("estimated_score")
    if score is None:
        summary["safety_status"] = "needs_direct_confirmation"
    elif isinstance(score, int) and score >= SUPPLEMENTAL_DIMENSION["alert_threshold"]:
        summary["safety_status"] = "needs_professional_review"
    else:
        summary["safety_status"] = "no_alert"
    summary.setdefault("priority_dimension_codes", [])
    summary.setdefault("distress_summary", "")


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
