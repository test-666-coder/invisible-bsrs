"use client";

import { ChangeEvent, CSSProperties, useEffect, useMemo, useRef, useState } from "react";

type Evidence = {
  evidence_id: string;
  transcript_segment_id?: string;
  speaker?: "patient" | "doctor" | "clinician" | "unknown" | string;
  quote: string;
};

type AssessmentItem = {
  item_id: string;
  scale_mapping: {
    item_number: number;
    dimension_code: string;
    display_label: string;
    included_in_core_total?: boolean;
    is_supplemental_item?: boolean;
  };
  value: {
    estimated_score: number | null;
    score_label: string | null;
    derived_presence?: boolean | null;
    model_confidence: number | null;
    evidence_sufficiency: string;
    assessment_status: string;
  };
  evidence: Evidence[];
  rationale_summary: string;
  requires_direct_confirmation?: boolean;
  clinician_confirmation: {
    status: string;
    confirmed_score: number | null;
    derived_presence?: boolean | null;
    alert_threshold?: number;
    alert_triggered?: boolean | null;
    note?: string | null;
  };
};

type SeverityBand = {
  code: string;
  label: string;
  min_score: number;
  max_score: number;
};

type AssessmentDocument = {
  schema_version: string;
  session: {
    session_id: string;
    status: string;
    language: string;
    assessment_window: {
      type: string;
      days: number;
      display_label: string;
    };
  };
  instrument: {
    code: string;
    display_name: string;
    form_profile: string;
    assessment_mode: string;
    score_scale: { value: number; label: string }[];
    core_total_rule?: { severity_bands: SeverityBand[] };
  };
  assessment: {
    core_items: AssessmentItem[];
    core_result: {
      calculation_status: string;
      answered_item_count: number;
      required_item_count: number;
      total_score: number | null;
      maximum_score: number;
      distress_level: SeverityBand | null;
    };
    supplemental_item: AssessmentItem;
    summary: {
      distress_summary: string;
      distress_level: string;
      safety_status: string;
      priority_dimension_codes: string[];
    };
  };
  clinical_review: {
    required: boolean;
    status: string;
    finalized: boolean;
    message: string;
  };
  analysis_metadata?: {
    model_name?: string;
    model_version?: string;
    prompt_version?: string;
    generated_at?: string;
  };
};

type PipelineEnvelope = {
  status: string;
  session_id: string;
  result: AssessmentDocument;
  files?: Record<string, string>;
};

const DEFAULT_PIPELINE_API_URL = "http://127.0.0.1:8765";
const configuredApiUrl =
  typeof process !== "undefined" ? process.env.NEXT_PUBLIC_PIPELINE_API_URL : "";
const pipelineApiUrl = (configuredApiUrl || DEFAULT_PIPELINE_API_URL).replace(/\/+$/, "");

