@echo off
cd /d "%~dp0"
@py "%~dp0GAMMAP.py"
set SCRIPT="%~dp0GAMMAP.py"
if not exist %SCRIPT% (
    echo ❌ ERROR: File not found at %SCRIPT%
)
exit /b