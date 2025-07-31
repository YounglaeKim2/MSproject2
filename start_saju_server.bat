@echo off
echo ========================================
echo   🔮 SAJU 백엔드 서버 시작
echo ========================================
echo 포트: 8000
echo 프로세스 구분: SAJU Backend
echo ========================================

cd /d "C:\workspace\MSproject2_SAJU\SAJU\backend"
title SAJU_Backend_Server
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1

pause