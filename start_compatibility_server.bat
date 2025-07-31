@echo off
echo ========================================
echo   💕 Compatibility 백엔드 서버 시작  
echo ========================================
echo 포트: 8002
echo 프로세스 구분: Compatibility Backend
echo ========================================

cd /d "C:\workspace\MSproject2_SAJU\Compatibility\backend"
title Compatibility_Backend_Server
python -m uvicorn app.main:app --reload --port 8002 --host 127.0.0.1

pause