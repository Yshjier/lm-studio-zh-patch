@echo off
chcp 65001 >nul
where py >nul 2>&1
if %errorlevel%==0 (
    py "%~dp0lms_zh.py" %*
) else (
    python "%~dp0lms_zh.py" %*
)