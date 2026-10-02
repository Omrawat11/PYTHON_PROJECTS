@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo 🚀 PYTHON_PROJECTS - VIRTUAL ENVIRONMENT & SETUP
echo ========================================================

:: 1. Verify Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not found in your system PATH!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i
echo 🐍 Using System: !PY_VER!

:: 2. Create virtual environment if it does not exist
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo 📦 Step 1: Creating isolated virtual environment in 'venv'...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment 'venv'.
        pause
        exit /b 1
    )
    echo ✅ Created 'venv' successfully!
) else (
    echo.
    echo ℹ️ Virtual environment 'venv' already exists.
)

:: 3. Upgrade pip inside the virtual environment
echo.
echo 🔄 Step 2: Upgrading pip inside venv...
call venv\Scripts\python.exe -m pip install --upgrade pip --quiet

:: 4. Install all consolidated requirements
echo.
echo 📥 Step 3: Installing all workspace dependencies from requirements.txt...
echo This will install Streamlit, Pygame, Pillow, Requests, Instaloader, Matplotlib, etc.
call venv\Scripts\pip.exe install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ⚠️ Warning: Some optional packages may have encountered warnings.
) else (
    echo.
    echo ✅ All packages successfully downloaded and installed inside venv!
)

echo.
echo ========================================================
echo 🎉 ALL SET! HOW TO USE YOUR VIRTUAL ENVIRONMENT:
echo ========================================================
echo 1. Activate venv in Command Prompt:
echo    call venv\Scripts\activate
echo.
echo 2. Or in PowerShell:
echo    .\venv\Scripts\Activate.ps1
echo.
echo 3. Run any project with the venv python:
echo    venv\Scripts\streamlit.exe run Rock_Paper_Scissor\PROJ_3.py
echo ========================================================
pause
