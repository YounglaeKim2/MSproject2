#!/usr/bin/env python3
import uvicorn
import os
import sys

# 환경변수 설정
os.environ['PYTHONIOENCODING'] = 'utf-8'

if __name__ == "__main__":
    print("SAJU Backend Starting on port 8000...")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1", 
        port=8000,
        reload=True,
        log_level="info"
    )