#!/usr/bin/env python3
"""
Compatibility 백엔드 서버 시작 스크립트  
프로세스 이름: python_compatibility
"""
import sys
import os

# 프로세스 이름 변경
try:
    import setproctitle
    setproctitle.setproctitle("python_compatibility")
    print("프로세스 이름을 'python_compatibility'로 변경했습니다.")
except ImportError:
    print("setproctitle 라이브러리가 없습니다. pip install setproctitle로 설치하세요.")
    print("기본 python.exe로 실행됩니다.")

# uvicorn 실행
if __name__ == "__main__":
    import uvicorn
    
    print("💕 Compatibility 백엔드 서버 시작 중...")
    print("📍 포트: 8002")
    print("🌐 CORS: localhost:3002, 4000, 4001")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8002,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )