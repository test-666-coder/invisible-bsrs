import json
import unittest

from patient_mood_pipeline.deidentify import redact_text
from patient_mood_pipeline.openai_bsrs import build_bsrs_prompt, normalize_bsrs_report
from patient_mood_pipeline.schemas import BSRS_REPORT_SCHEMA, SCHEMA_VERSION


class PipelineUnitTests(unittest.TestCase):
    def test_regex_deidentification_removes_common_phi(self):
        text = "姓名：王小明\n電話：0912-345-678\n身分證：A123456789\n地址：台北市中正區仁愛路1號"
        result = redact_text(text)
        self.assertNotIn("王小明", result.text)
        self.assertNotIn("0912", result.text)
        self.assertNotIn("A123456789", result.text)
        self.assertIn("[FIELD_VALUE]", result.text)

    def test_prompt_uses_deidentified_transcript(self):
        messages = build_bsrs_prompt("[NAME] 最近睡不好，也很焦慮。", {"dominant_label": "sad"})
        text = json.dumps(messages, ensure_ascii=False)
        self.assertIn("[NAME]", text)
        self.assertIn("BSRS-5", text)
        self.assertIn("sleep_disturbance", text)
        self.assertIn("suicide_ideation", text)
        self.assertNotIn("王小明", text)

    def test_schema_is_strict_object(self):
        self.assertEqual(BSRS_REPORT_SCHEMA["type"], "object")
        self.assertFalse(BSRS_REPORT_SCHEMA["additionalProperties"])
        self.assertIn("session", BSRS_REPORT_SCHEMA["required"])
        self.assertIn("instrument", BSRS_REPORT_SCHEMA["required"])
        self.assertIn("assessment", BSRS_REPORT_SCHEMA["required"])

    def test_normalize_report_recalculates_core_total(self):
        report = _minimal_report()
        normalized = normalize_bsrs_report(
            report,
            session_id="demo-001",
            language="zh-TW",
            model="gpt-test",
            generated_at="2026-08-15T00:00:00+00:00",
        )

        self.assertEqual(normalized["schema_version"], SCHEMA_VERSION)
        self.assertEqual(normalized["assessment"]["core_result"]["total_score"], 11)
        self.assertEqual(normalized["assessment"]["core_result"]["distress_level"]["code"], "moderate_distress")
        self.assertEqual(normalized["assessment"]["core_items"][0]["value"]["score_label"], "厲害")
        self.assertFalse(normalized["assessment"]["supplemental_item"]["scale_mapping"]["included_in_core_total"])
        self.assertIsNone(normalized["assessment"]["supplemental_item"]["value"]["derived_presence"])


def _core_item(score):
    return {
        "item_id": "placeholder",
        "scale_mapping": {
            "item_number": 1,
            "dimension_code": "placeholder",
            "display_label": "placeholder",
            "included_in_core_total": True,
        },
        "value": {
            "estimated_score": score,
            "score_label": None,
            "model_confidence": 0.8,
            "evidence_sufficiency": "sufficient",
            "assessment_status": "estimated",
        },
        "evidence": [],
        "rationale_summary": "test",
        "clinician_confirmation": {"status": "pending", "confirmed_score": None, "note": None},
    }


def _minimal_report():
    return {
        "schema_version": "draft",
        "session": {},
        "instrument": {},
        "assessment": {
            "core_items": [_core_item(score) for score in [3, 3, 2, 2, 1]],
            "core_result": {
                "calculation_status": "incomplete",
                "answered_item_count": 0,
                "required_item_count": 5,
                "total_score": None,
                "maximum_score": 20,
                "distress_level": {"code": None, "label": None, "min_score": None, "max_score": None},
            },
            "supplemental_item": {
                "item_id": "placeholder",
                "scale_mapping": {
                    "item_number": 6,
                    "dimension_code": "suicide_ideation",
                    "display_label": "自殺想法",
                    "is_supplemental_item": True,
                    "included_in_core_total": False,
                },
                "value": {
                    "estimated_score": None,
                    "score_label": None,
                    "derived_presence": None,
                    "model_confidence": None,
                    "evidence_sufficiency": "insufficient",
                    "assessment_status": "needs_direct_confirmation",
                },
                "evidence": [],
                "rationale_summary": "目前對話未提供足夠資訊。",
                "requires_direct_confirmation": True,
                "clinician_confirmation": {
                    "status": "required",
                    "confirmed_score": None,
                    "derived_presence": None,
                    "alert_threshold": 2,
                    "alert_triggered": None,
                },
            },
            "summary": {
                "distress_summary": "test",
                "distress_level": None,
                "safety_status": "needs_direct_confirmation",
                "priority_dimension_codes": [],
            },
        },
        "clinical_review": {
            "required": True,
            "status": "pending",
            "reviewed_by": None,
            "reviewed_at": None,
            "finalized": False,
            "message": "此結果為 AI 輔助評估草稿，需由醫療專業人員確認。",
        },
        "analysis_metadata": {},
    }


if __name__ == "__main__":
    unittest.main()
