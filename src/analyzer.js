(function attachAnalyzer(root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
  root.MoodThermometer = api;
})(typeof globalThis !== "undefined" ? globalThis : window, function buildAnalyzer() {
  const BSRS_ITEMS = [
    {
      id: "sleep",
      label: "睡眠困難",
      prompt: "睡眠困難，譬如難以入睡、易醒或早醒",
      aliases: ["睡眠", "睡不好", "失眠", "難以入睡", "易醒", "早醒", "半夜醒", "睡不著"],
      terms: ["睡不好", "失眠", "難以入睡", "睡不著", "易醒", "早醒", "半夜醒", "淺眠", "惡夢", "睡眠困難"],
    },
    {
      id: "anxiety",
      label: "緊張不安",
      prompt: "感覺緊張不安",
      aliases: ["緊張", "不安", "焦慮", "擔心", "心慌", "恐慌"],
      terms: ["緊張", "不安", "焦慮", "擔心", "心慌", "恐慌", "坐立難安", "喘不過氣", "害怕", "壓力很大"],
    },
    {
      id: "irritability",
      label: "苦惱或動怒",
      prompt: "覺得容易苦惱或動怒",
      aliases: ["苦惱", "動怒", "易怒", "生氣", "煩躁"],
      terms: ["苦惱", "動怒", "易怒", "生氣", "煩躁", "暴躁", "火大", "不耐煩", "想罵人", "失控"],
    },
    {
      id: "depression",
      label: "憂鬱低落",
      prompt: "感覺憂鬱、心情低落",
      aliases: ["憂鬱", "低落", "難過", "沒希望", "提不起勁"],
      terms: ["憂鬱", "低落", "難過", "沒希望", "絕望", "提不起勁", "哭", "想哭", "空掉", "沒有力氣", "沒有興趣"],
    },
    {
      id: "inferiority",
      label: "比不上別人",
      prompt: "覺得比不上別人",
      aliases: ["比不上", "沒用", "自責", "拖累", "負擔", "失敗"],
      terms: ["比不上", "沒用", "自責", "拖累", "負擔", "失敗", "沒價值", "不好", "沒有用", "丟臉"],
    },
  ];

  const SUICIDE_ITEM = {
    id: "suicide",
    label: "自殺意念",
    prompt: "有自殺的想法",
    aliases: ["自殺", "輕生", "不想活", "死掉", "傷害自己", "結束生命"],
    terms: ["自殺", "輕生", "不想活", "不想醒來", "死掉", "想死", "傷害自己", "結束生命", "活不下去", "消失"],
  };

  const INTENSITY = {
    severe: {
      scoreHint: 4,
      weight: 3,
      words: ["非常嚴重", "撐不下去", "受不了", "完全", "幾乎每天", "每天", "整天", "整晚", "一直", "沒有辦法", "快崩潰"],
    },
    moderate: {
      scoreHint: 3,
      weight: 2,
      words: ["嚴重", "常常", "好幾天", "反覆", "明顯", "影響工作", "影響生活", "中等", "蠻"],
    },
    mild: {
      scoreHint: 1,
      weight: 0.7,
      words: ["輕微", "有點", "一點", "偶爾", "稍微", "還好", "一陣子"],
    },
  };

  const LEVEL_WORDS = [
    { score: 0, terms: ["完全沒有", "不會", "沒有困擾", "沒有"] },
    { score: 1, terms: ["輕微", "有點", "一點"] },
    { score: 2, terms: ["中等", "中度", "還算困擾"] },
    { score: 3, terms: ["嚴重", "厲害"] },
    { score: 4, terms: ["非常嚴重", "非常厲害", "受不了"] },
  ];

  const NEGATORS = ["沒有", "沒", "無", "否認", "未曾", "並未", "不會", "沒有想", "沒有要"];
  const PLAN_TERMS = ["計畫", "方法", "準備", "遺書", "藥", "刀", "跳樓", "割腕", "上吊", "燒炭"];

  function normalizeText(text) {
    return String(text || "")
      .replace(/\r\n/g, "\n")
      .replace(/\u3000/g, " ")
      .trim();
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function splitSentences(text) {
    return normalizeText(text)
      .split(/[\n。！？!?；;]+/)
      .map((sentence) => sentence.trim())
      .filter(Boolean);
  }

  function nearbyText(sentence, index, radius) {
    const start = Math.max(0, index - radius);
    const end = Math.min(sentence.length, index + radius);
    return sentence.slice(start, end);
  }

  function hasAny(text, terms) {
    return terms.some((term) => text.includes(term));
  }

  function isNegated(sentence, index, term) {
    const before = sentence.slice(Math.max(0, index - 10), index);
    const after = sentence.slice(index + term.length, Math.min(sentence.length, index + term.length + 8));
    if (NEGATORS.some((negator) => before.includes(negator))) return true;
    if (/沒有.{0,8}(困擾|問題|念頭|想法)/.test(before + term + after)) return true;
    return false;
  }

  function intensityForContext(context) {
    if (hasAny(context, INTENSITY.severe.words)) return INTENSITY.severe;
    if (hasAny(context, INTENSITY.moderate.words)) return INTENSITY.moderate;
    if (hasAny(context, INTENSITY.mild.words)) return INTENSITY.mild;
    return { scoreHint: 2, weight: 1.2 };
  }

  function extractExplicitScore(text, item) {
    const aliases = item.aliases.map(escapeRegExp).join("|");
    const patterns = [
      new RegExp(`(?:${aliases})[^\\n。！？]{0,24}([0-4])\\s*分`, "g"),
      new RegExp(`([0-4])\\s*分[^\\n。！？]{0,24}(?:${aliases})`, "g"),
    ];

    for (const pattern of patterns) {
      const match = pattern.exec(text);
      if (match) return Number(match[1]);
    }

    const sentences = splitSentences(text);
    for (const sentence of sentences) {
      if (!hasAny(sentence, item.aliases)) continue;
      for (const level of LEVEL_WORDS) {
        if (hasAny(sentence, level.terms)) {
          if (level.score === 0 && item.id === "suicide" && /不想活|想死|自殺/.test(sentence) && !/沒有|否認|無/.test(sentence)) {
            continue;
          }
          return level.score;
        }
      }
    }

    return null;
  }

  function scoreFromWeight(weight, highestHint, itemId) {
    if (weight <= 0) return 0;
    if (itemId === "suicide") {
      if (highestHint >= 4 || weight >= 5) return 4;
      if (weight >= 3) return 3;
      if (weight >= 1.2) return 2;
      return 1;
    }
    if (highestHint >= 4 && weight >= 3) return 4;
    if (weight < 1.3) return 1;
    if (weight < 3.6) return 2;
    if (weight < 6.2) return 3;
    return 4;
  }

  function scoreItem(text, item) {
    const cleanText = normalizeText(text);
    const explicit = extractExplicitScore(cleanText, item);
    const sentences = splitSentences(cleanText);
    const evidence = [];
    let weight = 0;
    let highestHint = 0;
    let negatedHits = 0;
    const matchedTerms = new Set();

    for (const sentence of sentences) {
      let sentenceMatched = false;
      for (const term of item.terms) {
        let index = sentence.indexOf(term);
        while (index !== -1) {
          if (isNegated(sentence, index, term)) {
            negatedHits += 1;
          } else {
            const context = nearbyText(sentence, index, 18);
            const intensity = intensityForContext(context);
            weight += intensity.weight;
            highestHint = Math.max(highestHint, intensity.scoreHint);
            matchedTerms.add(term);
            sentenceMatched = true;
          }
          index = sentence.indexOf(term, index + term.length);
        }
      }

      if (item.id === "suicide" && sentenceMatched && hasAny(sentence, PLAN_TERMS)) {
        weight += 2.8;
        highestHint = 4;
      }

      if (sentenceMatched && evidence.length < 3) {
        evidence.push(sentence);
      }
    }

    const score = explicit !== null ? explicit : scoreFromWeight(weight, highestHint, item.id);
    const rawConfidence = explicit !== null ? 0.92 : Math.min(0.88, 0.3 + weight / 8 + matchedTerms.size * 0.08);
    const confidence = score === 0 && negatedHits > 0 ? 0.76 : rawConfidence;

    return {
      id: item.id,
      label: item.label,
      prompt: item.prompt,
      score,
      confidence: Number(confidence.toFixed(2)),
      evidence,
      matchedTerms: Array.from(matchedTerms),
      negatedHits,
      source: explicit !== null ? "explicit" : "heuristic",
    };
  }

  function getRiskLevel(total, suicideScore) {
    if (suicideScore >= 2) {
      return {
        key: "suicide",
        label: "需即時評估",
        className: "is-critical",
        message: "自殺意念達中等以上，建議立即進行自傷風險評估與安全計畫。",
      };
    }
    if (total >= 15) {
      return {
        key: "severe",
        label: "重度困擾",
        className: "is-critical",
        message: "總分達重度情緒困擾區間，建議高關懷並安排專業評估。",
      };
    }
    if (total >= 10) {
      return {
        key: "moderate",
        label: "中度困擾",
        className: "is-warning",
        message: "總分落在中度情緒困擾區間，建議進一步心理諮商或專業諮詢。",
      };
    }
    if (total >= 6) {
      return {
        key: "mild",
        label: "輕度困擾",
        className: "is-warning",
        message: "總分落在輕度情緒困擾區間，可評估社會支持與壓力調適資源。",
      };
    }
    return {
      key: "stable",
      label: "適應良好",
      className: "",
      message: "總分落在身心適應狀況良好區間，仍建議結合臨床會談脈絡判讀。",
    };
  }

  function analyzeBSRS(text) {
    const items = BSRS_ITEMS.map((item) => scoreItem(text, item));
    const suicide = scoreItem(text, SUICIDE_ITEM);
    const total = items.reduce((sum, item) => sum + item.score, 0);
    const risk = getRiskLevel(total, suicide.score);
    return { items, suicide, total, risk };
  }

  function getDominantMood(bsrs) {
    const ranking = [
      { label: "自傷風險", value: bsrs.suicide.score * 5 },
      { label: "低落自責", value: bsrs.items.find((item) => item.id === "depression").score + bsrs.items.find((item) => item.id === "inferiority").score },
      { label: "焦慮緊繃", value: bsrs.items.find((item) => item.id === "anxiety").score + bsrs.items.find((item) => item.id === "sleep").score * 0.5 },
      { label: "煩躁易怒", value: bsrs.items.find((item) => item.id === "irritability").score },
    ].sort((a, b) => b.value - a.value);

    if (ranking[0].value <= 1) return "平穩";
    return ranking[0].label;
  }

  function analyzeMood(text, bsrs, voiceMetrics) {
    const metrics = voiceMetrics || {};
    const dominantMood = getDominantMood(bsrs);
    const arousalBase = bsrs.items.find((item) => item.id === "anxiety").score + bsrs.items.find((item) => item.id === "irritability").score;
    const voiceEnergy = metrics.peakRms ? Math.min(4, metrics.peakRms * 22) : 0;
    const arousalScore = Math.min(10, arousalBase * 1.4 + voiceEnergy);
    const valenceScore = Math.max(0, Math.round(100 - bsrs.total * 4.2 - bsrs.suicide.score * 12));
    const arousalLevel = arousalScore >= 7 ? "高" : arousalScore >= 3.5 ? "中" : "低";
    const energyLabel = metrics.samples
      ? metrics.variance > 0.035
        ? "起伏大"
        : metrics.avgRms > 0.08
          ? "偏高"
          : "平穩"
      : "無語音資料";
    const paceLabel = metrics.durationSeconds
      ? metrics.charsPerMinute > 210
        ? "偏快"
        : metrics.charsPerMinute < 70
          ? "偏慢"
          : "適中"
      : "無語音資料";

    return {
      dominantMood,
      arousalLevel,
      arousalScore: Number(arousalScore.toFixed(1)),
      valenceScore,
      voice: {
        energyLabel,
        paceLabel,
        avgRms: metrics.avgRms || 0,
        peakRms: metrics.peakRms || 0,
        charsPerMinute: metrics.charsPerMinute || 0,
      },
    };
  }

  function replaceWithCount(text, regex, replacement, counts, key) {
    return text.replace(regex, function replacer(match, ...args) {
      counts[key] = (counts[key] || 0) + 1;
      if (typeof replacement === "function") {
        return replacement(match, ...args);
      }
      return String(replacement).replace(/\$(\d+)/g, function insertGroup(groupMatch, groupIndex) {
        return args[Number(groupIndex) - 1] || "";
      });
    });
  }

  function deidentifyTranscript(text) {
    let output = normalizeText(text);
    const counts = {};

    output = replaceWithCount(output, /(姓名|病歷號|身分證|電話|手機|地址|生日|出生日期)\s*[:：]\s*[^\n，。；;]+/g, "$1：[已去識別]", counts, "欄位");
    output = replaceWithCount(output, /\b[A-Z][12]\d{8}\b/gi, "[身分證字號]", counts, "身分證字號");
    output = replaceWithCount(output, /\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b/g, "[電子郵件]", counts, "電子郵件");
    output = replaceWithCount(output, /(?:\+?886[-\s]?)?0?9\d{2}[-\s]?\d{3}[-\s]?\d{3}/g, "[手機號碼]", counts, "手機號碼");
    output = replaceWithCount(output, /0\d{1,2}[-\s]?\d{6,8}(?:#\d{1,5})?/g, "[電話號碼]", counts, "電話號碼");
    output = replaceWithCount(output, /\b\d{3,4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/g, "[卡號]", counts, "卡號");
    output = replaceWithCount(output, /(民國\s*)?\d{2,4}\s*[年/-]\s*\d{1,2}\s*[月/-]\s*\d{1,2}\s*日?/g, "[日期]", counts, "日期");
    output = replaceWithCount(output, /\d{1,2}\s*月\s*\d{1,2}\s*日/g, "[日期]", counts, "日期");
    output = replaceWithCount(output, /(?:臺北|台北|新北|桃園|臺中|台中|臺南|台南|高雄|基隆|新竹|苗栗|彰化|南投|雲林|嘉義|屏東|宜蘭|花蓮|臺東|台東|澎湖|金門|連江)[市縣][^，。；;\n]{0,24}(?:路|街|巷|弄|號)/g, "[地址]", counts, "地址");
    output = replaceWithCount(output, /[\u4e00-\u9fa5]{2,12}(?:醫院|診所|公司|學校|大學|機構)/g, "[機構]", counts, "機構");

    output = output.replace(/(我叫|我是|姓名[:：]?)\s*([\u4e00-\u9fa5]{2,4})/g, function nameIntro(match, prefix) {
      counts["姓名"] = (counts["姓名"] || 0) + 1;
      return `${prefix}[姓名]`;
    });

    const surname = "陳林黃張李王吳劉蔡楊許鄭謝郭洪邱曾廖賴徐周葉蘇莊呂江何蕭羅高簡朱鍾施游詹沈彭胡余盧潘顏梁趙柯翁魏孫戴范方宋鄧杜侯曹薛傅丁溫紀";
    const honorificRegex = new RegExp(`[${surname}][\\u4e00-\\u9fa5]{1,2}(?:先生|小姐|女士|太太|醫師|醫生|主任|護理師)`, "g");
    output = replaceWithCount(output, honorificRegex, "[姓名稱謂]", counts, "姓名稱謂");

    return { text: output, counts };
  }

  function buildClinicalReport(transcript, deidentified, bsrs, mood) {
    const itemLines = bsrs.items
      .map((item) => `- ${item.label}：${item.score}/4，信心 ${Math.round(item.confidence * 100)}%，依據：${item.evidence[0] || "未擷取到明確句子"}`)
      .join("\n");
    const piiSummary = Object.keys(deidentified.counts).length
      ? Object.entries(deidentified.counts)
          .map(([key, value]) => `${key} ${value}`)
          .join("、")
      : "未偵測到明確個資";

    return [
      `BSRS-5 總分：${bsrs.total}/20`,
      `風險分層：${bsrs.risk.label}`,
      `自殺意念附加題：${bsrs.suicide.score}/4`,
      `主要情緒：${mood.dominantMood}`,
      `喚起程度：${mood.arousalLevel}`,
      "",
      "分項：",
      itemLines,
      `- 自殺意念：${bsrs.suicide.score}/4，依據：${bsrs.suicide.evidence[0] || "未擷取到明確句子"}`,
      "",
      "去識別化：",
      piiSummary,
      "",
      "臨床提醒：",
      bsrs.risk.message,
      "本結果為對話文字的輔助篩檢輸出，需由醫療專業人員結合完整病史、精神狀態檢查與安全評估判讀。",
    ].join("\n");
  }

  function analyzeTranscript(text, voiceMetrics) {
    const normalized = normalizeText(text);
    const deidentified = deidentifyTranscript(normalized);
    const bsrs = analyzeBSRS(normalized);
    const mood = analyzeMood(normalized, bsrs, voiceMetrics);
    const report = buildClinicalReport(normalized, deidentified, bsrs, mood);
    return {
      transcript: normalized,
      deidentified,
      bsrs,
      mood,
      report,
      createdAt: new Date().toISOString(),
    };
  }

  return {
    BSRS_ITEMS,
    SUICIDE_ITEM,
    analyzeTranscript,
    analyzeBSRS,
    analyzeMood,
    deidentifyTranscript,
  };
});