const demoData: AssessmentDocument = {
  schema_version: "1.1.0",
  session: {
    session_id: "demo-001",
    status: "completed",
    language: "zh-TW",
    assessment_window: { type: "past_7_days", days: 7, display_label: "最近一星期，包括今天" },
  },
  instrument: {
    code: "BSRS-5",
    display_name: "心情溫度計",
    form_profile: "taipei_online_order",
    assessment_mode: "ai_assisted_draft",
    score_scale: [
      { value: 0, label: "完全沒有" },
      { value: 1, label: "輕微" },
      { value: 2, label: "中等程度" },
      { value: 3, label: "厲害" },
      { value: 4, label: "非常厲害" },
    ],
  },
  assessment: {
    core_items: [
      item(
        "bsrs5-sleep",
        1,
        "sleep_disturbance",
        "睡眠困擾",
        3,
        "厲害",
        0.91,
        "最近幾乎每天都睡不好，半夜會一直醒。",
        "對話中明確出現持續性的睡眠中斷描述。",
      ),
      item(
        "bsrs5-anxiety",
        2,
        "anxiety",
        "緊張不安",
        3,
        "厲害",
        0.82,
        "最近一直覺得事情會出問題，腦袋停不下來。",
        "對話中出現持續擔憂與難以放鬆的描述。",
      ),
      item(
        "bsrs5-irritability",
        3,
        "irritability",
        "容易苦惱或動怒",
        2,
        "中等程度",
        0.76,
        "別人只是問我事情，我最近就很容易不耐煩。",
        "對話中出現近期耐受程度下降與容易不耐煩的描述。",
      ),
      item(
        "bsrs5-depressed-mood",
        4,
        "depressed_mood",
        "憂鬱或心情低落",
        2,
        "中等程度",
        0.73,
        "最近很多事情都提不起勁。",
        "對話中出現情緒低落與動力下降相關描述。",
      ),
      item(
        "bsrs5-inferiority",
        5,
        "inferiority",
        "覺得比不上別人",
        1,
        "輕微",
        0.68,
        "有時候會覺得自己是不是很沒用。",
        "對話中出現輕度自我價值降低的表述。",
      ),
    ],
    core_result: {
      calculation_status: "complete",
      answered_item_count: 5,
      required_item_count: 5,
      total_score: 11,
      maximum_score: 20,
      distress_level: { code: "moderate_distress", label: "中度情緒困擾", min_score: 10, max_score: 14 },
    },
    supplemental_item: {
      item_id: "bsrs-suicide-ideation",
      scale_mapping: {
        item_number: 6,
        dimension_code: "suicide_ideation",
        display_label: "自殺想法",
        is_supplemental_item: true,
        included_in_core_total: false,
      },
      value: {
        estimated_score: null,
        score_label: null,
        derived_presence: null,
        model_confidence: null,
        evidence_sufficiency: "insufficient",
        assessment_status: "needs_direct_confirmation",
      },
      evidence: [],
      rationale_summary: "目前對話未提供足夠資訊，不能將未提及視為完全沒有。",
      requires_direct_confirmation: true,
      clinician_confirmation: {
        status: "required",
        confirmed_score: null,
        derived_presence: null,
        alert_threshold: 2,
        alert_triggered: null,
      },
    },
    summary: {
      distress_summary:
        "五項核心指標總分為 11 分，屬於中度情緒困擾；睡眠困擾與緊張不安為目前較明顯的面向。",
      distress_level: "moderate_distress",
      safety_status: "needs_direct_confirmation",
      priority_dimension_codes: ["sleep_disturbance", "anxiety"],
    },
  },
  clinical_review: {
    required: true,
    status: "pending",
    finalized: false,
    message: "此結果為 AI 輔助評估草稿，需由醫療專業人員確認。",
  },
  analysis_metadata: { prompt_version: "bsrs-conversation-v1" },
};

function item(
  item_id: string,
  item_number: number,
  dimension_code: string,
  display_label: string,
  estimated_score: number,
  score_label: string,
  model_confidence: number,
  quote: string,
  rationale_summary: string,
): AssessmentItem {
  return {
    item_id,
    scale_mapping: { item_number, dimension_code, display_label, included_in_core_total: true },
    value: {
      estimated_score,
      score_label,
      model_confidence,
      evidence_sufficiency: "sufficient",
      assessment_status: "estimated",
    },
    evidence: [{ evidence_id: `ev-${item_number.toString().padStart(3, "0")}`, speaker: "patient", quote }],
    rationale_summary,
    clinician_confirmation: { status: "pending", confirmed_score: null },
  };
}

function ScoreDots({ score }: { score: number | null }) {
  return (
    <div className="score-dots" aria-label={score == null ? "資料不足" : `${score} 分`}>
      {[1, 2, 3, 4].map((value) => (
        <span key={value} className={score !== null && value <= score ? "filled" : ""} />
      ))}
    </div>
  );
}

function speakerName(speaker?: string) {
  if (speaker === "doctor" || speaker === "clinician") return "醫師";
  if (speaker === "patient") return "病患";
  return "對話證據";
}

function safetyLabel(item: AssessmentItem) {
  if (item.value.estimated_score === null) return "尚未確認";
  if (item.value.estimated_score >= 2) return "需優先專業評估";
  if (item.value.estimated_score > 0) return "出現相關訊號";
  return "AI 推估未出現";
}

function displayScoreLabel(score: number | null, fallback?: string | null) {
  if (score === 3) return "嚴重";
  if (score === 4) return "非常嚴重";
  return fallback ?? "";
}

function isAssessmentDocument(value: unknown): value is AssessmentDocument {
  const candidate = value as AssessmentDocument;
  return Boolean(
    candidate?.assessment?.core_items &&
      candidate.assessment.core_result &&
      candidate.assessment.supplemental_item,
  );
}

function unwrapAssessmentDocument(payload: unknown) {
  const envelope = payload as Partial<PipelineEnvelope>;
  const candidate = envelope.result ?? payload;
  if (!isAssessmentDocument(candidate)) {
    throw new Error("schema");
  }
  return {
    document: candidate,
    files: envelope.files ?? {},
  };
}

function buildSessionId(file: File) {
  const base = file.name.replace(/\.[^.]+$/, "").replace(/[^A-Za-z0-9_.-]+/g, "-").slice(0, 48);
  return `ui-${base || "audio"}`;
}

