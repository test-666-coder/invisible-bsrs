from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Redaction:
    start: int
    end: int
    label: str
    source: str
    text: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["text"] = self.text[:2] + "***" if self.text else ""
        return data


@dataclass(frozen=True)
class DeidentificationResult:
    text: str
    redactions: list[Redaction]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "redaction_count": len(self.redactions),
            "redactions": [redaction.to_dict() for redaction in self.redactions],
            "warnings": self.warnings,
        }


REGEX_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("MOBILE", re.compile(r"(?:手機|電話)\s*(?:是|為|:|：)\s*((?:[零〇○一二三四五六七八九0-9][\s-]*){8,12})")),
    ("FIELD_VALUE", re.compile(r"(姓名|病歷號|身分證|電話|手機|地址|生日|出生日期|電子郵件|email)\s*[:：]\s*[^\n，。；;]+", re.I)),
    ("NATIONAL_ID", re.compile(r"\b[A-Z][12]\d{8}\b", re.I)),
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")),
    ("MOBILE", re.compile(r"(?:\+?886[-\s]?)?0?9\d{2}[-\s]?\d{3}[-\s]?\d{3}")),
    ("PHONE", re.compile(r"0\d{1,2}[-\s]?\d{6,8}(?:#\d{1,5})?")),
    ("CARD", re.compile(r"\b\d{3,4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")),
    ("DATE", re.compile(r"(?:民國\s*)?\d{2,4}\s*[年/-]\s*\d{1,2}\s*[月/-]\s*\d{1,2}\s*日?")),
    ("DATE", re.compile(r"\d{1,2}\s*月\s*\d{1,2}\s*日")),
    ("ADDRESS", re.compile(r"(?:臺北|台北|新北|桃園|臺中|台中|臺南|台南|高雄|基隆|新竹|苗栗|彰化|南投|雲林|嘉義|屏東|宜蘭|花蓮|臺東|台東|澎湖|金門|連江)[市縣][^，。；;\n]{0,28}(?:路|街|巷|弄|號)")),
    ("ORGANIZATION", re.compile(r"[\u4e00-\u9fa5]{2,16}(?:醫院|診所|公司|學校|大學|機構)")),
    ("NAME", re.compile(r"(?:我叫|姓名[:：]?)\s*([\u4e00-\u9fa5]{2,4})")),
    ("NAME", re.compile(r"我是\s*([陳林黃張李王吳劉蔡楊許鄭謝郭洪邱曾廖賴徐周葉蘇莊呂江何蕭羅高簡朱鍾施游詹沈彭胡余盧潘顏梁趙柯翁魏孫戴范方宋鄧杜侯曹薛傅丁溫紀][\u4e00-\u9fa5]{1,2})")),
    ("NAME_TITLE", re.compile(r"[陳林黃張李王吳劉蔡楊許鄭謝郭洪邱曾廖賴徐周葉蘇莊呂江何蕭羅高簡朱鍾施游詹沈彭胡余盧潘顏梁趙柯翁魏孫戴范方宋鄧杜侯曹薛傅丁溫紀][\u4e00-\u9fa5]{1,2}(?:先生|小姐|女士|太太|醫師|醫生|主任|護理師)")),
]

NER_LABEL_MAP = {
    "PERSON": "NAME",
    "PER": "NAME",
    "ORG": "ORGANIZATION",
    "GPE": "LOCATION",
    "LOC": "LOCATION",
    "LOCATION": "LOCATION",
    "FAC": "LOCATION",
    "DATE": "DATE",
    "TIME": "DATE",
}

GENERIC_TIME_TERMS = {
    "今天",
    "昨天",
    "前天",
    "明天",
    "最近",
    "這幾天",
    "这几天",
    "這幾",
    "这几",
    "半夜",
    "每天",
    "一週",
    "一周",
}


def redact_text(
    text: str,
    ner_entities: Iterable[dict] | None = None,
    warnings: list[str] | None = None,
) -> DeidentificationResult:
    source_text = text or ""
    redactions = _regex_redactions(source_text)
    if ner_entities:
        redactions.extend(_ner_redactions(source_text, ner_entities))

    merged = _merge_redactions(redactions)
    output = source_text
    for redaction in sorted(merged, key=lambda item: item.start, reverse=True):
        replacement = f"[{redaction.label}]"
        output = output[: redaction.start] + replacement + output[redaction.end :]

    return DeidentificationResult(text=output, redactions=merged, warnings=warnings or [])


def _regex_redactions(text: str) -> list[Redaction]:
    redactions: list[Redaction] = []
    for label, pattern in REGEX_PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span(1) if label in {"MOBILE", "NAME"} and match.lastindex else match.span()
            redactions.append(Redaction(start=start, end=end, label=label, source="regex", text=text[start:end]))
    return redactions


def _ner_redactions(text: str, entities: Iterable[dict]) -> list[Redaction]:
    redactions: list[Redaction] = []
    for entity in entities:
        raw_label = str(entity.get("entity_group") or entity.get("entity") or "").replace("B-", "").replace("I-", "")
        label = NER_LABEL_MAP.get(raw_label.upper())
        start = entity.get("start")
        end = entity.get("end")
        if label is None or start is None or end is None:
            continue
        if int(end) <= int(start):
            continue
        entity_text = text[int(start) : int(end)]
        stripped = entity_text.strip()
        if label == "DATE" and (stripped in GENERIC_TIME_TERMS or (len(stripped) <= 4 and not re.search(r"\d", stripped))):
            continue
        redactions.append(
            Redaction(
                start=int(start),
                end=int(end),
                label=label,
                source="ner",
                text=entity_text,
            )
        )
    return redactions


def _merge_redactions(redactions: list[Redaction]) -> list[Redaction]:
    if not redactions:
        return []

    ordered = sorted(redactions, key=lambda item: (item.start, -(item.end - item.start)))
    merged: list[Redaction] = []
    for item in ordered:
        if not merged or item.start > merged[-1].end:
            merged.append(item)
            continue

        previous = merged[-1]
        if item.end > previous.end:
            label = previous.label if previous.source == "regex" else item.label
            source = "regex+ner" if previous.source != item.source else previous.source
            merged[-1] = Redaction(
                start=previous.start,
                end=item.end,
                label=label,
                source=source,
                text=previous.text,
            )
    return merged
