from __future__ import annotations

SCHEMA_VERSION = "1.1.0"
PROMPT_VERSION = "bsrs-conversation-v1"

SCORE_SCALE = [
    {"value": 0, "label": "完全沒有"},
    {"value": 1, "label": "輕微"},
    {"value": 2, "label": "中等程度"},
    {"value": 3, "label": "厲害"},
    {"value": 4, "label": "非常厲害"},
]

SCORE_LABELS = {item["value"]: item["label"] for item in SCORE_SCALE}

CORE_DIMENSIONS = [
    {
        "item_id": "bsrs5-sleep",
        "item_number": 1,
        "dimension_code": "sleep_disturbance",
        "display_label": "睡眠困擾",
        "question": "睡眠困難，譬如難以入睡、易醒或早醒。",
    },
    {
        "item_id": "bsrs5-anxiety",
        "item_number": 2,
        "dimension_code": "anxiety",
        "display_label": "緊張不安",
        "question": "感覺緊張不安。",
    },
    {
        "item_id": "bsrs5-irritability",
        "item_number": 3,
        "dimension_code": "irritability",
        "display_label": "容易苦惱或動怒",
        "question": "覺得容易苦惱或動怒。",
    },
    {
        "item_id": "bsrs5-depressed-mood",
        "item_number": 4,
        "dimension_code": "depressed_mood",
        "display_label": "憂鬱或心情低落",
        "question": "感覺憂鬱、心情低落。",
    },
    {
        "item_id": "bsrs5-inferiority",
        "item_number": 5,
        "dimension_code": "inferiority",
        "display_label": "覺得比不上別人",
        "question": "覺得比不上別人。",
    },
]

SUPPLEMENTAL_DIMENSION = {
    "item_id": "bsrs-suicide-ideation",
    "item_number": 6,
    "dimension_code": "suicide_ideation",
    "display_label": "自殺想法",
    "question": "有自殺的想法。",
    "alert_threshold": 2,
}

DISTRESS_BANDS = [
    {"code": "good_adaptation", "label": "身心適應狀況良好", "min_score": 0, "max_score": 5},
    {"code": "mild_distress", "label": "輕度情緒困擾", "min_score": 6, "max_score": 9},
    {"code": "moderate_distress", "label": "中度情緒困擾", "min_score": 10, "max_score": 14},
    {"code": "severe_distress", "label": "重度情緒困擾", "min_score": 15, "max_score": 20},
]

BSRS_ITEM_DEFINITIONS = {
    item["dimension_code"]: item["question"] for item in CORE_DIMENSIONS
} | {
    SUPPLEMENTAL_DIMENSION["dimension_code"]: (
        f"{SUPPLEMENTAL_DIMENSION['question']} 附加題，不納入五題總分；"
        f"{SUPPLEMENTAL_DIMENSION['alert_threshold']} 分以上需專業評估。"
    )
}


def instrument_template() -> dict:
    return {
        "code": "BSRS-5",
        "display_name": "心情溫度計",
        "form_profile": "taipei_online_order",
        "assessment_mode": "ai_assisted_draft",
        "score_scale": SCORE_SCALE,
        "core_total_rule": {
            "included_dimension_codes": [item["dimension_code"] for item in CORE_DIMENSIONS],
            "score_range": {"min": 0, "max": 20},
            "severity_bands": DISTRESS_BANDS,
        },
        "supplemental_item_rule": {
            "dimension_code": SUPPLEMENTAL_DIMENSION["dimension_code"],
            "included_in_core_total": False,
            "score_range": {"min": 0, "max": 4},
            "professional_review_threshold": SUPPLEMENTAL_DIMENSION["alert_threshold"],
        },
    }


NULLABLE_SCORE = {"type": ["integer", "null"], "minimum": 0, "maximum": 4}
NULLABLE_STRING = {"type": ["string", "null"]}
NULLABLE_NUMBER = {"type": ["number", "null"], "minimum": 0, "maximum": 1}
NULLABLE_BOOLEAN = {"type": ["boolean", "null"]}


SCORE_RANGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["min", "max"],
    "properties": {
        "min": {"type": "integer"},
        "max": {"type": "integer"},
    },
}


SEVERITY_BAND_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["code", "label", "min_score", "max_score"],
    "properties": {
        "code": {"type": "string"},
        "label": {"type": "string"},
        "min_score": {"type": "integer"},
        "max_score": {"type": "integer"},
    },
}


SCALE_MAPPING_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["item_number", "dimension_code", "display_label", "included_in_core_total"],
    "properties": {
        "item_number": {"type": "integer", "minimum": 1, "maximum": 6},
        "dimension_code": {"type": "string"},
        "display_label": {"type": "string"},
        "included_in_core_total": {"type": "boolean"},
    },
}


