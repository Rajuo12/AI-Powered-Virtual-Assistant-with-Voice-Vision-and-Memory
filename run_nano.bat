@echo off
title Nano AI Desktop Assistant
color 0C

echo.
echo  ==============================================
echo        NANO AI DESKTOP ASSISTANT
echo  ==============================================
echo.

:: Start Ollama if not running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >NUL
if %errorlevel% neq 0 (
    echo [1/3] Starting Ollama...
    start /min "Ollama" ollama serve
    timeout /t 3 /nobreak >nul
) else (
    echo [1/3] Ollama already running
)

:: Start API server
echo [2/2] Starting FastAPI Backend (port 8000)...
start /min "Nano API Server" python api_server.py
timeout /t 2 /nobreak >nul

:: Start agent (passes any arguments like --text)
python agent_nano.py %*

pause