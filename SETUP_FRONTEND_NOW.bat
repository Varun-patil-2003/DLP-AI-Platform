@echo off
REM One-click frontend setup and start

echo ============================================================
echo   FRONTEND SETUP - ONE TIME INSTALLATION
echo ============================================================
echo.

cd /d "%~dp0frontend"

echo Current directory: %CD%
echo.

REM Check if node_modules exists
if exist "node_modules\" (
    echo Dependencies already installed!
    echo.
) else (
    echo Installing dependencies... This will take 2-3 minutes.
    echo Please be patient...
    echo.
    
    call npm install
    
    if %errorlevel% neq 0 (
        echo.
        echo ============================================================
        echo   ERROR: Installation failed!
        echo ============================================================
        echo.
        echo Please check:
        echo 1. Are you connected to the internet?
        echo 2. Is Node.js installed? Run: node --version
        echo.
        echo If Node.js is not installed:
        echo - Download from: https://nodejs.org/
        echo - Install it
        echo - Run this file again
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo ============================================================
    echo   Installation Complete!
    echo ============================================================
    echo.
)

echo Starting frontend server...
echo.
echo The browser will open automatically.
echo Close this window to stop the server.
echo.
echo ============================================================

call npm start

pause
