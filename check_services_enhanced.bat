@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   MSProject2 SAJU Service Status Check v2.0
echo ==========================================
echo Real-time Service Monitoring
echo %date% %time%
echo.

:: Color settings (Windows 10+)
:: Green = 92, Red = 91, Yellow = 93, Blue = 94, Cyan = 96

set "services[0]=Landing Page:4000:http://localhost:4000"
set "services[1]=SAJU Backend:8000:http://localhost:8000/health"
set "services[2]=SAJU Frontend:3000:http://localhost:3000"
set "services[3]=Mobile App:8082:http://localhost:8082"
set "services[4]=Compatibility Backend:8002:http://localhost:8002/health"
set "services[5]=Compatibility Frontend:3002:http://localhost:3002"
set "services[6]=Physiognomy Backend:8001:http://localhost:8001/docs"
set "services[7]=Physiognomy Frontend:3001:http://localhost:3001"

echo ==============================================
echo            Checking Port Status...
echo ==============================================

for /l %%i in (0,1,7) do (
    call :check_service "!services[%%i]!"
)

echo.
echo ==============================================
echo          Real-time HTTP Response Check...
echo ==============================================

:: HTTP status check using curl (if curl is installed)
where curl >nul 2>&1
if %errorlevel%==0 (
    echo [INFO] HTTP status check using curl...
    
    call :http_check "Landing Page" "http://localhost:4000"
    call :http_check "SAJU API" "http://localhost:8000/health"
    call :http_check "Compatibility API" "http://localhost:8002/health"
    call :http_check "Physiognomy API" "http://localhost:8001/docs"
) else (
    echo [WARNING] curl not installed, skipping HTTP status check.
    echo [TIP] curl is pre-installed on Windows 10+.
)

echo.
echo ==============================================
echo              Overall Status Summary
echo ==============================================

echo Service Access URLs:
echo   Main Landing:   http://localhost:4000 (Real-time Monitoring)
echo   SAJU Analysis:  http://localhost:3000
echo   Mobile App:     http://localhost:8082
echo   Compatibility: http://localhost:3002
echo   Physiognomy:   http://localhost:3001

echo.
echo API Documentation:
echo   SAJU API:    http://localhost:8000/docs
echo   Compatibility API: http://localhost:8002/docs
echo   Physiognomy API:   http://localhost:8001/docs

echo.
echo Recommendations:
echo   - Check real-time status on Landing Page (localhost:4000)
echo   - For problematic services, check logs: ./logs/
echo   - Full restart: stop_all_enhanced.bat then start_all_enhanced.bat

pause
goto :eof

:: Function: Port status check
:check_service
set "info=%~1"
for /f "tokens=1,2,3 delims=:" %%a in ("!info!") do (
    set "name=%%a"
    set "port=%%b"
    set "url=%%c"
)

:: Check if port is in use
netstat -an | find ":!port!" | find "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [✅] !name! ^(Port !port!^) - Running
) else (
    echo [❌] !name! ^(Port !port!^) - Stopped
)
goto :eof

:: Function: HTTP status check
:http_check
set "service_name=%~1"
set "url=%~2"

curl -s -o nul -w "%%{http_code}" --connect-timeout 3 "%url%" >temp_status.txt 2>nul
if %errorlevel%==0 (
    set /p status_code=<temp_status.txt
    if "!status_code!"=="200" (
        echo [✅] %service_name% - HTTP 200 OK
    ) else if "!status_code!"=="000" (
        echo [❌] %service_name% - Connection Failed
    ) else (
        echo [⚠️] %service_name% - HTTP !status_code!
    )
) else (
    echo [❌] %service_name% - No Response
)

if exist temp_status.txt del temp_status.txt
goto :eof
