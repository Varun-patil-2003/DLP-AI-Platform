@echo off
REM Quick AI Integration Installation Script
REM Installs Google Gemini AI SDK

echo ============================================================
echo   AI Integration Setup - Google Gemini
echo ============================================================
echo.

echo [1/2] Installing Google Generative AI SDK...
pip install --upgrade google-generativeai

echo.
echo [2/2] Verifying installation...
pip show google-generativeai

echo.
echo ============================================================
echo   Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Run: python app\app.py
echo 2. Look for: [OK] Google Gemini AI initialized successfully
echo 3. Start making predictions with AI-powered alerts!
echo.
echo Guide: AI_INTEGRATION_GUIDE.md
echo ============================================================

pause
