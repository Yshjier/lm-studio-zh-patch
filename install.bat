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

rem status 在本窗口内运行以便查看输出；其余命令拉起独立 Python 窗口后关闭本 cmd
if /i "%CMD%"=="status" goto :inline

echo [%date% %time%] launching install.py %* >> "%PATCH_DIR%logs\bat.log"
start "LM Studio Patch" "%PYTHON_EXE%" "%PATCH_DIR%install.py" %*
exit /b 0

:inline
"%PYTHON_EXE%" "%PATCH_DIR%install.py" %*
set "RC=%errorlevel%"
echo. >> "%PATCH_DIR%logs\bat.log"
echo [%date% %time%] install.py exit code %RC% >> "%PATCH_DIR%logs\bat.log"
pause
