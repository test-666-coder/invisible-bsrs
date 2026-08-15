param(
  [int]$ApiPort = 8765,
  [int]$UiPort = 5174
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$UiRoot = Join-Path $Root "UI"
$Logs = Join-Path $Root "outputs\devserver_logs"
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Node = (Get-Command node -ErrorAction SilentlyContinue)
$Npm = (Get-Command npm.cmd -ErrorAction SilentlyContinue)
if ($null -eq $Npm) {
  $Npm = (Get-Command npm -ErrorAction SilentlyContinue)
}
$ApiUrl = "http://127.0.0.1:$ApiPort"
$UiUrl = "http://localhost:$UiPort/"

New-Item -ItemType Directory -Force -Path $Logs | Out-Null

function Test-ListeningPort([int]$Port) {
  $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
  return $null -ne $connection
}

function Wait-HttpOk([string]$Url, [int]$Seconds) {
  for ($attempt = 0; $attempt -lt $Seconds; $attempt += 1) {
    try {
      Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3 | Out-Null
      return $true
    } catch {
      Start-Sleep -Seconds 1
    }
  }
  return $false
}

if (-not (Test-Path $Python)) {
  throw "找不到 Python venv：$Python"
}

if ($null -eq $Node) {
  throw "找不到 node。請先安裝 Node.js 22.13 以上，並確認 node 可在 PowerShell 中執行。"
}

if ($null -eq $Npm) {
  throw "找不到 npm。請先安裝 Node.js 22.13 以上，並確認 npm 可在 PowerShell 中執行。"
}

$nodeVersionText = (& $Node.Source --version).Trim()
$nodeVersion = [version]($nodeVersionText.TrimStart("v"))
$minimumNodeVersion = [version]"22.13.0"
if ($nodeVersion -lt $minimumNodeVersion) {
  throw "目前 Node.js 版本是 $nodeVersionText；UI 需要 Node.js 22.13 以上。請更新 Node.js 後再啟動。"
}

if (-not (Test-ListeningPort $ApiPort)) {
  $apiOut = Join-Path $Logs "pipeline_api.out.log"
  $apiErr = Join-Path $Logs "pipeline_api.err.log"
  $apiArgs = "-m uvicorn patient_mood_pipeline.web_api:app --host 127.0.0.1 --port $ApiPort"
  $apiProcess = Start-Process -FilePath $Python -ArgumentList $apiArgs -WorkingDirectory $Root -WindowStyle Hidden -RedirectStandardOutput $apiOut -RedirectStandardError $apiErr -PassThru
  Write-Output "API started: pid=$($apiProcess.Id), url=$ApiUrl"
} else {
  Write-Output "API already listening: $ApiUrl"
}

if (-not (Wait-HttpOk "$ApiUrl/api/health" 20)) {
  throw "模型 API 未在預期時間內啟動：$ApiUrl"
}

if (-not (Test-ListeningPort $UiPort)) {
  $uiOut = Join-Path $Logs "ui.out.log"
  $uiErr = Join-Path $Logs "ui.err.log"
  $env:NEXT_PUBLIC_PIPELINE_API_URL = $ApiUrl
  $uiArgs = "run dev -- --host localhost --port $UiPort"
  $uiProcess = Start-Process -FilePath $Npm.Source -ArgumentList $uiArgs -WorkingDirectory $UiRoot -WindowStyle Hidden -RedirectStandardOutput $uiOut -RedirectStandardError $uiErr -PassThru
  Write-Output "UI started: pid=$($uiProcess.Id), url=$UiUrl"
} else {
  Write-Output "UI already listening: $UiUrl"
}

if (-not (Wait-HttpOk $UiUrl 40)) {
  throw "UI 未在預期時間內啟動：$UiUrl"
}

Write-Output "Ready: $UiUrl"
