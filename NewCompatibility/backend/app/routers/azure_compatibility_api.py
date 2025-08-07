"""
Azure OpenAI API 라우터 - NewCompatibility 전용
궁합 분석에 특화된 Azure AI 엔드포인트
"""
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
import json
import logging
from datetime import datetime

from app.models.compatibility import CompatibilityRequest
from app.services.saju_client import saju_client
from app.services.compatibility_engine import compatibility_engine  
from app.services.azure_compatibility_ai_service import get_azure_compatibility_service

# 로깅 설정
logger = logging.getLogger(__name__)

# 라우터 생성
azure_compatibility_router = APIRouter()

class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

@azure_compatibility_router.get("/test")
async def azure_compatibility_test():
    """Azure OpenAI 궁합 AI 연결 테스트"""
    try:
        azure_service = get_azure_compatibility_service()
        test_result = await azure_service.test_connection()
        
        return UnicodeJSONResponse({
            "success": True,
            "message": "Azure OpenAI 궁합 AI 테스트 완료",
            "service": "compatibility",
            "data": test_result
        })
    except Exception as e:
        logger.error(f"Azure 궁합 AI 테스트 실패: {e}")
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "Azure OpenAI 궁합 AI 테스트 실패"
        }, status_code=500)

@azure_compatibility_router.post("/chat")
async def azure_compatibility_chat(
    request: CompatibilityRequest,
    question: str = Query(..., description="사용자 질문")
):
    """Azure AI 궁합 대화형 해석"""
    try:
        logger.info(f"Azure AI 궁합 채팅 요청: {question}")
        
        # 1. SAJU API로부터 두 사람의 사주 분석 결과 가져오기
        saju_result = await saju_client.analyze_multiple_saju(
            request.person1.dict(),
            request.person2.dict()
        )
        
        if not saju_result.get("success", False):
            return UnicodeJSONResponse({
                "success": False,
                "error": saju_result.get("error", "saju_analysis_failed"),
                "message": saju_result.get("message", "사주 분석에 실패했습니다")
            }, status_code=500)
        
        # 2. 궁합 계산 엔진으로 분석
        compatibility_result = compatibility_engine.calculate_overall_compatibility(
            saju_result["person1"],
            saju_result["person2"]
        )
        
        if not compatibility_result.get("success", False):
            return UnicodeJSONResponse({
                "success": False,
                "error": compatibility_result.get("error", "compatibility_calculation_failed"),
                "message": compatibility_result.get("message", "궁합 계산에 실패했습니다")
            }, status_code=500)
        
        # 3. Azure AI 해석을 위한 데이터 구성
        analysis_data = {
            "score": {
                "total": compatibility_result["overall_score"],
                "wuxing": compatibility_result["detailed_scores"]["love"],
                "ten_gods": compatibility_result["detailed_scores"]["communication"],
                "grade": "우수" if compatibility_result["overall_score"] >= 70 else "보통" if compatibility_result["overall_score"] >= 50 else "노력필요",
                "description": compatibility_result["summary"]
            },
            "analysis": {
                "wuxing_compatibility": f"오행 분석: {compatibility_result['detailed_scores']['love']}점",
                "ten_gods_compatibility": f"십성 분석: {compatibility_result['detailed_scores']['communication']}점",
                "overall_summary": compatibility_result["summary"]
            },
            "persons": {
                "person1": {"name": request.person1.name, "birth_date": f"{request.person1.year}년 {request.person1.month}월 {request.person1.day}일"},
                "person2": {"name": request.person2.name, "birth_date": f"{request.person2.year}년 {request.person2.month}월 {request.person2.day}일"}
            }
        }
        
        # 4. Azure AI 해석
        azure_service = get_azure_compatibility_service()
        ai_result = await azure_service.interpret_compatibility(analysis_data, question)
        
        return UnicodeJSONResponse({
            "success": True,
            "data": {
                "basic_info": {
                    "person1": f"{request.person1.name} ({request.person1.year}년생)",
                    "person2": f"{request.person2.name} ({request.person2.year}년생)",
                    "compatibility_score": compatibility_result["overall_score"]
                },
                "user_question": question,
                "ai_interpretation": ai_result,
                "provider": "azure_openai_compatibility"
            }
        })
        
    except Exception as e:
        logger.error(f"Azure AI 궁합 해석 오류: {e}")
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "Azure AI 궁합 해석 중 오류가 발생했습니다."
        }, status_code=500)

