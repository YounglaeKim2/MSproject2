"""
새로운 궁합 서비스 - SAJU API 기반
- 기존 SAJU API를 활용한 궁합 분석
- 완전히 독립적인 마이크로서비스
- 포트 8003 사용
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import logging
from datetime import datetime

from app.models.compatibility import (
    HealthCheckResponse, 
    ServiceInfoResponse, 
    CompatibilityRequest,
    CompatibilityAnalysisResponse,
    CompatibilityScore,
    CompatibilityDetail
)
from app.services.saju_client import saju_client
from app.services.compatibility_engine import compatibility_engine
from app.services.compatibility_ai_interpreter import get_compatibility_ai_interpreter

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

app = FastAPI(
    title="새로운 궁합 분석 서비스",
    description="SAJU API 기반 궁합 분석 서비스 - 완전히 새로운 구현",
    version="1.0.0",
    default_response_class=UnicodeJSONResponse
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3003",  # 새 궁합 프론트엔드
        "http://localhost:3000",  # SAJU 프론트엔드 (호환성)
        "http://localhost:4000",  # 랜딩 페이지
        "*",  # 개발 중 모든 origins 허용
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "새로운 궁합 분석 서비스",
        "version": "1.0.0",
        "description": "SAJU API 기반 궁합 분석",
        "status": "Phase 2 완료 - SAJU API 클라이언트 구현",
        "saju_api": "http://localhost:8000",
        "created": "2025-08-06",
        "endpoints": [
            "/",
            "/health", 
            "/info",
            "/api/v1/compatibility/test",
            "/api/v1/compatibility/analyze",
            "/api/v1/compatibility/ai-chat",
            "/api/v1/compatibility/suggested-questions",
            "/api/v1/compatibility/ai-test"
        ]
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """헬스 체크 엔드포인트 (SAJU API 연결 상태 포함)"""
    try:
        # SAJU API 연결 상태 확인
        saju_health = await saju_client.check_health()
        
        return HealthCheckResponse(
            status="healthy" if saju_health.get("status") == "healthy" else "degraded",
            timestamp=datetime.now().isoformat(),
            dependencies={
                "saju_api": saju_health
            }
        )
    except Exception as e:
        logger.error(f"헬스 체크 실패: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            dependencies={
                "saju_api": {"status": "error", "error": str(e)}
            }
        )

@app.get("/info", response_model=ServiceInfoResponse)
async def service_info():
    """서비스 정보 엔드포인트"""
    return ServiceInfoResponse(
        endpoints=[
            "/",
            "/health", 
            "/info",
            "/api/v1/compatibility/test",
            "/api/v1/compatibility/analyze"
        ],
        dependencies={
            "SAJU_API": "http://localhost:8000",
            "FastAPI": "0.104.1",
            "Python": "3.8+"
        }
    )

@app.post("/api/v1/compatibility/test", response_model=CompatibilityAnalysisResponse)
async def test_saju_connection(request: CompatibilityRequest):
    """SAJU API 연결 테스트용 엔드포인트"""
    try:
        logger.info("SAJU API 연결 테스트 시작")
        
        # 두 사람의 사주 분석 요청
        result = await saju_client.analyze_multiple_saju(
            request.person1.dict(),
            request.person2.dict()
        )
        
        if not result.get("success", False):
            return CompatibilityAnalysisResponse(
                success=False,
                error=result.get("error", "unknown_error"),
                message=result.get("message", "SAJU API 호출에 실패했습니다")
            )
        
        # 테스트 성공 응답
        return CompatibilityAnalysisResponse(
            success=True,
            person1_name=request.person1.name,
            person2_name=request.person2.name,
            summary=f"SAJU API 연결 테스트 성공! {request.person1.name}님과 {request.person2.name}님의 사주 데이터를 성공적으로 받아왔습니다.",
            detailed_analysis="이것은 연결 테스트입니다. 실제 궁합 분석은 /api/v1/compatibility/analyze 엔드포인트를 사용하세요.",
            analysis_time=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"SAJU API 연결 테스트 실패: {e}")
        return CompatibilityAnalysisResponse(
            success=False,
            error="test_failed",
            message=f"SAJU API 연결 테스트 중 오류가 발생했습니다: {str(e)}"
        )

@app.post("/api/v1/compatibility/analyze", response_model=CompatibilityAnalysisResponse)
async def analyze_compatibility(request: CompatibilityRequest):
    """실제 궁합 분석 엔드포인트"""
    try:
        logger.info(f"궁합 분석 시작: {request.person1.name} & {request.person2.name}")
        
        # 1. SAJU API로부터 두 사람의 사주 분석 결과 가져오기
        saju_result = await saju_client.analyze_multiple_saju(
            request.person1.dict(),
            request.person2.dict()
        )
        
        if not saju_result.get("success", False):
            return CompatibilityAnalysisResponse(
                success=False,
                error=saju_result.get("error", "saju_analysis_failed"),
                message=saju_result.get("message", "사주 분석에 실패했습니다")
            )
        
        # 2. 궁합 계산 엔진으로 분석
        compatibility_result = compatibility_engine.calculate_overall_compatibility(
            saju_result["person1"],
            saju_result["person2"]
        )
        
        if not compatibility_result.get("success", False):
            return CompatibilityAnalysisResponse(
                success=False,
                error=compatibility_result.get("error", "compatibility_calculation_failed"),
                message=compatibility_result.get("message", "궁합 계산에 실패했습니다")
            )
        
        # 3. 응답 구성
        return CompatibilityAnalysisResponse(
            success=True,
            person1_name=request.person1.name,
            person2_name=request.person2.name,
            compatibility_score=CompatibilityScore(
                overall=compatibility_result["overall_score"],
                love=compatibility_result["detailed_scores"]["love"],
                marriage=compatibility_result["detailed_scores"]["marriage"],
                communication=compatibility_result["detailed_scores"]["communication"],
                values=compatibility_result["detailed_scores"]["values"]
            ),
            analysis_details=CompatibilityDetail(
                strengths=compatibility_result["strengths"],
                weaknesses=compatibility_result["weaknesses"],
                advice=compatibility_result["advice"],
                relationship_tips=[
                    "정기적인 소통 시간을 가지세요",
                    "서로의 관심사를 존중하고 지지하세요",
                    "갈등이 생겼을 때는 차분하게 대화로 해결하세요",
                    "감사의 마음을 자주 표현하세요"
                ]
            ),
            summary=compatibility_result["summary"],
            detailed_analysis=f"""
            🌟 오행 분석 (점수: {compatibility_result['wuxing_analysis']['score']}점)
            {compatibility_result['wuxing_analysis']['analysis']}
            
            🎭 십성 분석 (점수: {compatibility_result['sibseong_analysis']['score']}점)  
            {compatibility_result['sibseong_analysis']['analysis']}
            
            💫 종합 평가
            전체적으로 {compatibility_result['overall_score']}점의 궁합을 보여주며, 
            {"매우 좋은" if compatibility_result['overall_score'] >= 70 else "보통의" if compatibility_result['overall_score'] >= 50 else "노력이 필요한"} 관계입니다.
            """,
            analysis_time=compatibility_result["analysis_time"]
        )
        
    except Exception as e:
        logger.error(f"궁합 분석 실패: {e}")
        return CompatibilityAnalysisResponse(
            success=False,
            error="analysis_failed",
            message=f"궁합 분석 중 예상치 못한 오류가 발생했습니다: {str(e)}"
        )

# AI 채팅 엔드포인트
@app.post("/api/v1/compatibility/ai-chat")
async def ai_chat_compatibility(
    request: CompatibilityRequest,
    question: str = Query(..., description="사용자 질문")
):
    """AI 대화형 궁합 해석"""
    try:
        logger.info(f"AI 궁합 채팅 요청: {question}")
        
        # 1. 궁합 분석 실행
        compatibility_result = await analyze_compatibility(request)
        
        if not compatibility_result.success:
            return UnicodeJSONResponse({
                "success": False,
                "error": compatibility_result.error,
                "message": compatibility_result.message
            }, status_code=500)
        
        # 2. AI 해석을 위한 데이터 구성
        analysis_data = {
            "score": {
                "total": compatibility_result.compatibility_score.overall,
                "wuxing": (compatibility_result.compatibility_score.love + compatibility_result.compatibility_score.marriage) // 2,
                "ten_gods": (compatibility_result.compatibility_score.communication + compatibility_result.compatibility_score.values) // 2,
                "grade": "우수" if compatibility_result.compatibility_score.overall >= 70 else "보통" if compatibility_result.compatibility_score.overall >= 50 else "노력필요",
                "description": compatibility_result.summary
            },
            "analysis": {
                "wuxing_compatibility": f"오행 분석: {compatibility_result.compatibility_score.love}점",
                "ten_gods_compatibility": f"십성 분석: {compatibility_result.compatibility_score.communication}점",
                "overall_summary": compatibility_result.summary
            },
            "persons": {
                "person1": {"name": request.person1.name, "birth_date": f"{request.person1.year}년 {request.person1.month}월 {request.person1.day}일"},
                "person2": {"name": request.person2.name, "birth_date": f"{request.person2.year}년 {request.person2.month}월 {request.person2.day}일"}
            }
        }
        
        # 3. AI 해석
        ai_interpreter = get_compatibility_ai_interpreter()
        ai_result = await ai_interpreter.interpret_compatibility(
            analysis_data, 
            question,
            None  # context
        )
        
        return UnicodeJSONResponse({
            "success": True,
            "data": {
                "basic_info": {
                    "person1": f"{request.person1.name} ({request.person1.year}년생)",
                    "person2": f"{request.person2.name} ({request.person2.year}년생)"
                },
                "user_question": question,
                "ai_interpretation": ai_result
            }
        })
        
    except Exception as e:
        logger.error(f"AI 궁합 해석 오류: {e}")
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "AI 해석 중 오류가 발생했습니다."
        }, status_code=500)

# AI 질문 생성 엔드포인트
@app.post("/api/v1/compatibility/suggested-questions")
async def generate_suggested_questions(
    request: CompatibilityRequest,
    method: str = Query("ai", description="질문 생성 방식: ai|fallback")
):
    """궁합 분석 결과 기반 개인화된 예상 질문 생성"""
    try:
        logger.info(f"AI 질문 생성 요청 (방식: {method})")
        
        # 1. 궁합 분석 실행
        compatibility_result = await analyze_compatibility(request)
        
        if not compatibility_result.success:
            return UnicodeJSONResponse({
                "success": False,
                "error": compatibility_result.error,
                "message": compatibility_result.message
            }, status_code=500)
        
        # 2. AI 해석을 위한 데이터 구성
        analysis_data = {
            "score": {
                "total": compatibility_result.compatibility_score.overall,
                "grade": "우수" if compatibility_result.compatibility_score.overall >= 70 else "보통" if compatibility_result.compatibility_score.overall >= 50 else "노력필요"
            },
            "analysis": {
                "overall_summary": compatibility_result.summary,
                "wuxing_compatibility": f"오행 궁합: {compatibility_result.compatibility_score.love}점",
                "ten_gods_compatibility": f"십성 궁합: {compatibility_result.compatibility_score.communication}점"
            }
        }
        
        # 3. 개인화된 질문 생성
        ai_interpreter = get_compatibility_ai_interpreter()
        
        if method == "ai":
            persons_info = {
                "person1": {"name": request.person1.name, "year": request.person1.year},
                "person2": {"name": request.person2.name, "year": request.person2.year}
            }
            questions_result = await ai_interpreter.generate_suggested_questions(
                analysis_data,
                persons_info
            )
        else:
            # 폴백 질문 사용
            questions_result = {
                "suggested_questions": ai_interpreter._get_fallback_questions(),
                "generation_method": "fallback"
            }
        
        return UnicodeJSONResponse({
            "success": True,
            "data": questions_result
        })
        
    except Exception as e:
        logger.error(f"질문 생성 오류: {e}")
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "질문 생성 중 오류가 발생했습니다."
        }, status_code=500)

# AI 연결 테스트 엔드포인트
@app.get("/api/v1/compatibility/ai-test")
async def test_ai_connection():
    """AI 연결 테스트"""
    try:
        ai_interpreter = get_compatibility_ai_interpreter()
        test_result = await ai_interpreter.test_connection()
        return UnicodeJSONResponse(test_result)
    except Exception as e:
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "AI 연결 테스트 실패"
        }, status_code=500)

@app.get("/info")
async def service_info():
    return {
        "name": "새로운 궁합 분석 서비스",
        "version": "1.0.0",
        "description": "기존 SAJU API를 활용한 완전히 새로운 궁합 분석 서비스",
        "features": [
            "SAJU API 기반 개인 사주 분석",
            "두 사람의 궁합 분석",
            "오행 상생상극 분석",
            "십성 배합 분석",
            "종합 궁합 점수",
            "AI 기반 해석 (향후 추가)"
        ],
        "architecture": {
            "type": "마이크로서비스",
            "dependencies": ["SAJU API (포트 8000)"],
            "independence": "완전 독립 실행",
            "ports": {
                "backend": 8003,
                "frontend": 3003
            }
        },
        "development": {
            "phase": "Phase 1 - 구조 생성 완료",
            "next": "Phase 2 - SAJU API 클라이언트 구현",
            "created": "2025-08-06"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003, reload=True)
