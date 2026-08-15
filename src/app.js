(function startApp() {
  const analyzer = window.MoodThermometer;
  const $ = (selector) => document.querySelector(selector);

  const nodes = {
    transcript: $("#transcriptInput"),
    analyzeButton: $("#analyzeButton"),
    sampleButton: $("#sampleButton"),
    startSpeechButton: $("#startSpeechButton"),
    stopSpeechButton: $("#stopSpeechButton"),
    clearButton: $("#clearButton"),
    copyButton: $("#copyButton"),
    exportButton: $("#exportButton"),
    speechStatus: $("#speechStatus"),
    paceMetric: $("#paceMetric"),
    energyMetric: $("#energyMetric"),
    voiceMoodMetric: $("#voiceMoodMetric"),
    totalScore: $("#totalScore"),
    thermometerFill: $("#thermometerFill"),
    riskBadge: $("#riskBadge"),
    riskNote: $("#riskNote"),
    scaleBody: $("#scaleBody"),
    deidentifiedOutput: $("#deidentifiedOutput"),
    dominantMood: $("#dominantMood"),
    arousalLevel: $("#arousalLevel"),
    suicideScore: $("#suicideScore"),
    clinicalReport: $("#clinicalReport"),
  };

  const sampleTranscript = [
    "醫師：最近一週睡眠怎麼樣？",
    "患者：幾乎每天都睡不好，半夜醒來後就很難再睡。",
    "醫師：情緒有什麼變化？",
    "患者：一直很緊張，擔心工作會出錯，也很容易對家人生氣。這幾天心情很低落，覺得自己很沒用。",
    "醫師：有沒有想傷害自己，或是不想活的念頭？",
    "患者：沒有想傷害自己，也沒有不想活。",
  ].join("\n");

  let recognition = null;
  let finalTranscript = "";
  let mediaStream = null;
  let audioContext = null;
  let analyserNode = null;
  let animationId = null;
  let lastResult = null;
  let voiceStats = resetVoiceStats();

  function resetVoiceStats() {
    return {
      startedAt: 0,
      endedAt: 0,
      samples: 0,
      sumRms: 0,
      sumVariance: 0,
      peakRms: 0,
      avgRms: 0,
      variance: 0,
      durationSeconds: 0,
      charsPerMinute: 0,
    };
  }

  function setStatus(text, mode) {
    nodes.speechStatus.textContent = text;
    nodes.speechStatus.classList.toggle("status-pill--accent", mode === "accent");
  }

  function getSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return null;
    const instance = new SpeechRecognition();
    instance.lang = "zh-TW";
    instance.continuous = true;
    instance.interimResults = true;
    return instance;
  }

  async function startSpeech() {
    recognition = getSpeechRecognition();
    if (!recognition) {
      setStatus("瀏覽器不支援", "accent");
      return;
    }

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setupAudioMeter(mediaStream);
      finalTranscript = nodes.transcript.value.trim();
      voiceStats = resetVoiceStats();
      voiceStats.startedAt = Date.now();

      recognition.onresult = handleSpeechResult;
      recognition.onerror = () => setStatus("語音中斷", "accent");
      recognition.onend = () => {
        nodes.startSpeechButton.disabled = false;
        nodes.stopSpeechButton.disabled = true;
        stopAudioMeter();
        if (nodes.transcript.value.trim()) runAnalysis();
      };

      recognition.start();
      nodes.startSpeechButton.disabled = true;
      nodes.stopSpeechButton.disabled = false;
      setStatus("聆聽中", "");
    } catch (error) {
      setStatus("麥克風未開啟", "accent");
    }
  }

  function stopSpeech() {
    if (recognition) recognition.stop();
    nodes.startSpeechButton.disabled = false;
    nodes.stopSpeechButton.disabled = true;
    setStatus("已停止", "");
    stopAudioMeter();
  }

  function handleSpeechResult(event) {
    let interim = "";
    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const transcript = event.results[index][0].transcript;
      if (event.results[index].isFinal) {
        finalTranscript = `${finalTranscript}\n${transcript}`.trim();
      } else {
        interim += transcript;
      }
    }
    nodes.transcript.value = [finalTranscript, interim].filter(Boolean).join("\n");
    updateSpeechDerivedMetrics();
  }

  function setupAudioMeter(stream) {
    audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 1024;
    source.connect(analyserNode);
    readAudioMeter();
  }

  function readAudioMeter() {
    if (!analyserNode) return;
    const buffer = new Uint8Array(analyserNode.fftSize);
    analyserNode.getByteTimeDomainData(buffer);
    let sumSquares = 0;
    for (const value of buffer) {
      const centered = (value - 128) / 128;
      sumSquares += centered * centered;
    }
    const rms = Math.sqrt(sumSquares / buffer.length);
    voiceStats.samples += 1;
    voiceStats.sumRms += rms;
    voiceStats.peakRms = Math.max(voiceStats.peakRms, rms);
    voiceStats.avgRms = voiceStats.sumRms / voiceStats.samples;
    voiceStats.sumVariance += Math.abs(rms - voiceStats.avgRms);
    voiceStats.variance = voiceStats.sumVariance / voiceStats.samples;
    nodes.energyMetric.textContent = voiceStats.variance > 0.035 ? "起伏大" : voiceStats.avgRms > 0.08 ? "偏高" : "平穩";
    animationId = requestAnimationFrame(readAudioMeter);
  }

  function stopAudioMeter() {
    if (animationId) cancelAnimationFrame(animationId);
    if (mediaStream) mediaStream.getTracks().forEach((track) => track.stop());
    if (audioContext && audioContext.state !== "closed") audioContext.close();
    animationId = null;
    mediaStream = null;
    audioContext = null;
    analyserNode = null;
    updateSpeechDerivedMetrics();
  }

  function updateSpeechDerivedMetrics() {
    if (!voiceStats.startedAt) return;
    voiceStats.endedAt = Date.now();
    voiceStats.durationSeconds = Math.max(1, (voiceStats.endedAt - voiceStats.startedAt) / 1000);
    const charCount = nodes.transcript.value.replace(/\s/g, "").length;
    voiceStats.charsPerMinute = Math.round((charCount / voiceStats.durationSeconds) * 60);
    nodes.paceMetric.textContent = voiceStats.charsPerMinute > 210 ? "偏快" : voiceStats.charsPerMinute < 70 ? "偏慢" : "適中";
  }

  function runAnalysis() {
    const text = nodes.transcript.value.trim();
    if (!text) {
      setStatus("待輸入", "accent");
      return;
    }
    updateSpeechDerivedMetrics();
    lastResult = analyzer.analyzeTranscript(text, voiceStats);
    renderResult(lastResult);
    setStatus("已分析", "");
  }

  function renderResult(result) {
    nodes.totalScore.textContent = result.bsrs.total;
    nodes.thermometerFill.style.width = `${Math.min(100, (result.bsrs.total / 20) * 100)}%`;
    nodes.riskBadge.textContent = result.bsrs.risk.label;
    nodes.riskNote.textContent = result.bsrs.risk.message;
    nodes.riskNote.classList.remove("is-warning", "is-critical");
    if (result.bsrs.risk.className) nodes.riskNote.classList.add(result.bsrs.risk.className);

    const rows = result.bsrs.items.concat(result.bsrs.suicide).map((item) => {
      const high = item.score >= 3 || (item.id === "suicide" && item.score >= 2);
      return `
        <tr>
          <td><strong>${item.label}</strong><div class="evidence">${item.prompt}</div></td>
          <td><span class="score-badge ${high ? "score-high" : ""}">${item.score}</span></td>
          <td>${Math.round(item.confidence * 100)}%</td>
          <td><div class="evidence">${item.evidence.join("；") || "未擷取到明確句子"}</div></td>
        </tr>
      `;
    });
    nodes.scaleBody.innerHTML = rows.join("");

    nodes.deidentifiedOutput.textContent = result.deidentified.text || "尚未產生";
    nodes.dominantMood.textContent = result.mood.dominantMood;
    nodes.arousalLevel.textContent = result.mood.arousalLevel;
    nodes.suicideScore.textContent = `${result.bsrs.suicide.score}/4`;
    nodes.voiceMoodMetric.textContent = result.mood.dominantMood;
    nodes.paceMetric.textContent = result.mood.voice.paceLabel;
    nodes.energyMetric.textContent = result.mood.voice.energyLabel;
    nodes.clinicalReport.textContent = result.report;
  }

  function clearAll() {
    nodes.transcript.value = "";
    nodes.scaleBody.innerHTML = "";
    nodes.deidentifiedOutput.textContent = "尚未產生";
    nodes.clinicalReport.textContent = "尚未產生";
    nodes.totalScore.textContent = "--";
    nodes.thermometerFill.style.width = "0%";
    nodes.riskBadge.textContent = "尚未分析";
    nodes.riskNote.textContent = "請先輸入逐字稿。結果僅供醫療專業人員作為篩檢參考。";
    nodes.riskNote.classList.remove("is-warning", "is-critical");
    nodes.dominantMood.textContent = "--";
    nodes.arousalLevel.textContent = "--";
    nodes.suicideScore.textContent = "--";
    nodes.paceMetric.textContent = "--";
    nodes.energyMetric.textContent = "--";
    nodes.voiceMoodMetric.textContent = "--";
    lastResult = null;
    setStatus("待命", "");
  }

  async function copyReport() {
    if (!lastResult) runAnalysis();
    if (!lastResult) return;
    await navigator.clipboard.writeText(lastResult.report);
    setStatus("已複製", "");
  }

  function exportJson() {
    if (!lastResult) runAnalysis();
    if (!lastResult) return;
    const blob = new Blob([JSON.stringify(lastResult, null, 2)], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const stamp = new Date().toISOString().replace(/[:.]/g, "-");
    link.href = url;
    link.download = `bsrs-report-${stamp}.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  nodes.startSpeechButton.addEventListener("click", startSpeech);
  nodes.stopSpeechButton.addEventListener("click", stopSpeech);
  nodes.analyzeButton.addEventListener("click", runAnalysis);
  nodes.sampleButton.addEventListener("click", () => {
    nodes.transcript.value = sampleTranscript;
    runAnalysis();
  });
  nodes.clearButton.addEventListener("click", clearAll);
  nodes.copyButton.addEventListener("click", copyReport);
  nodes.exportButton.addEventListener("click", exportJson);
  nodes.transcript.addEventListener("input", () => {
    if (nodes.transcript.value.trim()) runAnalysis();
  });
})();
