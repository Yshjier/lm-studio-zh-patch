@echo off
setlocal
set PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe
set PATH=%PATH%;C:\Program Files\nodejs;C:\Users\Administrator\AppData\Local\Programs\Python\Python312
cd /d "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch"
echo ============================================
echo  LM Studio 汉化补丁 - 一键全量部署
echo ============================================
echo.
"%PY%" _deploy_all.py
echo.
echo ---- 部署日志 (logs\apply.log) ----
type "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\logs\apply.log"
echo.
echo ============================================
pause
