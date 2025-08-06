@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo    MSProject2 SAJU Platform Start v2.0
echo ==========================================
echo 6 Microservices + Real-time Monitoring
echo Enhanced Integrated Execution Script (Windows)
echo %date% %time%
echo.

:: Check current directory
if not exist "landing" (
    echo [ERROR] Please run from MSProject2 root directory!
    echo [INFO] Required folders: landing, SAJU, NewCompatibility, Physiognomy, AppService
    pause
    exit /b 1
)

:: Create log directory
if not exist "logs" mkdir logs
echo [INFO] Log directory created: ./logs/

echo.
echo ==============================================
echo               Starting Services...
echo ==============================================

:: 1. Landing Page Start (Port 4000)
echo [1/6] Landing Page starting... (Port 4000)
cd landing
start "Landing Page" cmd /c "python server.py > ../logs/landing.log 2>&1"
cd ..
timeout /t 2 /nobreak >nul

:: 2. SAJU Backend Start (Port 8000)
echo [2/6] SAJU Backend starting... (Port 8000)
cd SAJU\backend
pip install -r requirements.txt > ..\..\logs\saju-backend-install.log 2>&1
start "SAJU Backend" cmd /c "python -m app.main > ../../logs/saju-backend.log 2>&1"
cd ..\..
timeout /t 3 /nobreak >nul

:: 3. SAJU Frontend Start (Port 3000)
echo [3/6] SAJU Frontend starting... (Port 3000)
cd SAJU\frontend
npm install > ..\..\logs\saju-frontend-install.log 2>&1
start "SAJU Frontend" cmd /c "npm start > ../../logs/saju-frontend.log 2>&1"
cd ..\..
timeout /t 5 /nobreak >nul

:: 4. Mobile App Start (Port 8082)
echo [4/6] Mobile App starting... (Port 8082)
cd AppService\FortuneApp
npm install > ..\..\logs\mobile-app-install.log 2>&1
start "Mobile App" cmd /c "npx expo start --port 8082 --tunnel > ../../logs/mobile-app.log 2>&1"
cd ..\..
timeout /t 3 /nobreak >nul

:: 5. NewCompatibility Service Start
echo [5/6] NewCompatibility Service starting... (Port 8003, 3003)
cd NewCompatibility
start "NewCompatibility Backend" cmd /c "start_new_compatibility.bat > ../logs/newcompat-backend.log 2>&1"
start "NewCompatibility Frontend" cmd /c "start_frontend.bat > ../logs/newcompat-frontend.log 2>&1"
cd ..
timeout /t 3 /nobreak >nul

:: 6. Physiognomy Service Start
echo [6/6] Physiognomy Service starting... (Port 8001, 3001)
cd Physiognomy\backend
pip install -r requirements.txt > ..\..\logs\physiognomy-backend-install.log 2>&1
start "Physiognomy Backend" cmd /c "python main.py > ../../logs/physiognomy-backend.log 2>&1"
cd ..\frontend
npm install > ..\..\logs\physiognomy-frontend-install.log 2>&1
start "Physiognomy Frontend" cmd /c "npm start > ../../logs/physiognomy-frontend.log 2>&1"
cd ..\..

echo [6/6] Waiting for services to start... (30 seconds)
timeout /t 30 /nobreak >nul

echo.
echo ==========================================
echo    MSProject2 SAJU Platform Started!
echo ==========================================
echo.
echo Main Landing:   http://localhost:4000 (Real-time Monitoring)
echo SAJU Analysis:  http://localhost:3000
echo Mobile App:     http://localhost:8082
echo NewCompatibility: http://localhost:3003
echo Physiognomy:   http://localhost:3001
echo.
echo API Documentation:
echo   - SAJU API:         http://localhost:8000/docs
echo   - NewCompatibility: http://localhost:8003/docs
echo   - Physiognomy:      http://localhost:8001/docs
echo.
echo Monitoring:
echo   - Real-time Status: Check on Landing Page
echo   - Log Files:        ./logs/*.log
echo   - Stop Services:    stop_all_enhanced.bat
echo.
echo All services started successfully!
echo Check real-time service status on Landing Page (localhost:4000)!
echo.

:: Auto open landing page
echo Opening landing page automatically...
timeout /t 3 /nobreak >nul
start "" "http://localhost:4000"

pause
