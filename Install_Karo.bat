@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Social Auto App - Install
set "LOG=%~dp0install_log.txt"
echo ==================================================
echo    Social Auto App - ek click install
echo ==================================================
echo.
if not exist "%~dp0requirements.txt" (
  echo  ! Aa file ZIP ni andar thi chale chhe.
  echo    Pehla zip par right-click - "Extract All" - pachhi kholela folder mathi aa file chalavo.
  pause
  exit /b 1
)
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY ( python --version >nul 2>&1 && set "PY=python" )

if defined PY goto have_python
echo [1/4] Python nathi - jate install thay chhe (5 minute, internet joie)...
winget --version >nul 2>&1
if errorlevel 1 goto no_winget
winget install -e --id Python.Python.3.13 --scope user --accept-package-agreements --accept-source-agreements
set "PATH=%LOCALAPPDATA%\Programs\Python\Python313\;%LOCALAPPDATA%\Programs\Python\Python313\Scripts\;%PATH%"
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY ( python --version >nul 2>&1 && set "PY=python" )
if defined PY goto have_python
echo.
echo  ! Python install thayu pan haju dekhatu nathi. PC restart kari ne aa file fari chalavo.
pause
exit /b 1

:no_winget
echo.
echo  ! Python jate install karo (link khule chhe). Install vakhte "Add python.exe to PATH" par TICK karo.
echo    Pachhi aa Install_Karo.bat fari chalavo.
start "" "https://www.python.org/ftp/python/3.13.17/python-3.13.17-amd64.exe"
pause
exit /b 1

:have_python
for /f "tokens=*" %%v in ('%PY% --version') do echo [1/4] %%v taiyar chhe.
echo [2/4] App ni jaruri vastu install thay chhe (pehli vaar 3-5 minute)...
%PY% -m pip install --upgrade pip > "%LOG%" 2>&1
%PY% -m pip install -r requirements.txt >> "%LOG%" 2>&1
if errorlevel 1 (
  echo.
  echo  ! Install ma bhul aavi. Vigat: install_log.txt  ^(aa file Claude ne mokalo^)
  echo    Internet chalu chhe e tapaso ane aa file fari chalavo.
  pause
  exit /b 1
)
echo [3/4] Gujarati akshar ane font taiyar thay chhe...
%PY% -c "import app.winfix as w; print(w.download()[1])" >> "%LOG%" 2>&1
%PY% -c "from app import fonts; print(fonts.ensure(quiet=True))" >> "%LOG%" 2>&1
%PY% -c "import app.winfix as w; print('  Gujarati akshar:', 'OK' if w.raqm_ok() else 'NATHI - App ma Tapas thi sudharo')"

echo [4/4] Desktop par icon bane chhe...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d=[Environment]::GetFolderPath('Desktop'); $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut((Join-Path $d 'Social Auto App.lnk')); $s.TargetPath='%~dp0App_Chalu_Karo.bat'; $s.WorkingDirectory='%~dp0'; $s.IconLocation='%SystemRoot%\System32\SHELL32.dll,13'; $s.Save(); $s=$w.CreateShortcut((Join-Path $d 'Social Auto App (PC + Mobile).lnk')); $s.TargetPath='%~dp0App_PC_ane_Mobile.bat'; $s.WorkingDirectory='%~dp0'; $s.IconLocation='%SystemRoot%\System32\SHELL32.dll,17'; $s.Save()" >> "%LOG%" 2>&1
if errorlevel 1 echo  ! Desktop icon na banyo - folder mathi App_Chalu_Karo.bat chalavo.

echo.
echo ==================================================
echo   OK - Install pura!  Have Desktop par
echo   "Social Auto App" icon par double-click karo.
echo ==================================================
echo.
set /p go="Hamna j app kholvi chhe? (h = haa) : "
if /i "%go%"=="h" start "" "%~dp0App_Chalu_Karo.bat"
exit /b 0
