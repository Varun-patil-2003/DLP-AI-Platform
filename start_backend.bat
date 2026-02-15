@echo off
REM Start Flask Backend

echo ============================================================
echo   Starting Flask Backend with AI Integration
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting server...
echo.
echo Backend will be available at:
echo   - Local: http://localhost:5000
echo   - Network: http://YOUR_IP:5000
echo.
echo Press Ctrl+C to stop
echo ============================================================
echo.

python app\app.py

pause
