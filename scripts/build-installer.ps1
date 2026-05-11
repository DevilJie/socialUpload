# build-installer.ps1 — 构建完整的一键安装包
# 包含: Python 运行环境 + Flask 后端 + 前端

$ErrorActionPreference = "Stop"
$PROJECT_ROOT = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"
$FRONTEND_DIR = Join-Path $PROJECT_ROOT "frontend"
$TAURI_DIR = Join-Path $PROJECT_ROOT "src-tauri"
$PYTHON_VERSION = "3.12.0"
$PYTHON_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-3.12.0-embed-amd64.zip"
$PYTHON_ZIP = Join-Path $env:TEMP "python-embed.zip"
$PYTHON_DIR = Join-Path $TAURI_DIR "python"

function Write-Step {
    param($msg)
    Write-Host "[BUILD] $msg" -ForegroundColor Cyan
}

Write-Step "Starting installer build..."

# Step 1: 下载 Python embeddable
Write-Step "Downloading Python $PYTHON_VERSION..."
if (-not (Test-Path $PYTHON_ZIP)) {
    Invoke-WebRequest -Uri $PYTHON_URL -OutFile $PYTHON_ZIP
}

# Step 2: 解压 Python
Write-Step "Extracting Python..."
if (Test-Path $PYTHON_DIR) {
    Remove-Item $PYTHON_DIR -Recurse -Force
}
Expand-Archive -Path $PYTHON_ZIP -DestinationPath $PYTHON_DIR

# Step 3: 创建 venv
Write-Step "Creating Python venv..."
$VENV_DIR = Join-Path $BACKEND_DIR "venv"
if (Test-Path $VENV_DIR) {
    Remove-Item $VENV_DIR -Recurse -Force
}
python -m venv $VENV_DIR

# Step 4: 安装依赖
Write-Step "Installing Python dependencies..."
& "$VENV_DIR\Scripts\pip.exe" install --upgrade pip
& "$VENV_DIR\Scripts\pip.exe" install -r "$BACKEND_DIR\requirements.txt"
& "$VENV_DIR\Scripts\pip.exe" install waitress

# Step 5: 构建前端
Write-Step "Building frontend..."
Set-Location $FRONTEND_DIR
npm install
npm run build
Set-Location $TAURI_DIR

Write-Step "Build complete! Run: npx tauri build"