SUPPLEMENTAL_SCALE_MAPPING_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["item_number", "dimension_code", "display_label", "is_supplemental_item", "included_in_core_total"],
    "properties": {
        "item_number": {"type": "integer", "minimum": 6, "maximum": 6},
        "dimension_code": {"type": "string"},
        "display_label": {"type": "string"},
        "is_supplemental_item": {"type": "boolean"},
        "included_in_core_total": {"type": "boolean"},
    },
}


VALUE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "estimated_score",
        "score_label",
        "model_confidence",
        "evidence_sufficiency",
        "assessment_status",
    ],
    "properties": {
        "estimated_score": NULLABLE_SCORE,
        "score_label": NULLABLE_STRING,
        "model_confidence": NULLABLE_NUMBER,
        "evidence_sufficiency": {
            "type": "string",
            "enum": ["sufficient", "partial", "insufficient"],
        },
        "assessment_status": {
            "type": "string",
            "enum": ["estimated", "needs_direct_confirmation", "not_assessed"],
        },
    },
}


SUPPLEMENTAL_VALUE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "estimated_score",
        "score_label",
        "derived_presence",
        "model_confidence",
        "evidence_sufficiency",
        "assessment_status",
    ],
    "properties": {
        "estimated_score": NULLABLE_SCORE,
        "score_label": NULLABLE_STRING,
        "derived_presence": NULLABLE_BOOLEAN,
        "model_confidence": NULLABLE_NUMBER,
        "evidence_sufficiency": {
            "type": "string",
            "enum": ["sufficient", "partial", "insufficient"],
        },
        "assessment_status": {
            "type": "string",
            "enum": ["estimated", "needs_direct_confirmation", "not_assessed"],
        },
    },
}


EVIDENCE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["evidence_id", "transcript_segment_id", "speaker", "quote"],
    "properties": {
        "evidence_id": {"type": "string"},
        "transcript_segment_id": {"type": "string"},
        "speaker": {"type": "string", "enum": ["patient", "doctor", "clinician", "unknown"]},
        "quote": {"type": "string"},
    },
}


CORE_CLINICIAN_CONFIRMATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["status", "confirmed_score", "note"],
    "properties": {
        "status": {"type": "string", "enum": ["pending", "confirmed", "overridden", "not_applicable"]},
        "confirmed_score": NULLABLE_SCORE,
        "note": NULLABLE_STRING,
    },
}


SUPPLEMENTAL_CLINICIAN_CONFIRMATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["status", "confirmed_score", "derived_presence", "alert_threshold", "alert_triggered"],
    "properties": {
        "status": {"type": "string", "enum": ["required", "pending", "confirmed", "overridden"]},
        "confirmed_score": NULLABLE_SCORE,
        "derived_presence": NULLABLE_BOOLEAN,
        "alert_threshold": {"type": "integer", "minimum": 2, "maximum": 2},
        "alert_triggered": NULLABLE_BOOLEAN,
    },
}


CORE_ITEM_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "item_id",
        "scale_mapping",
        "value",
        "evidence",
        "rationale_summary",
        "clinician_confirmation",
    ],
    "properties": {
        "item_id": {"type": "string"},
        "scale_mapping": SCALE_MAPPING_SCHEMA,
        "value": VALUE_SCHEMA,
        "evidence": {"type": "array", "items": EVIDENCE_SCHEMA, "maxItems": 5},
        "rationale_summary": {"type": "string"},
        "clinician_confirmation": CORE_CLINICIAN_CONFIRMATION_SCHEMA,
    },
}


