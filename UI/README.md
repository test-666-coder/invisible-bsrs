# 隱形溫度計 UI

這個資料夾是新版 BSRS-5 量表畫面。它可以載入既有 JSON，也可以把音檔送到本機 Python 模型服務，完成「聲音 -> 逐字稿 -> 去識別化 -> 語音情緒 -> BSRS JSON -> UI」流程。

## 啟動方式

請先確認已安裝 Node.js 22.13 以上，並在專案根目錄完成 Python 環境與 `.env` 設定。

先在專案根目錄啟動模型服務：

```powershell
.\.venv\Scripts\python.exe -m uvicorn patient_mood_pipeline.web_api:app --host 127.0.0.1 --port 8765
```

再啟動 UI：

```powershell
cd UI
npm install
npm run dev
```

開啟 UI 後按「上傳音檔」。音檔選好後會自動分析，完成時畫面會直接更新量表結果。

## 輸出檔案

模型服務會把每次分析的檔案保留在專案根目錄：

- `outputs/ui_uploads/`：上傳音檔
- `outputs/ui_runs/*_asr_transcript.txt`：語音轉文字
- `outputs/ui_runs/*_deidentified_transcript.txt`：去識別化逐字稿
- `outputs/ui_runs/*_voice_emotion.json`：語音情緒
- `outputs/ui_runs/*_bsrs.json`：量表 JSON

前端預設呼叫 `http://127.0.0.1:8765`。如果需要改位置，可在啟動 UI 前設定：

```powershell
$env:NEXT_PUBLIC_PIPELINE_API_URL="http://127.0.0.1:8765"
```
