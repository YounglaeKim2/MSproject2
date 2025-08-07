"""
Azure OpenAI API 라우터 - 완전 독립형
기존 saju.py와 충돌 없음
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.models.saju import BirthInfoRequest
from app.services.saju_analyzer import saju_analyzer
from app.services.azure_openai_service import get_azure_service
import logging
from typing import Dict, Any
import traceback

# 로깅 설정
logger = logging.getLogger(__name__)

# 독립적인 라우터
azure_router = APIRouter()

def safe_convert_to_dict(obj) -> Any:
    """객체를 dict로 안전하게 변환 (기존 saju.py에서 복사)"""
    try:
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    result[key] = safe_convert_to_dict(value)
            return result
        elif hasattr(obj, '_asdict'):
            return {k: safe_convert_to_dict(v) for k, v in obj._asdict().items()}
        elif isinstance(obj, dict):
            return {k: safe_convert_to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [safe_convert_to_dict(item) for item in obj]
        else:
            return obj
    except Exception as e:
        logger.error(f"객체 변환 실패: {e}")
        return str(obj)


@azure_router.get("/test")
async def azure_test():
    """Azure OpenAI 연결 테스트"""
    try:
        azure_service = get_azure_service()
        result = await azure_service.test_connection()
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Azure OpenAI 테스트 실패"
        }


@azure_router.post("/chat")
async def azure_chat(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="사용자 질문")
):
    """Azure OpenAI 사주 채팅"""
    try:
        logger.info(f"Azure 채팅 요청: {question} (사용자: {birth_info.name})")
        
        # 1. 사주 분석 (기존 analyzer 사용)
        raw_result = saju_analyzer.analyze_saju(birth_info)
        saju_data = safe_convert_to_dict(raw_result)
        
        # 2. Azure OpenAI 해석
        azure_service = get_azure_service()
        ai_result = await azure_service.interpret_saju(saju_data, question)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                    "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성"
                },
                "user_question": question,
                "ai_interpretation": ai_result,
                "provider": "azure_openai"
            }
        }
        
    except Exception as e:
        logger.error(f"Azure 채팅 오류: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Azure 채팅 실패: {str(e)}")


@azure_router.post("/questions")
async def azure_questions(birth_info: BirthInfoRequest):
    """Azure OpenAI 개인화된 질문 생성"""
    try:
        logger.info(f"Azure 질문 생성 요청: {birth_info.name}")
        
        # 1. 사주 분석
        raw_result = saju_analyzer.analyze_saju(birth_info)
        saju_data = safe_convert_to_dict(raw_result)
        
        # 2. Azure OpenAI 질문 생성
        azure_service = get_azure_service()
        questions_result = await azure_service.generate_questions(saju_data, birth_info.dict())
        
        return {
            "success": True,
            "data": questions_result
        }
        
    except Exception as e:
        logger.error(f"Azure 질문 생성 오류: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Azure 질문 생성 실패: {str(e)}")


@azure_router.post("/analyze")
async def azure_analyze(birth_info: BirthInfoRequest):
    """Azure OpenAI 통합 사주 분석 (기존 analyze + Azure AI 해석)"""
    try:
        logger.info(f"Azure 통합 분석 요청: {birth_info.name}")
        
        # 1. 기본 사주 분석
        raw_result = saju_analyzer.analyze_saju(birth_info)
        saju_data = safe_convert_to_dict(raw_result)
        
        # 2. 기본 질문으로 AI 해석 추가
        azure_service = get_azure_service()
        default_question = "전반적인 사주 해석을 해주세요"
        ai_interpretation = await azure_service.interpret_saju(saju_data, default_question)
        
        # 3. 개인화된 질문도 생성
        suggested_questions = await azure_service.generate_questions(saju_data, birth_info.dict())
        
        # 4. 기존 형식과 유사하게 구성
        response_data = {
            "basic_info": {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성"
            },
            
            # 기본 사주 데이터 (기존 형식 유지)
            "saju_palja": saju_data.get('palja', {}),
            "wuxing_analysis": saju_data.get('wuxing', {}),
            
            # 해석 데이터
            "interpretations": {
                "personality": saju_data.get('personality', {}).get('basic_nature', ''),
                "career": saju_data.get('career', {}).get('career_tendency', ''),
                "health": saju_data.get('health', {}).get('health_advice', []),
                "relationships": saju_data.get('relationship', {}).get('relationship_style', ''),
                "wealth": saju_data.get('fortune', {}).get('wealth_potential', '')
            },
            
            # Azure AI 추가 기능
            "azure_ai": {
                "interpretation": ai_interpretation,
                "suggested_questions": suggested_questions.get('suggested_questions', [])
            },
            
            "provider": "azure_openai",
            "enhanced": True
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"Azure 통합 분석 오류: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Azure 통합 분석 실패: {str(e)}")


@azure_router.get("/info")
async def azure_info():
    """Azure OpenAI 서비스 정보"""
    return {
        "service": "Azure OpenAI for SAJU",
        "model": "GPT-4.1",
        "provider": "Microsoft Azure",
        "features": [
            "사주 해석",
            "개인화된 질문 생성", 
            "통합 분석",
            "실시간 채팅"
        ],
        "endpoints": [
            "/azure/test - 연결 테스트",
            "/azure/chat - AI 채팅",
            "/azure/questions - 질문 생성",
            "/azure/analyze - 통합 분석",
            "/azure/info - 서비스 정보"
        ]
    }