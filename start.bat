@echo off
title ZETRA DISCORD FIVEM BOT

:START
cls
echo ===============================
echo     ZETRA DISCORD FIVEM BOT
echo ===============================
echo.

REM 
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    pause
    exit
)

echo Python detected.
echo.

REM
echo Starting bot...
echo.

python main.py
set EXITCODE=%ERRORLEVEL%

echo.
echo Bot stopped with exit code %EXITCODE%.
echo Restarting in 5 seconds...
echo Press CTRL+C to stop.
echo.

timeout /t 5 >nul
goto START
