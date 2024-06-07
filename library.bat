@echo off

set "chromePath_x64=C:\Program Files\Google\Chrome\Application"

REM Get the current PATH variable
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find /i "Path"') do set "currentPath=%%b"

REM Append the Chrome path to the current PATH variable
set "newPath_x64=%currentPath%;%chromePath_x64%"

REM Update the PATH variable in the system environment
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%newPath_x64%" /f

set "chromePath_x86=C:\Program Files (x86)\Google\Chrome\Application"

REM Get the current PATH variable
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| find /i "Path"') do set "currentPath=%%b"

REM Append the Chrome path to the current PATH variable
set "newPath_x86=%currentPath%;%chromePath_x86%"

REM Update the PATH variable in the system environment
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%newPath_x86%" /f

echo.
echo Google Chrome path has been added to the System PATH variable.
echo.
echo Installing Python Libraries...

pip install bs4
pip install requests
pip install pandas

pause