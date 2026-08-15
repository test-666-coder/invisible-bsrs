# 使用教學

這份文件說明如何從一台新電腦啟動 Invisible BSRS Demo。完成後，使用者可以在瀏覽器上傳醫病對話音檔，系統會跑完：

```text
音檔 -> 語音轉文字 -> 去識別化 -> 逐字稿校正 -> 語音情緒 -> BSRS JSON -> UI 量表
```

> 目前專案是概念驗證 Demo，不可用於真實臨床診斷或正式醫療決策。

## 需要先安裝

- Python 3.10 以上
- Node.js 22.13 以上
- Git
- OpenAI API key
- 可選：NVIDIA GPU。沒有 GPU 也能跑，但本地語音模型會比較慢。

## 1. 下載專案

```powershell
git clone https://github.com/test-666-coder/invisible-bsrs.git
cd invisible-bsrs
```

## 2. 建立 Python 環境

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. 建立環境設定

```powershell
copy .env.example .env
```

打開 `.env`，至少填入：

```text
OPENAI_API_KEY=你的 OpenAI API key
```

預設語音轉文字模型是：

```text
ASR_MODEL_ID=openai/whisper-tiny
```

如果語音辨識錯誤率太高，可以改成：

```text
ASR_MODEL_ID=openai/whisper-small
```

`whisper-small` 下載較久、吃更多記憶體，但通常比 `tiny` 穩。

## 4. 下載本地模型

```powershell
python -m patient_mood_pipeline.download_models
```

模型會下載到 Hugging Face cache。第一次下載可能需要幾分鐘到十幾分鐘，取決於網路和模型大小。

如果 Windows 下載大檔卡住，請確認 `.env` 保留：

```text
HF_HUB_DISABLE_XET=1
HF_HUB_DISABLE_SYMLINKS=1
```

## 5. 安裝 UI 套件

```powershell
cd UI
npm install
cd ..
```

如果 `npm install` 或 `npm run dev` 顯示 Node 版本不符，請先更新 Node.js。UI 的 `package.json` 目前要求 `node >=22.13.0`。

## 6. 啟動完整聲音到 UI 流程

### 方法 A：一鍵啟動

```powershell
.\scripts\start_voice_to_ui.ps1
```

啟動完成後打開：

```text
http://localhost:5174/
```

### 方法 B：手動開兩個終端機

第一個終端機啟動模型服務：

```powershell
.\.venv\Scripts\python.exe -m uvicorn patient_mood_pipeline.web_api:app --host 127.0.0.1 --port 8765
```

第二個終端機啟動 UI：

```powershell
cd UI
npm run dev -- --host localhost --port 5174
```

接著開啟：

```text
http://localhost:5174/
```

## 7. 手動測試

在 UI 按「上傳音檔」，選擇 `.wav`、`.mp3` 或 `.flac` 醫病對話音檔。分析完成後，畫面會顯示 BSRS 量表結果。

每次分析會留下中間檔案，方便確認每個步驟：

- `outputs/ui_uploads/`：上傳的音檔
- `outputs/ui_runs/*_asr_transcript.txt`：語音轉文字結果
- `outputs/ui_runs/*_deidentified_transcript.txt`：去識別化後逐字稿
- `outputs/ui_runs/*_corrected_transcript.txt`：GPT 校正後逐字稿
- `outputs/ui_runs/*_voice_emotion.json`：語音情緒分析
- `outputs/ui_runs/*_bsrs.json`：BSRS 量表 JSON

## 8. 只跑後端管線

如果不想開 UI，也可以直接對音檔跑完整流程：

```powershell
python -m patient_mood_pipeline.run --audio .\samples\your_audio.wav --session-id demo-001 --output .\outputs\result.json --intermediate-prefix .\outputs\manual_test
```

如果已經有逐字稿，可以跳過語音轉文字：

```powershell
python -m patient_mood_pipeline.run --transcript-file .\samples\your_transcript.txt --output .\outputs\result.json
```

只測本地模型、不呼叫 OpenAI：

```powershell
python -m patient_mood_pipeline.run --audio .\samples\your_audio.wav --local-only --output .\outputs\local_only.json
```

## 9. 常見問題

### UI 顯示「請確認本機模型服務已啟動」

代表 `http://127.0.0.1:8765` 沒有服務在跑。請先啟動：

```powershell
.\.venv\Scripts\python.exe -m uvicorn patient_mood_pipeline.web_api:app --host 127.0.0.1 --port 8765
```

### 第一次上傳音檔很慢

第一次分析會載入本地模型，GPU 或 CPU 使用率可能需要一段時間才會上來。後續同一個服務沒有關掉時，通常會比較快。

### 語音轉文字錯誤率太高

先確認音檔格式正常，建議使用清楚的單聲道 `.wav`。如果仍不穩，把 `.env` 改成：

```text
ASR_MODEL_ID=openai/whisper-small
ASR_NUM_BEAMS=5
```

改完後需要重新啟動模型服務。

### 想確認目前使用哪些模型

啟動模型服務後打開：

```text
http://127.0.0.1:8765/api/health
```

裡面會列出目前 ASR、去識別化、語音情緒和 OpenAI 量表模型。
