@echo off
echo ========================================
echo   MSProject2 SAJU - 서비스 상태 확인
echo ========================================
echo.

:: 포트별 서비스 상태 확인
echo [서비스 상태 확인]

:: 메인 앱 (포트 4000)
netstat -an | findstr ":4000 " >nul && (
    echo   메인 앱 (4000):     ✅ 실행 중
) || (
    echo   메인 앱 (4000):     ❌ 중지됨
)

:: SAJU 프론트엔드 (포트 3000)
netstat -an | findstr ":3000 " >nul && (
    echo   사주 UI (3000):     ✅ 실행 중
) || (
    echo   사주 UI (3000):     ❌ 중지됨
)

:: 궁합 프론트엔드 (포트 3002)
netstat -an | findstr ":3002 " >nul && (
    echo   궁합 UI (3002):     ✅ 실행 중
) || (
    echo   궁합 UI (3002):     ❌ 중지됨
)

:: 관상 프론트엔드 (포트 3001)
netstat -an | findstr ":3001 " >nul && (
    echo   관상 UI (3001):     ✅ 실행 중
) || (
    echo   관상 UI (3001):     ❌ 중지됨
)

:: SAJU 백엔드 (포트 8000)
netstat -an | findstr ":8000 " >nul && (
    echo   사주 API (8000):    ✅ 실행 중
) || (
    echo   사주 API (8000):    ❌ 중지됨
)

:: 궁합 백엔드 (포트 8002)
netstat -an | findstr ":8002 " >nul && (
    echo   궁합 API (8002):    ✅ 실행 중
) || (
    echo   궁합 API (8002):    ❌ 중지됨
)

:: 관상 백엔드 (포트 8001)
netstat -an | findstr ":8001 " >nul && (
    echo   관상 API (8001):    ✅ 실행 중
) || (
    echo   관상 API (8001):    ❌ 중지됨
)

echo.
echo [Docker 컨테이너 상태]
docker ps --format "table {{.Names}}\t{{.Status}}" --filter "name=physiognomy" 2>nul || (
    echo   관상학 컨테이너:       ❌ Docker 미실행 또는 컨테이너 없음
)

echo.
echo [접속 URL 테스트]
echo   테스트를 시작합니다... (5초 정도 소요)

:: URL 접속 테스트 (curl 대신 powershell 사용)
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:4000' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   메인 허브:         ✅ http://localhost:4000' } else { Write-Host '   메인 허브:         ❌ 응답 오류' } } catch { Write-Host '   메인 허브:         ❌ 연결 실패' }" 2>nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   사주 분석:         ✅ http://localhost:3000' } else { Write-Host '   사주 분석:         ❌ 응답 오류' } } catch { Write-Host '   사주 분석:         ❌ 연결 실패' }" 2>nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3002' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   궁합 분석:         ✅ http://localhost:3002' } else { Write-Host '   궁합 분석:         ❌ 응답 오류' } } catch { Write-Host '   궁합 분석:         ❌ 연결 실패' }" 2>nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3001' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   관상 분석:         ✅ http://localhost:3001' } else { Write-Host '   관상 분석:         ❌ 응답 오류' } } catch { Write-Host '   관상 분석:         ❌ 연결 실패' }" 2>nul

echo.
echo [API 상태 확인]
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   사주 API:          ✅ http://localhost:8000/docs' } else { Write-Host '   사주 API:          ❌ 응답 오류' } } catch { Write-Host '   사주 API:          ❌ 연결 실패' }" 2>nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8002/health' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   궁합 API:          ✅ http://localhost:8002/docs' } else { Write-Host '   궁합 API:          ❌ 응답 오료' } } catch { Write-Host '   궁합 API:          ❌ 연결 실패' }" 2>nul

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8001/docs' -TimeoutSec 3 -UseBasicParsing; if($response.StatusCode -eq 200) { Write-Host '   관상 API:          ✅ http://localhost:8001/docs' } else { Write-Host '   관상 API:          ❌ 응답 오류' } } catch { Write-Host '   관상 API:          ❌ 연결 실패' }" 2>nul

echo.
echo ========================================
echo   상태 확인 완료!
echo ========================================
echo.
echo [도움말]
echo   - 서비스 시작: start_all.bat
echo   - 서비스 중지: stop_all.bat
echo   - 개별 재시작: 해당 터미널에서 Ctrl+C 후 재실행
echo.
pause