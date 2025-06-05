@echo off
setlocal enabledelayedexpansion
set "REQUIRED_VERSION=3.13.3"
set "INSTALLER_NAME=python-%REQUIRED_VERSION%-amd64.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/%REQUIRED_VERSION%/%INSTALLER_NAME%"

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do (
    if "%%v"=="%REQUIRED_VERSION%" (
        echo ... Python %REQUIRED_VERSION% is already installed ...
        goto END
    )
)

echo ... Python %REQUIRED_VERSION% is not installed ...
echo Downloading installer...

powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_NAME%'"

echo Installing Python %REQUIRED_VERSION%...
start /wait "" "%INSTALLER_NAME%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

del "%INSTALLER_NAME%"

echo Python %REQUIRED_VERSION% installation complete.
:END

powershell -Command "python.exe -m pip install --upgrade pip"
Python Setup_GAMMAP.py
pause
exit /b