BSRS_REPORT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "session",
        "instrument",
        "assessment",
        "clinical_review",
        "analysis_metadata",
    ],
    "properties": {
        "schema_version": {"type": "string"},
        "session": {
            "type": "object",
            "additionalProperties": False,
            "required": ["session_id", "status", "language", "assessment_window"],
            "properties": {
                "session_id": {"type": "string"},
                "status": {"type": "string", "enum": ["completed", "partial", "failed"]},
                "language": {"type": "string"},
                "assessment_window": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["type", "days", "display_label"],
                    "properties": {
                        "type": {"type": "string", "enum": ["past_7_days"]},
                        "days": {"type": "integer", "minimum": 7, "maximum": 7},
                        "display_label": {"type": "string"},
                    },
                },
            },
        },
        "instrument": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "code",
                "display_name",
                "form_profile",
                "assessment_mode",
                "score_scale",
                "core_total_rule",
                "supplemental_item_rule",
            ],
            "properties": {
                "code": {"type": "string"},
                "display_name": {"type": "string"},
                "form_profile": {"type": "string"},
                "assessment_mode": {"type": "string"},
                "score_scale": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["value", "label"],
                        "properties": {
                            "value": {"type": "integer", "minimum": 0, "maximum": 4},
                            "label": {"type": "string"},
                        },
                    },
                },
                "core_total_rule": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["included_dimension_codes", "score_range", "severity_bands"],
                    "properties": {
                        "included_dimension_codes": {"type": "array", "items": {"type": "string"}},
                        "score_range": SCORE_RANGE_SCHEMA,
                        "severity_bands": {"type": "array", "items": SEVERITY_BAND_SCHEMA},
                    },
                },
                "supplemental_item_rule": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "dimension_code",
                        "included_in_core_total",
                        "score_range",
                        "professional_review_threshold",
                    ],
                    "properties": {
                        "dimension_code": {"type": "string"},
                        "included_in_core_total": {"type": "boolean"},
                        "score_range": SCORE_RANGE_SCHEMA,
                        "professional_review_threshold": {"type": "integer", "minimum": 2, "maximum": 2},
                    },
                },
            },
        },
        "assessment": {
            "type": "object",
            "additionalProperties": False,
            "required": ["core_items", "core_result", "supplemental_item", "summary"],
            "properties": {
                "core_items": {"type": "array", "minItems": 5, "maxItems": 5, "items": CORE_ITEM_SCHEMA},
                "core_result": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "calculation_status",
                        "answered_item_count",
                        "required_item_count",
                        "total_score",
                        "maximum_score",
                        "distress_level",
                    ],
                    "properties": {
                        "calculation_status": {"type": "string", "enum": ["complete", "incomplete"]},
                        "answered_item_count": {"type": "integer", "minimum": 0, "maximum": 5},
                        "required_item_count": {"type": "integer", "minimum": 5, "maximum": 5},
                        "total_score": {"type": ["integer", "null"], "minimum": 0, "maximum": 20},
                        "maximum_score": {"type": "integer", "minimum": 20, "maximum": 20},
                        "distress_level": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["code", "label", "min_score", "max_score"],
                            "properties": {
                                "code": {"type": ["string", "null"]},
                                "label": {"type": ["string", "null"]},
                                "min_score": {"type": ["integer", "null"]},
                                "max_score": {"type": ["integer", "null"]},
                            },
                        },
                    },
                },
                "supplemental_item": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "item_id",
                        "scale_mapping",
                        "value",
                        "evidence",
                        "rationale_summary",
                        "requires_direct_confirmation",
                        "clinician_confirmation",
                    ],
                    "properties": {
                        "item_id": {"type": "string"},
                        "scale_mapping": SUPPLEMENTAL_SCALE_MAPPING_SCHEMA,
                        "value": SUPPLEMENTAL_VALUE_SCHEMA,
                        "evidence": {"type": "array", "items": EVIDENCE_SCHEMA, "maxItems": 5},
                        "rationale_summary": {"type": "string"},
                        "requires_direct_confirmation": {"type": "boolean"},
                        "clinician_confirmation": SUPPLEMENTAL_CLINICIAN_CONFIRMATION_SCHEMA,
                    },
                },
                "summary": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "distress_summary",
                        "distress_level",
                        "safety_status",
                        "priority_dimension_codes",
                    ],
                    "properties": {
                        "distress_summary": {"type": "string"},
                        "distress_level": {"type": ["string", "null"]},
                        "safety_status": {
                            "type": "string",
                            "enum": ["no_alert", "needs_direct_confirmation", "needs_professional_review"],
                        },
                        "priority_dimension_codes": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        },
        "clinical_review": {
            "type": "object",
            "additionalProperties": False,
            "required": ["required", "status", "reviewed_by", "reviewed_at", "finalized", "message"],
            "properties": {
                "required": {"type": "boolean"},
                "status": {"type": "string", "enum": ["pending", "reviewed"]},
                "reviewed_by": NULLABLE_STRING,
                "reviewed_at": NULLABLE_STRING,
                "finalized": {"type": "boolean"},
                "message": {"type": "string"},
            },
        },
        "analysis_metadata": {
            "type": "object",
            "additionalProperties": False,
            "required": ["model_name", "model_version", "prompt_version", "generated_at"],
            "properties": {
                "model_name": {"type": "string"},
                "model_version": {"type": "string"},
                "prompt_version": {"type": "string"},
                "generated_at": {"type": "string"},
            },
        },
    },
}
