@echo off
REM Quick script to get your network IP address

echo ============================================================
echo   Your Network IP Address
echo ============================================================
echo.

echo Finding your IPv4 address...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    echo YOUR IP ADDRESS: %%a
)

echo.
echo ============================================================
echo   Access your app from other devices:
echo ============================================================
echo.
echo Replace YOUR_IP with the address shown above:
echo.
echo   Frontend: http://YOUR_IP:3000
echo   Backend:  http://YOUR_IP:5000
echo.
echo Example: http://192.168.1.100:3000
echo.
echo ============================================================
echo.
echo Make sure other devices are on the same WiFi network!
echo.

pause
