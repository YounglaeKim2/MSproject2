#!/usr/bin/env python3
"""간단한 테스트 서버"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Test server is running"}

@app.get("/api/v1/saju/test")
async def saju_test():
    return {"success": True, "message": "SAJU API is working"}

@app.post("/api/v1/saju/analyze")
async def analyze_test(data: dict):
    return {
        "success": True,
        "message": "Analysis test response",
        "basic_info": {
            "name": data.get("name", "테스트"),
            "birth_date": "테스트 날짜"
        },
        "saju_palja": {
            "year_pillar": {"stem": "甲", "branch": "子"},
            "month_pillar": {"stem": "甲", "branch": "子"},
            "day_pillar": {"stem": "甲", "branch": "子"},
            "hour_pillar": {"stem": "甲", "branch": "子"}
        }
    }

if __name__ == "__main__":
    print("Test server starting on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8002)