from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any


TRANSCRIPT_CORRECTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["corrected_transcript", "correction_summary", "changed_terms", "quality_flags"],
    "properties": {
        "corrected_transcript": {"type": "string"},
        "correction_summary": {"type": "string"},
        "changed_terms": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["before", "after", "reason"],
                "properties": {
                    "before": {"type": "string"},
                    "after": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
        },
        "quality_flags": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


def build_transcript_correction_prompt(
    deidentified_transcript: str,
    *,
    language: str = "zh-TW",
    generated_at: str | None = None,
) -> list[dict[str, str]]:
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    placeholders = sorted(set(re.findall(r"\[[A-Z_]+\]", deidentified_transcript or "")))
    return [
        {
            "role": "system",
            "content": (
                "你是醫病對話 ASR 逐字稿校對 agent。"
                "你的任務是修正明顯的語音辨識錯字、同音字、標點與說話者標籤。"
                "只能依據逐字稿本身修正，不可以新增沒有出現的症狀、否定句、計畫、診斷或個人資料。"
                "若一句話不確定，請保留原意並在 quality_flags 說明。"
                "必須完整保留所有去識別化標籤，例如 [NAME]、[MOBILE]、[ADDRESS]，不可改寫、刪除或展開。"
                "可以把明顯 ASR 誤聽的醫師/患者標籤正規化，例如「一時」改為「醫師」、「換者」改為「患者」。"
                "自殺想法、沒有自傷計畫、沒有立即衝動等安全相關語句不可擅自加強或減弱。"
                "逐字稿可能來自台灣華語、台語腔或國台語混雜語音；請優先使用台灣臨床對話常見用詞，"
                "例如「一時」可能是「醫師」、「換者」可能是「患者」、「食育」可能是「食慾」、"
                "「胸口僅僅」可能是「胸口緊緊」、「心情溫度記」可能是「心情溫度計」。"
                "也請留意「伊斯、醫失、一失」可能是「醫師」，「換著、患著」可能是「患者」，"
                "「南睡」可能是「難睡」，「待伴」可能是「待辦」，「人愛路」可能是「仁愛路」，"
                "「生遷」可能是「升遷」，「貨比不上、會不上」需依上下文判斷是否是「會不會比不上」。"
                "若台灣腔造成同音誤聽，只修正明顯錯字，不要把患者淡化或否認的語氣改成直接承認症狀。"
            ),
        },
        {
            "role": "user",
            "content": (
                f"language: {language}\n"
                f"generated_at: {generated_at}\n"
                f"placeholders_to_preserve: {json.dumps(placeholders, ensure_ascii=False)}\n\n"
                "請修正以下已去識別化 ASR 逐字稿。"
                "輸出 corrected_transcript 時請使用自然的繁體中文醫病對話逐字稿，保留醫師/患者語氣。\n\n"
                f"{deidentified_transcript}"
            ),
        },
    ]


def correct_deidentified_transcript(
    *,
    deidentified_transcript: str,
    model: str,
    language: str = "zh-TW",
    max_output_tokens: int = 20000,
) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Missing OPENAI_API_KEY. Add it to .env or the environment before running transcript correction.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Missing OpenAI SDK. Install requirements.txt before calling the OpenAI API.") from exc

    generated_at = datetime.now(timezone.utc).isoformat()
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=build_transcript_correction_prompt(
            deidentified_transcript,
            language=language,
            generated_at=generated_at,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "transcript_correction",
                "schema": TRANSCRIPT_CORRECTION_SCHEMA,
                "strict": True,
            }
        },
        max_output_tokens=max_output_tokens,
    )
    result = _load_response_json(response, step_name="逐字稿校正")
    result["model_id"] = model
    result["generated_at"] = generated_at
    result["input_placeholders"] = sorted(set(re.findall(r"\[[A-Z_]+\]", deidentified_transcript or "")))
    result["output_placeholders"] = sorted(set(re.findall(r"\[[A-Z_]+\]", result.get("corrected_transcript", ""))))
    return result


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


def _load_response_json(response, *, step_name: str) -> dict[str, Any]:
    text = _response_text(response).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        preview_start = max(0, exc.pos - 120)
        preview_end = min(len(text), exc.pos + 120)
        preview = text[preview_start:preview_end].replace("\n", " ")
        raise RuntimeError(
            f"{step_name} 的 OpenAI 回傳 JSON 不完整或格式錯誤：{exc.msg} "
            f"(line {exc.lineno}, column {exc.colno}, char {exc.pos})。"
            "常見原因是音檔/逐字稿太長造成輸出被截斷；請提高 OPENAI_TRANSCRIPT_MAX_OUTPUT_TOKENS，"
            "或縮短單次分析音檔。"
            f" 錯誤附近片段：{preview}"
        ) from exc
