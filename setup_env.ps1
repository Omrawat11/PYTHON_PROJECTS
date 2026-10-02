Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "🚀 PYTHON_PROJECTS - VIRTUAL ENVIRONMENT & SETUP" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Check Python
try {
    $pyVersion = & python --version
    Write-Host "🐍 Found: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found in PATH! Please install Python from https://www.python.org" -ForegroundColor Red
    exit 1
}

# 2. Create venv
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "`n📦 Step 1: Creating virtual environment 'venv'..." -ForegroundColor Yellow
    & python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment 'venv' created successfully!" -ForegroundColor Green
} else {
    Write-Host "`nℹ️ Virtual environment 'venv' already exists." -ForegroundColor Gray
}

# 3. Upgrade pip
Write-Host "`n🔄 Step 2: Upgrading pip inside venv..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe -m pip install --upgrade pip --quiet

# 4. Install all requirements
Write-Host "`n📥 Step 3: Installing all dependencies from requirements.txt..." -ForegroundColor Yellow
& .\venv\Scripts\pip.exe install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ All packages successfully installed inside venv!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ Some packages may have finished with warnings." -ForegroundColor Yellow
}

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "🎉 ALL SET! HOW TO ACTIVATE & USE:" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "1. Activate in PowerShell:  .\venv\Scripts\Activate.ps1"
Write-Host "2. Run Streamlit:           .\venv\Scripts\streamlit.exe run Rock_Paper_Scissor\PROJ_3.py"
Write-Host "3. Run any Python script:   .\venv\Scripts\python.exe <filename.py>"
Write-Host "========================================================`n"
