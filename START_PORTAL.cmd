@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Follow README setup first to create the Python environment.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" scripts\start_portal.py
if errorlevel 1 pause