@azure_compatibility_router.post("/questions")
async def azure_compatibility_questions(request: CompatibilityRequest):
    """Azure AI 궁합 맞춤 질문 생성"""
    try:
        logger.info(f"Azure AI 궁합 질문 생성 요청")
        
        # 1. SAJU API로부터 두 사람의 사주 분석 결과 가져오기
        saju_result = await saju_client.analyze_multiple_saju(
            request.person1.dict(),
            request.person2.dict()
        )
        
        if not saju_result.get("success", False):
            return UnicodeJSONResponse({
                "success": False,
                "error": saju_result.get("error", "saju_analysis_failed"),
                "message": saju_result.get("message", "사주 분석에 실패했습니다")
            }, status_code=500)
        
        # 2. 궁합 계산 엔진으로 분석
        compatibility_result = compatibility_engine.calculate_overall_compatibility(
            saju_result["person1"],
            saju_result["person2"]
        )
        
        if not compatibility_result.get("success", False):
            return UnicodeJSONResponse({
                "success": False,
                "error": compatibility_result.get("error", "compatibility_calculation_failed"),
                "message": compatibility_result.get("message", "궁합 계산에 실패했습니다")
            }, status_code=500)
        
        # 3. Azure AI 질문 생성을 위한 데이터 구성
        analysis_data = {
            "score": {
                "total": compatibility_result["overall_score"],
                "grade": "우수" if compatibility_result["overall_score"] >= 70 else "보통" if compatibility_result["overall_score"] >= 50 else "노력필요"
            },
            "analysis": {
                "overall_summary": compatibility_result["summary"],
                "wuxing_compatibility": f"오행 궁합: {compatibility_result['detailed_scores']['love']}점",
                "ten_gods_compatibility": f"십성 궁합: {compatibility_result['detailed_scores']['communication']}점"
            },
            "persons": {
                "person1": {"name": request.person1.name},
                "person2": {"name": request.person2.name}
            }
        }
        
        # 4. 개인화된 질문 생성
        persons_info = {
            "person1": {"name": request.person1.name, "year": request.person1.year},
            "person2": {"name": request.person2.name, "year": request.person2.year}
        }
        
        azure_service = get_azure_compatibility_service()
        questions_result = await azure_service.generate_compatibility_questions(
            analysis_data,
            persons_info
        )
        
        return UnicodeJSONResponse({
            "success": True,
            "data": questions_result
        })
        
    except Exception as e:
        logger.error(f"Azure AI 궁합 질문 생성 오류: {e}")
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "Azure AI 궁합 질문 생성 중 오류가 발생했습니다."
        }, status_code=500)

@azure_compatibility_router.get("/analyze/{person1_name}/{person2_name}")
async def azure_compatibility_analyze(
    person1_name: str,
    person2_name: str,
    person1_year: int = Query(...),
    person1_month: int = Query(...),
    person1_day: int = Query(...),
    person1_hour: int = Query(...),
    person1_gender: str = Query(...),
    person2_year: int = Query(...),
    person2_month: int = Query(...),
    person2_day: int = Query(...),
    person2_hour: int = Query(...),
    person2_gender: str = Query(...)
):
    """Azure AI 궁합 분석 + 해석 (간단한 GET 방식)"""
    try:
        # CompatibilityRequest 객체 생성
        from app.models.compatibility import Person
        
        person1 = Person(
            name=person1_name,
            year=person1_year,
            month=person1_month,
            day=person1_day,
            hour=person1_hour,
            gender=person1_gender
        )
        
        person2 = Person(
            name=person2_name,
            year=person2_year,
            month=person2_month,
            day=person2_day,
            hour=person2_hour,
            gender=person2_gender
        )
        
        request = CompatibilityRequest(person1=person1, person2=person2)
        
        # 기본 질문으로 분석
        return await azure_compatibility_chat(request, "우리 둘의 궁합은 어떤가요?")
        
    except Exception as e:
        logger.error(f"Azure AI 궁합 분석 오류: {e}")
        return UnicodeJSONResponse({
            "success": False,
            "error": str(e),
            "message": "Azure AI 궁합 분석 중 오류가 발생했습니다."
        }, status_code=500)

@azure_compatibility_router.get("/info")
async def azure_compatibility_info():
    """Azure OpenAI 궁합 서비스 정보"""
    return UnicodeJSONResponse({
        "service": "Azure OpenAI 궁합 분석 AI",
        "version": "1.0.0",
        "provider": "azure_openai",
        "model": "gpt-4.1",
        "specialization": "compatibility_analysis",
        "endpoints": [
            "/test - 연결 테스트",
            "/chat - 대화형 해석",
            "/questions - 맞춤 질문 생성",
            "/analyze - 직접 분석",
            "/info - 서비스 정보"
        ],
        "features": [
            "궁합 전문 AI 해석",
            "개인화된 질문 생성",
            "관계 개선 조언",
            "실시간 대화형 상담"
        ]
    })