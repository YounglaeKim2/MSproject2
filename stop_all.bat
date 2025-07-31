@echo off
echo ========================================
echo   MSProject2 SAJU - 전체 서비스 중지
echo ========================================
echo.

echo [INFO] 모든 관련 프로세스를 찾아서 종료합니다...
echo.

:: Node.js 프로세스 종료 (포트 기준)
echo [1/4] Node.js 서비스 종료 중...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":4000 "') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000 "') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3002 "') do taskkill /PID %%a /F >nul 2>&1

:: Python/FastAPI 프로세스 종료
echo [2/4] Python/FastAPI 서비스 종료 중...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8002 "') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001 "') do taskkill /PID %%a /F >nul 2>&1

:: Docker 컨테이너 정리
echo [3/4] Docker 컨테이너 정리 중...
cd Physiognomy >nul 2>&1 && docker-compose down >nul 2>&1
cd .. >nul 2>&1

:: 프로세스 이름으로 추가 정리
echo [4/4] 추가 프로세스 정리 중...
taskkill /IM "node.exe" /F >nul 2>&1
taskkill /IM "python.exe" /F >nul 2>&1
taskkill /IM "uvicorn.exe" /F >nul 2>&1

:: 잠시 대기
timeout /t 2 >nul

:: 포트 사용 여부 최종 확인
echo.
echo [INFO] 포트 사용 여부 최종 확인:
for %%p in (4000 3000 3002 8000 8002 8001) do (
    netstat -an | findstr ":%%p " >nul && (
        echo   포트 %%p: 아직 사용 중
    ) || (
        echo   포트 %%p: 정리 완료
    )
)

echo.
echo ========================================
echo   모든 서비스 중지 완료!
echo ========================================
echo.
echo [INFO] 모든 포트가 정리되었습니다.
echo [INFO] 필요 시 다시 ./start_all.bat을 실행하세요.
echo.
pause