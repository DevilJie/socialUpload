# build-installer.ps1 — 构建完整的一键安装包
# 包含: Python 运行环境 + Flask 后端 + 前端

$ErrorActionPreference = "Stop"
$PROJECT_ROOT = Split-Path $PSScriptRoot -Parent
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"
$FRONTEND_DIR = Join-Path $PROJECT_ROOT "frontend"
$TAURI_DIR = Join-Path $PROJECT_ROOT "src-tauri"
$PYTHON_DIR = Join-Path $PROJECT_ROOT "python"
$VENV_DIR = Join-Path $BACKEND_DIR "venv"
$VENV_SCRIPTS = Join-Path $VENV_DIR "Scripts"
$VENV_PYTHON = Join-Path $VENV_SCRIPTS "python.exe"

function Write-Step {
    param($msg)
    Write-Host "[BUILD] $msg" -ForegroundColor Cyan
}

Write-Step "Starting installer build..."

# Step 1: 创建或更新 backend/venv
Write-Step "Creating/updating Python venv..."
if (Test-Path $VENV_DIR) {
    Remove-Item $VENV_DIR -Recurse -Force
}
python -m venv $VENV_DIR

# Step 2: 安装依赖
Write-Step "Installing Python dependencies..."
& "$VENV_PYTHON" -m pip install --upgrade pip
& "$VENV_PYTHON" -m pip install -r "$BACKEND_DIR\requirements.txt"

# Step 3: 复制 venv 到 src-tauri/python
Write-Step "Copying venv to src-tauri/python..."
if (Test-Path $PYTHON_DIR) {
    Remove-Item $PYTHON_DIR -Recurse -Force
}
Copy-Item -Path $VENV_DIR -Destination $PYTHON_DIR -Recurse

# 验证 Scripts/python.exe 存在
$VENV_PYTHON_CHECK = Join-Path (Join-Path $PYTHON_DIR "Scripts") "python.exe"
if (-not (Test-Path $VENV_PYTHON_CHECK)) {
    Write-Host "[ERROR] venv copy failed! Scripts/python.exe not found at $VENV_PYTHON_CHECK" -ForegroundColor Red
    Write-Host "This is NOT a venv! Check if backend/venv was created correctly." -ForegroundColor Red
    Remove-Item $PYTHON_DIR -Recurse -Force -ErrorAction SilentlyContinue
    exit 1
}
Write-Step "venv validated successfully!"

# Step 4: 构建前端
Write-Step "Building frontend..."
Set-Location $FRONTEND_DIR
npm install
npm run build
Set-Location $TAURI_DIR

Write-Step "Build complete! Run: npx tauri build"
