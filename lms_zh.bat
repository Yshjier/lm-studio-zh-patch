@echo off
chcp 65001 >nul
REM LM Studio 中文汉化 — 单文件管理工具启动器
REM 直接双击即可; 工具内部会自动请求 UAC 提权(安装/卸载/适配新版时)。
where py >nul 2>&1
if %errorlevel%==0 (
    py "%~dp0lms_zh.py" %*
) else (
    python "%~dp0lms_zh.py" %*
)
