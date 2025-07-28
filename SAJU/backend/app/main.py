from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import saju_simple

app = FastAPI(
    title="사주 웹 서비스 API",
    description="사주팔자 분석 및 해석 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(saju_simple.router, prefix="/api/v1/saju", tags=["saju"])

@app.get("/")
async def root():
    return {"message": "사주 웹 서비스 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}