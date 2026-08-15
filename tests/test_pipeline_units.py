import json
import unittest

from patient_mood_pipeline.deidentify import redact_text
from patient_mood_pipeline.local_models import summarize_emotion_scores
from patient_mood_pipeline.openai_bsrs import build_bsrs_prompt, normalize_bsrs_report
from patient_mood_pipeline.openai_transcript import build_transcript_correction_prompt
from patient_mood_pipeline.schemas import BSRS_REPORT_SCHEMA, SCHEMA_VERSION


class PipelineUnitTests(unittest.TestCase):
    def test_regex_deidentification_removes_common_phi(self):
        text = "姓名：王小明\n電話：0912-345-678\n身分證：A123456789\n地址：台北市中正區仁愛路1號"
        result = redact_text(text)
        self.assertNotIn("王小明", result.text)
        self.assertNotIn("0912", result.text)
        self.assertNotIn("A123456789", result.text)
        self.assertIn("[FIELD_VALUE]", result.text)

    def test_regex_deidentification_removes_spoken_mobile_number(self):
        text = "我叫王小明，手機是零九一二三四五六七八最近幾乎每天都睡不好。"
        result = redact_text(text)
        self.assertNotIn("王小明", result.text)
        self.assertNotIn("零九一二三四五六七八", result.text)
        self.assertIn("最近幾乎每天都睡不好", result.text)

    def test_deidentification_does_not_remove_self_criticism_as_name(self):
        text = "患者說，我是很糟，覺得自己很沒用。"
        result = redact_text(text)
        self.assertIn("我是很糟", result.text)
        self.assertIn("覺得自己很沒用", result.text)

    def test_deidentification_keeps_generic_clinical_time_terms(self):
        text = "最近每天睡不好，半夜會醒來，這幾天心情低落。"
        ner_entities = [
            {"entity_group": "DATE", "start": 0, "end": 2},
            {"entity_group": "TIME", "start": 8, "end": 10},
            {"entity_group": "DATE", "start": 14, "end": 17},
        ]
        result = redact_text(text, ner_entities)
        self.assertIn("最近每天睡不好", result.text)
        self.assertIn("半夜會醒來", result.text)
        self.assertIn("這幾天心情低落", result.text)

    def test_prompt_uses_deidentified_transcript(self):
        messages = build_bsrs_prompt("[NAME] 最近睡不好，也很焦慮。", {"dominant_label": "sad"})
        text = json.dumps(messages, ensure_ascii=False)
        self.assertIn("[NAME]", text)
        self.assertIn("BSRS-5", text)
        self.assertIn("sleep_disturbance", text)
        self.assertIn("suicide_ideation", text)
        self.assertIn("間接證據", text)
        self.assertIn("患者常會淡化", text)
        self.assertNotIn("王小明", text)

    def test_prompt_keeps_manageable_stress_low_and_scores_direct_safety_denial(self):
        messages = build_bsrs_prompt("患者偶爾急一下但能察覺並修正。醫師問有沒有不想活，患者說完全沒有。", None)
        text = json.dumps(messages, ensure_ascii=False)
        self.assertIn("繁體中文", text)
        self.assertIn("低嚴重度與保護因子", text)
        self.assertIn("0 或 1", text)
        self.assertIn("偶爾急一下但能察覺並修正", text)
        self.assertIn("estimated_score 應為 0", text)
        self.assertIn("requires_direct_confirmation=false", text)

    def test_transcript_correction_prompt_preserves_deidentified_placeholders(self):
        messages = build_transcript_correction_prompt("[NAME] 手機是[MOBILE]，最近睡不好。")
        text = json.dumps(messages, ensure_ascii=False)
        self.assertIn("[NAME]", text)
        self.assertIn("[MOBILE]", text)
        self.assertIn("placeholders_to_preserve", text)
        self.assertNotIn("王小明", text)

    def test_transcript_correction_prompt_mentions_taiwan_mandarin(self):
        messages = build_transcript_correction_prompt("伊斯問：最近南睡嗎？換著說胸口僅僅，待伴很多。")
        text = json.dumps(messages, ensure_ascii=False)
        self.assertIn("台灣華語", text)
        self.assertIn("醫師", text)
        self.assertIn("患者", text)
        self.assertIn("食慾", text)
        self.assertIn("胸口緊緊", text)
        self.assertIn("難睡", text)
        self.assertIn("待辦", text)

    def test_voice_emotion_summary_adds_finer_profile(self):
        profile = summarize_emotion_scores(
            [
                {"label": "angry", "score": 0.7},
                {"label": "fearful", "score": 0.2},
                {"label": "sad", "score": 0.1},
            ]
        )
        self.assertEqual(profile["dominant_emotion"]["zh_label"], "煩躁/生氣")
        self.assertEqual(profile["dimensional_scores"]["valence_label"], "負向")
        self.assertEqual(profile["dimensional_scores"]["arousal_label"], "高")
        self.assertGreater(profile["dimensional_scores"]["agitation_score"], 0.8)

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

    def test_normalize_report_marks_direct_safety_denial_as_estimated(self):
        report = _minimal_report()
        supplemental = report["assessment"]["supplemental_item"]
        supplemental["value"]["estimated_score"] = 0
        supplemental["value"]["evidence_sufficiency"] = "sufficient"
        supplemental["evidence"] = [
            {
                "evidence_id": "ev-safety",
                "transcript_segment_id": "seg-safety",
                "speaker": "patient",
                "quote": "沒有，這個完全沒有。",
            }
        ]

        normalized = normalize_bsrs_report(
            report,
            session_id="demo-001",
            language="zh-TW",
            model="gpt-test",
            generated_at="2026-08-15T00:00:00+00:00",
        )

        value = normalized["assessment"]["supplemental_item"]["value"]
        self.assertEqual(value["estimated_score"], 0)
        self.assertEqual(value["score_label"], "完全沒有")
        self.assertFalse(value["derived_presence"])
        self.assertEqual(value["assessment_status"], "estimated")
        self.assertFalse(normalized["assessment"]["supplemental_item"]["requires_direct_confirmation"])
        self.assertEqual(normalized["assessment"]["summary"]["distress_level"], "moderate_distress")
        self.assertEqual(normalized["assessment"]["summary"]["safety_status"], "no_alert")

    def test_normalize_report_recovers_direct_safety_denial_from_transcript(self):
        report = _minimal_report()

        normalized = normalize_bsrs_report(
            report,
            session_id="demo-001",
            language="zh-TW",
            model="gpt-test",
            generated_at="2026-08-15T00:00:00+00:00",
            deidentified_transcript="醫師問最近有沒有不想活或想傷害自己。患者回答沒有，這個完全沒有。",
        )

        supplemental = normalized["assessment"]["supplemental_item"]
        self.assertEqual(supplemental["value"]["estimated_score"], 0)
        self.assertEqual(supplemental["value"]["assessment_status"], "estimated")
        self.assertFalse(supplemental["requires_direct_confirmation"])
        self.assertTrue(supplemental["evidence"])


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