async function readErrorMessage(response: Response) {
  try {
    const payload = (await response.json()) as { detail?: string };
    return payload.detail || `分析服務回應 ${response.status}`;
  } catch {
    const text = await response.text();
    return text || `分析服務回應 ${response.status}`;
  }
}

export default function Home() {
  const [data, setData] = useState<AssessmentDocument>(demoData);
  const [fileName, setFileName] = useState("範例 JSON");
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [audioFileName, setAudioFileName] = useState("尚未選擇音檔");
  const [isAnalyzingAudio, setIsAnalyzingAudio] = useState(false);
  const [resultArtifacts, setResultArtifacts] = useState<Record<string, string>>({});
  const [selectedCode, setSelectedCode] = useState(
    demoData.assessment.core_items[0].scale_mapping.dimension_code,
  );
  const [draftScores, setDraftScores] = useState<Record<string, number>>({});
  const [confirmed, setConfirmed] = useState<Record<string, number>>({});
  const [ringProgress, setRingProgress] = useState(0);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const audioInput = useRef<HTMLInputElement>(null);

  const items = data.assessment.core_items;
  const selected = useMemo(
    () => items.find((assessmentItem) => assessmentItem.scale_mapping.dimension_code === selectedCode) ?? items[0],
    [items, selectedCode],
  );
  const result = data.assessment.core_result;
  const safety = data.assessment.supplemental_item;
  const totalScore = items.reduce(
    (sum, assessmentItem) =>
      sum +
      (confirmed[assessmentItem.scale_mapping.dimension_code] ??
        assessmentItem.clinician_confirmation.confirmed_score ??
        assessmentItem.value.estimated_score ??
        0),
    0,
  );
  const severityBands = data.instrument.core_total_rule?.severity_bands ?? [
    { code: "good_adaptation", label: "身心適應狀況良好", min_score: 0, max_score: 5 },
    { code: "mild_distress", label: "輕度情緒困擾", min_score: 6, max_score: 9 },
    { code: "moderate_distress", label: "中度情緒困擾", min_score: 10, max_score: 14 },
    { code: "severe_distress", label: "重度情緒困擾", min_score: 15, max_score: 20 },
  ];
  const displayedDistress =
    severityBands.find((band) => totalScore >= band.min_score && totalScore <= band.max_score) ??
    result.distress_level;
  const scoreWasRecalculated = Object.keys(confirmed).length > 0;
  const artifactCount = Object.keys(resultArtifacts).length;
  const audioStatus = isAnalyzingAudio ? "模型分析中" : artifactCount > 0 ? "結果完成" : "等待上傳";

  useEffect(() => {
    let resetFrame = 0;
    let secondFrame = 0;
    const firstFrame = requestAnimationFrame(() => {
      setRingProgress(0);
      resetFrame = requestAnimationFrame(() => {
        secondFrame = requestAnimationFrame(() =>
          setRingProgress(Math.max(0, Math.min(1, totalScore / result.maximum_score)) * 360),
        );
      });
    });
    return () => {
      cancelAnimationFrame(firstFrame);
      cancelAnimationFrame(resetFrame);
      cancelAnimationFrame(secondFrame);
    };
  }, [totalScore, result.maximum_score]);

  useEffect(() => {
    let cancelled = false;
    fetch(`${pipelineApiUrl}/api/latest-result`)
      .then((response) => {
        if (!response.ok) throw new Error("no latest result");
        return response.json();
      })
      .then((payload) => {
        if (cancelled) return;
        const { document, files } = unwrapAssessmentDocument(payload);
        setData(document);
        setFileName("最新分析結果");
        setResultArtifacts(files);
        setSelectedCode(document.assessment.core_items[0]?.scale_mapping.dimension_code ?? "");
        setDraftScores({});
        setConfirmed({});
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  function flash(text: string) {
    setNotice(text);
    window.setTimeout(() => setNotice(""), 2200);
  }

  function resetReviewState(nextData: AssessmentDocument) {
    setSelectedCode(nextData.assessment.core_items[0]?.scale_mapping.dimension_code ?? "");
    setDraftScores({});
    setConfirmed({});
  }

  function confirmScore(code: string, score: number) {
    setConfirmed((current) => ({ ...current, [code]: score }));
    setDraftScores((current) => ({ ...current, [code]: score }));
    flash("分數已確認，BSRS-5 總分已重新計算");
  }

  function chooseAudio(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    setAudioFile(file);
    setAudioFileName(file?.name ?? "尚未選擇音檔");
    setError("");
    event.target.value = "";
    if (file) {
      void analyzeSelectedAudio(file);
    }
  }

  async function analyzeSelectedAudio(file: File) {
    setIsAnalyzingAudio(true);
    setError("");
    setNotice("");
    try {
      const body = new FormData();
      body.append("audio", file);
      body.append("session_id", buildSessionId(file));
      body.append("language", data.session.language || "zh-TW");

      const response = await fetch(`${pipelineApiUrl}/api/analyze-audio`, {
        method: "POST",
        body,
      });
      if (!response.ok) {
        throw new Error(await readErrorMessage(response));
      }

      const payload = await response.json();
      const { document, files } = unwrapAssessmentDocument(payload);
      setData(document);
      setFileName(file.name);
      setResultArtifacts(files);
      resetReviewState(document);
      flash("音檔分析完成，量表已更新");
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "音檔分析失敗。";
      setError(`${message} 請確認本機模型服務已啟動。`);
    } finally {
      setIsAnalyzingAudio(false);
    }
  }

  return (
    <main>
      {notice && (
        <div className="toast" role="status">
          ✓ {notice}
        </div>
      )}
      <header className="topbar">
        <div className="brand-mark">澄</div>
        <div className="brand-copy">
          <strong>澄心</strong>
          <span>AI 情緒聽診器</span>
        </div>
        <div className="header-divider" />
        <div className="session-title">
          <span>個案評估</span>
          <strong>#{data.session.session_id}</strong>
        </div>
        <div className="top-actions">
          <span className="status-badge">
            <i /> {data.session.status === "completed" ? "分析完成" : data.session.status}
          </span>
          <span className="file-name" title={audioFile ? audioFileName : fileName}>
            {audioFile ? audioFileName : fileName}
          </span>
          <input
            ref={audioInput}
            className="file-input"
            type="file"
            accept="audio/*,.wav,.mp3,.m4a,.flac,.ogg,.webm"
            onChange={chooseAudio}
          />
          <button className="load-button analyze-audio-button" disabled={isAnalyzingAudio} onClick={() => audioInput.current?.click()}>
            {isAnalyzingAudio ? "分析中" : "上傳音檔"}
          </button>
          <button className="avatar">林</button>
        </div>
      </header>

      {error && (
        <div className="error-banner" role="alert">
          {error}
          <button onClick={() => setError("")}>×</button>
        </div>
      )}

      <section className="context-bar">
        <div>
          <span className="eyebrow">評估期間</span>
          <strong>{data.session.assessment_window.display_label}</strong>
        </div>
        <div>
          <span className="eyebrow">量表</span>
          <strong>
            {data.instrument.code} {data.instrument.display_name}
          </strong>
        </div>
        <div>
          <span className="eyebrow">聲音分析</span>
          <strong>{audioStatus}</strong>
        </div>
        <div className="disclaimer">
          <span>AI</span>
          <p>
            <strong>AI 輔助評估草稿</strong>
            <small>{data.clinical_review.message}</small>
          </p>
        </div>
      </section>

      {artifactCount > 0 && (
        <section className="artifact-banner">
          <span>檔案已保留</span>
          <strong>{resultArtifacts.result_json ?? resultArtifacts.bsrs_json ?? "outputs/ui_runs"}</strong>
          <small>逐字稿、去識別化、語音情緒與量表結果已同步輸出。</small>
        </section>
      )}

      <section className={`upload-strip ${isAnalyzingAudio ? "busy" : artifactCount > 0 ? "done" : ""}`}>
        <div>
          <span className="eyebrow">音檔</span>
          <strong>{isAnalyzingAudio ? "分析中" : artifactCount > 0 ? "量表已產生" : "待上傳"}</strong>
        </div>
        <button className="load-button upload-strip-button" disabled={isAnalyzingAudio} onClick={() => audioInput.current?.click()}>
          {isAnalyzingAudio ? "分析中" : "上傳音檔"}
        </button>
        <small>{audioFile ? audioFileName : fileName}</small>
      </section>

      <div className="workspace">
        <section className="results-column">
          <article className={`panel score-card severity-${displayedDistress?.code ?? "unknown"}`}>
            <div className="panel-heading">
              <div>
                <h2>{data.instrument.code} 核心評估</h2>
              </div>
              <span className="review-state">
                {data.clinical_review.status === "pending" ? "待醫師確認" : data.clinical_review.status}
              </span>
            </div>
            <div className="overall-row">
              <div className="score-ring" style={{ "--score-progress": `${ringProgress}deg` } as CSSProperties}>
                <strong>{totalScore}</strong>
                <span>/ {result.maximum_score}</span>
              </div>
              <div>
                <span className="level-label">{displayedDistress?.label ?? "資料不足"}</span>
                <p>
                  {scoreWasRecalculated
                    ? `醫師確認後的五項核心指標總分為 ${totalScore} 分，屬於${displayedDistress?.label ?? "待評估"}。`
                    : data.assessment.summary.distress_summary}
                </p>
              </div>
            </div>
            <div className="scale-list">
              {items.map((assessmentItem) => {
                const code = assessmentItem.scale_mapping.dimension_code;
                const shown =
                  confirmed[code] ??
                  assessmentItem.clinician_confirmation.confirmed_score ??
                  assessmentItem.value.estimated_score;
                return (
                  <button
                    key={assessmentItem.item_id}
                    className={`scale-row ${code === selectedCode ? "active" : ""}`}
                    onClick={() => setSelectedCode(code)}
                  >
                    <span className="scale-label">
                      {assessmentItem.scale_mapping.display_label}
                      {confirmed[code] !== undefined && <small>✓ 已確認</small>}
                    </span>
                    <ScoreDots score={shown} />
                    <strong>
                      {shown ?? "—"} <small>/ 4</small>
                    </strong>
                    <span className="chevron">›</span>
                  </button>
                );
              })}
            </div>
          </article>

          {selected && (
            <article className="panel evidence-card">
              <div className="evidence-header">
                <h2>判斷依據</h2>
                <span className="confidence">
                  AI 信心 {selected.value.model_confidence == null ? "—" : `${Math.round(selected.value.model_confidence * 100)}%`}
                </span>
              </div>
              {selected.evidence.length ? (
                selected.evidence.map((evidence) => (
                  <blockquote key={evidence.evidence_id}>
                    「{evidence.quote}」
                    <small>
                      {speakerName(evidence.speaker)} · {evidence.transcript_segment_id ?? evidence.evidence_id}
                    </small>
                  </blockquote>
                ))
              ) : (
                <blockquote className="empty-evidence">目前沒有可引用的對話證據</blockquote>
              )}
              <p className="reason">{selected.rationale_summary}</p>
              <div className="review-row">
                <div className="ai-estimate-copy">
                  <span>
                    AI 推估：
                    <strong>
                      {selected.value.estimated_score ?? "資料不足"}
                      {selected.value.estimated_score !== null &&
                        ` 分 · ${displayScoreLabel(
                          selected.value.estimated_score,
                          selected.value.score_label ??
                            data.instrument.score_scale.find((score) => score.value === selected.value.estimated_score)?.label,
                        )}`}
                    </strong>
                  </span>
                  <span>醫師可點擊底下數字重新評分</span>
                </div>
                <div className="score-picker" aria-label="醫師重新評分">
                  {data.instrument.score_scale.map((score) => {
                    const code = selected.scale_mapping.dimension_code;
                    const activeScore =
                      draftScores[code] ??
                      confirmed[code] ??
                      selected.clinician_confirmation.confirmed_score ??
                      selected.value.estimated_score;
                    return (
                      <button
                        key={score.value}
                        title={displayScoreLabel(score.value, score.label)}
                        className={activeScore === score.value ? "selected" : ""}
                        onClick={() => setDraftScores((current) => ({ ...current, [code]: score.value }))}
                      >
                        {score.value}
                      </button>
                    );
                  })}
                </div>
                <button
                  className="confirm-button"
                  onClick={() => {
                    const code = selected.scale_mapping.dimension_code;
                    confirmScore(
                      code,
                      draftScores[code] ??
                        confirmed[code] ??
                        selected.clinician_confirmation.confirmed_score ??
                        selected.value.estimated_score ??
                        0,
                    );
                  }}
                >
                  點此確認分數
                </button>
              </div>
            </article>
          )}

          <article className={`panel safety-card ${safety.value.estimated_score !== null && safety.value.estimated_score >= 2 ? "urgent" : ""}`}>
            <div className="safety-icon">!</div>
            <div className="safety-copy">
              <h2>
                {safety.scale_mapping.display_label}：{safetyLabel(safety)}
              </h2>
              <p>{safety.rationale_summary}</p>
              {safety.evidence.length > 0 && <p className="safety-evidence">「{safety.evidence[0].quote}」</p>}
            </div>
            <button className="safety-button" onClick={() => flash("已標記為需要直接安全確認")}>
              {safety.requires_direct_confirmation ? "開始安全確認" : "查看安全證據"}
            </button>
          </article>
        </section>
      </div>
    </main>
  );
}
