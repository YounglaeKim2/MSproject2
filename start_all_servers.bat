@echo off
echo ========================================  
echo   🚀 MSProject2 SAJU 전체 서버 시작
echo ========================================
echo.

echo [1/3] 🔮 SAJU 백엔드 시작 중... (포트 8000)
start "SAJU_Backend" cmd /k "cd /d C:\workspace\MSproject2_SAJU\SAJU\backend && python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1"

timeout /t 3 /nobreak >nul

echo [2/3] 💕 Compatibility 백엔드 시작 중... (포트 8002)  
start "Compatibility_Backend" cmd /k "cd /d C:\workspace\MSproject2_SAJU\Compatibility\backend && python -m uvicorn app.main:app --reload --port 8002 --host 127.0.0.1"

timeout /t 3 /nobreak >nul

echo [3/3] 🌐 Main App 프론트엔드 시작 중... (포트 4000)
start "Main_Frontend" cmd /k "cd /d C:\workspace\MSproject2_SAJU\main-app && npm start"

echo.
echo ========================================
echo   ✅ 모든 서버가 시작되었습니다!
echo ========================================
echo 🔮 SAJU API:          http://localhost:8000
echo 💕 Compatibility API: http://localhost:8002  
echo 🌐 Main App:          http://localhost:4000
echo ========================================
echo.
echo 서버를 종료하려면 각 창을 닫거나 Ctrl+C를 누르세요.
pause