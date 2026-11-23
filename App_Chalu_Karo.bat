@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Social Auto App
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY ( python --version >nul 2>&1 && set "PY=python" )
if not defined PY (
  echo Python nathi - pehla "Install_Karo.bat" chalavo.
  pause
  exit /b 1
)
echo Social Auto App chalu thay chhe ...
echo (Aa kaali window BAND NA KARO - nani kari do. Keys taalu hoy to master password puchhshe.)
start "" /min cmd /c "timeout /t 5 >nul & start msedge --app=http://localhost:8080 || start http://localhost:8080"
%PY% main.py --app
echo.
echo App band thai. Upar laal bhul hoy to eno photo Claude ne mokalo.
pause
