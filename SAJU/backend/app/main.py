from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import saju

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
app.include_router(saju.router, prefix="/api/v1/saju", tags=["saju"])

@app.get("/")
async def root():
    return {"message": "사주 웹 서비스 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/test-saju")
async def test_saju_analysis():
    """테스트용 사주 분석"""
    from app.services.saju_analyzer import saju_analyzer
    from app.models.saju import BirthInfoRequest
    
    # 테스트 데이터
    test_data = BirthInfoRequest(
        year=1990, month=5, day=15, hour=14, gender="M", name="테스트"
    )
    
    # 실제 분석 수행
    result = saju_analyzer.analyze_saju(test_data)
    
    return {"message": "실제 분석기 호출 성공", "result_type": str(type(result)), "result": result}