@echo off
echo ========================================
echo   MSProject2 SAJU - 전체 서비스 시작
echo ========================================
echo.

:: 현재 디렉토리 확인
if not exist "main-app" (
    echo [ERROR] MSProject2_SAJU 루트 디렉토리에서 실행해주세요!
    pause
    exit /b 1
)

:: 포트 사용 여부 확인
echo [INFO] 포트 사용 여부 확인 중...
netstat -an | findstr ":4000 " >nul && (
    echo [WARNING] 포트 4000이 이미 사용 중입니다!
    echo [WARNING] 기존 프로세스를 종료하고 다시 시도해주세요.
    pause
    exit /b 1
)

echo [INFO] 모든 서비스를 시작합니다...
echo [INFO] 총 6개 터미널 창이 열립니다.
echo.

:: 1. 메인 앱 (포트 4000) - Vite 버전
echo [1/6] 메인 앱 시작 중... (포트 4000) [Vite - 초고속!]
start "MSProject2-MainApp-Vite" cmd /k "cd main-app && npm install && npm start"
timeout /t 3

:: 2. SAJU 백엔드 (포트 8000)
echo [2/6] SAJU 백엔드 시작 중... (포트 8000)
start "MSProject2-SAJU-Backend" cmd /k "cd SAJU\backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000"
timeout /t 5

:: 3. SAJU 프론트엔드 (포트 3000)
echo [3/6] SAJU 프론트엔드 시작 중... (포트 3000)
start "MSProject2-SAJU-Frontend" cmd /k "cd SAJU\frontend && npm install && npm start"
timeout /t 3

:: 4. 궁합 백엔드 (포트 8002)
echo [4/6] 궁합 백엔드 시작 중... (포트 8002)
start "MSProject2-Compatibility-Backend" cmd /k "cd Compatibility\backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8002"
timeout /t 5

:: 5. 궁합 프론트엔드 (포트 3002)
echo [5/6] 궁합 프론트엔드 시작 중... (포트 3002)
start "MSProject2-Compatibility-Frontend" cmd /k "cd Compatibility\frontend && npm install && npm start"
timeout /t 3

:: 6. 관상학 서비스 (Docker 필수!)
echo [6/6] 관상학 서비스 시작 중... (포트 8001/3001)
echo [IMPORTANT] Docker Desktop이 실행 중인지 확인해주세요!
start "MSProject2-Physiognomy-Docker" cmd /k "cd Physiognomy && docker-compose up --build"

echo.
echo ========================================
echo   모든 서비스 시작 완료!
echo ========================================
echo.
echo 서비스 접속 URL:
echo   메인 허브:   http://localhost:4000
echo   사주 분석:   http://localhost:3000
echo   궁합 분석:   http://localhost:3002
echo   관상 분석:   http://localhost:3001
echo.
echo API 문서:
echo   SAJU API:    http://localhost:8000/docs
echo   궁합 API:    http://localhost:8002/docs
echo   관상 API:    http://localhost:8001/docs
echo.
echo [주의] 모든 서비스가 완전히 시작되려면 2-3분 정도 소요됩니다.
echo [주의] 관상학 서비스는 Docker 빌드로 인해 추가 시간이 필요할 수 있습니다.
echo.
pause