@echo off
REM Check if Node.js and npm are installed

echo ============================================================
echo   Checking Node.js Installation
echo ============================================================
echo.

echo Checking Node.js version...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Node.js is NOT installed!
    echo.
    echo SOLUTION:
    echo 1. Download from: https://nodejs.org/
    echo 2. Install the LTS version
    echo 3. Restart this script
    echo.
    pause
    start https://nodejs.org/
    exit /b 1
) else (
    echo [OK] Node.js is installed
    node --version
)

echo.
echo Checking npm version...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] npm is NOT installed!
    echo.
    echo This is unusual - npm should come with Node.js
    echo Try reinstalling Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
) else (
    echo [OK] npm is installed
    npm --version
)

echo.
echo ============================================================
echo   All prerequisites are installed!
echo ============================================================
echo.
echo You can now run: SETUP_FRONTEND_NOW.bat
echo.

pause
