@echo off
REM Install all frontend dependencies

echo ============================================================
echo   Installing Frontend Dependencies
echo ============================================================
echo.

echo This will take 2-3 minutes...
echo Please wait...
echo.

call npm install

echo.
echo ============================================================
if %errorlevel% == 0 (
    echo   Installation Successful!
    echo ============================================================
    echo.
    echo Next step: Run start.bat to launch the frontend
) else (
    echo   Installation Failed!
    echo ============================================================
    echo.
    echo Try running as Administrator
)
echo.

pause
