@echo off
setlocal EnableExtensions
chcp 65001 >nul
title LM Studio Chinese Patch v2.0
set "PATCH_DIR=%~dp0"
set "CMD=%~1"
cd /d "%PATCH_DIR%"
if not exist "%PATCH_DIR%logs" mkdir "%PATCH_DIR%logs"

if not exist "%PATCH_DIR%install.py" (
  echo [ERROR] install.py not found in %PATCH_DIR%
  pause
  exit /b 1
)

set "PYTHON_EXE="
for %%V in (313 312 311 310 39) do if not defined PYTHON_EXE if exist "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe"
for %%V in (313 312 311 310 39) do if not defined PYTHON_EXE if exist "C:\Program Files\Python%%V\python.exe" set "PYTHON_EXE=C:\Program Files\Python%%V\python.exe"
if not defined PYTHON_EXE if exist "C:\Windows\py.exe" set "PYTHON_EXE=C:\Windows\py.exe"
if not defined PYTHON_EXE (
  where py.exe >nul 2>&1 && set "PYTHON_EXE=py.exe"
)
if not defined PYTHON_EXE (
  where python.exe >nul 2>&1 && set "PYTHON_EXE=python.exe"
)
if not defined PYTHON_EXE (
  echo [ERROR] Python not found. Please install Python 3 first.
  pause
  exit /b 1
)

echo [OK] Python: %PYTHON_EXE%
echo [OK] Patch dir: %PATCH_DIR%
echo.
"%PYTHON_EXE%" "%PATCH_DIR%install.py" %*
set "RC=%errorlevel%"
echo. >> "%PATCH_DIR%logs\bat.log"
echo [%date% %time%] install.py exit code %RC% >> "%PATCH_DIR%logs\bat.log"
if "%RC%"=="0" goto :ok
echo.
echo [FAILED] Setup finished with code %RC%. Quit LM Studio from the tray, then run again.
echo See logs\bat.log and logs\install.log for details.
goto :end
:ok
if /i not "%CMD%"=="status" (
  echo.
  echo [OK] Quit LM Studio from the tray, then reopen it to apply the patch.
)
:end
echo.
echo Usage: install / uninstall / update / status
echo.
if not defined LMS_NO_PAUSE pause
