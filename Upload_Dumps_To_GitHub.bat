@echo off
setlocal
cd /d "%~dp0"

echo ================================================================
echo  GIMI-Model-Dumps - 1-Click GitHub Upload (Genshin / Wuwa / NTE)
echo ================================================================
echo.
echo Folders scanned:
echo   - %~dp0Genshin
echo   - %~dp0Wuwa
echo   - %~dp0NTE
echo.

python tools\sync_dumps.py --push
if errorlevel 1 (
    echo.
    echo [!] Upload encountered an issue. Please review the messages above.
    pause
    exit /b 1
)

echo.
pause
endlocal
