@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   MSProject2 SAJU Platform Stop v2.0
echo ==========================================
echo Cleaning up all services...
echo Date: %date% %time%
echo.

echo ==============================================
echo          Port-based Process Cleanup...
echo ==============================================

:: Port-based process termination
set ports=4000 3000 8000 8082 3002 8002 3001 8001
set services=Landing SAJU-Frontend SAJU-Backend MobileApp Compatibility-Frontend Compatibility-Backend Physiognomy-Frontend Physiognomy-Backend

echo [CLEANUP] Cleaning port-based processes...

:: Kill processes on each port
for %%p in (%ports%) do (
    echo [INFO] Checking port %%p processes...
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":%%p" ^| find "LISTENING"') do (
        echo [KILL] Port %%p - Terminating PID %%a...
        taskkill /f /pid %%a >nul 2>&1
    )
)

echo.
echo ==============================================
echo           Remaining Process Cleanup...
echo ==============================================

:: Node.js related process cleanup
echo [CLEANUP] Node.js related processes...
taskkill /f /im node.exe >nul 2>&1
if %errorlevel%==0 (
    echo [SUCCESS] Node.js processes cleaned
) else (
    echo [INFO] No Node.js processes to clean
)

:: Python related process cleanup
echo [CLEANUP] Python web server processes...
taskkill /f /im python.exe >nul 2>&1
if %errorlevel%==0 (
    echo [SUCCESS] Python processes cleaned
) else (
    echo [INFO] No Python processes to clean
)

:: CMD windows cleanup (service related)
echo [CLEANUP] Service CMD windows cleanup...
tasklist /fi "imagename eq cmd.exe" /fo csv | find /v "PID" > temp_cmds.txt
for /f "tokens=2 delims=," %%i in (temp_cmds.txt) do (
    set pid=%%~i
    wmic process where "ProcessId=!pid!" get commandline /format:list | find "uvicorn" >nul
    if !errorlevel!==0 (
        echo [KILL] Service CMD window ^(PID: !pid!^) terminating...
        taskkill /f /pid !pid! >nul 2>&1
    )
)
if exist temp_cmds.txt del temp_cmds.txt >nul 2>&1

echo.
echo ==============================================
echo             Log File Cleanup Option...
echo ==============================================

if exist "logs" (
    echo [OPTION] Log files found:
    dir logs /b
    echo.
    set /p response="Delete log files? (y/N): "
    if /i "!response!"=="y" (
        del /q logs\* >nul 2>&1
        echo [SUCCESS] Log files deleted
    ) else (
        echo [INFO] Log files preserved (./logs/)
    )
) else (
    echo [INFO] No log files to delete
)

echo.
echo ==========================================
echo    MSProject2 SAJU Platform Stop Complete!
echo ==========================================
echo.
echo Cleanup Summary:
echo   - All service processes terminated
echo   - 8 ports (4000,3000,8000,8082,3002,8002,3001,8001) cleaned
echo   - Node.js/Python remaining processes cleaned
echo   - Service CMD windows cleaned
echo.
echo Next start: start_all_enhanced.bat
echo Quick restart: stop_all_enhanced.bat then start_all_enhanced.bat

pause
