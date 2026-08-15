# 心情溫度計輔助分析台

這是一個醫病對話分析原型，現在包含兩層：

- 前端 demo：可貼上逐字稿，快速展示去識別化、情緒線索與 BSRS-5 結果。
- 模型管線：本地 Hugging Face 模型處理語音與個資，最後用 OpenAI API 產生結構化 BSRS JSON。

## 功能

- 語音轉逐字稿：預設 `openai/whisper-small` 本地 ASR。
- 語音轉心情：預設 `Dpngtm/wav2vec2-emotion-recognition` 本地語音情緒分類。
- 逐字稿去識別化：預設 `ckiplab/albert-tiny-chinese-ner` 加上 regex 遮蔽個資。
- 逐字稿與心情轉量表：使用 OpenAI API Structured Outputs 產生 `schema_version=1.1.0` 的 BSRS JSON。

## 使用方式

前端 demo：

```powershell
python -m http.server 5173 --bind 127.0.0.1
```

然後開啟 `http://127.0.0.1:5173/`。

完整模型管線：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m patient_mood_pipeline.download_models
python -m patient_mood_pipeline.run --audio .\samples\conversation.wav --session-id demo-001 --output .\outputs\result.json
```

詳細架構請看 `docs/architecture.md`。

正式輸出的 JSON 頂層會是：

- `session`
- `instrument`
- `assessment.core_items`
- `assessment.core_result`
- `assessment.supplemental_item`
- `clinical_review`
- `analysis_metadata`

其中 `core_result.total_score` 只加總前五題；`suicide_ideation` 是第六題附加題，不納入五題總分。

## 注意

這個版本是 hackathon 原型。量表結果只能作為醫療專業人員的篩檢參考，不能單獨作為診斷。預設不保存原始逐字稿，也不把原始逐字稿送到 OpenAI。
