from fastapi import APIRouter, HTTPException, Depends
from app.models.saju import (
    BirthInfoRequest, SajuAnalysisResponse, ErrorResponse,
    SajuAnalysisSimpleResponse, BasicInfo, PillarInfo, SajuPalja,
    WuxingAnalysisSimple, InterpretationsSimple
)
from app.services.saju_analyzer import saju_analyzer
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/analyze", 
    response_model=SajuAnalysisResponse,
    summary="사주팔자 분석",
    description="출생 정보를 바탕으로 사주팔자를 분석하고 종합적인 운세를 제공합니다."
)
async def analyze_saju(birth_info: BirthInfoRequest):
    """
    사주팔자 종합 분석 API
    
    - **year**: 출생년도 (1900-2100)
    - **month**: 출생월 (1-12)
    - **day**: 출생일 (1-31)
    - **hour**: 출생시간 (0-23)
    - **gender**: 성별 (male/female)
    - **name**: 이름
    """
    try:
        logger.info(f"사주 분석 요청: {birth_info.dict()}")
        
        # 입력 검증
        if birth_info.year < 1900 or birth_info.year > 2100:
            raise HTTPException(status_code=400, detail="년도는 1900-2100 사이여야 합니다.")
        
        if birth_info.month < 1 or birth_info.month > 12:
            raise HTTPException(status_code=400, detail="월은 1-12 사이여야 합니다.")
        
        if birth_info.day < 1 or birth_info.day > 31:
            raise HTTPException(status_code=400, detail="일은 1-31 사이여야 합니다.")
        
        if birth_info.hour < 0 or birth_info.hour > 23:
            raise HTTPException(status_code=400, detail="시간은 0-23 사이여야 합니다.")
        
        if birth_info.gender not in ["male", "female", "M", "F"]:
            raise HTTPException(status_code=400, detail="성별은 male 또는 female이어야 합니다.")
        
        # 사주 분석 수행
        analysis_result = saju_analyzer.analyze_saju(birth_info)
        
        logger.info("사주 분석 완료")
        return analysis_result
        
    except ValueError as ve:
        logger.error(f"데이터 오류: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"사주 분석 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다.")

@router.get(
    "/palja-only",
    summary="사주팔자만 추출",
    description="출생 정보로부터 사주팔자(四柱八字)만 추출합니다."
)
async def get_palja_only(
    year: int,
    month: int, 
    day: int,
    hour: int,
    gender: str
):
    """사주팔자만 빠르게 조회"""
    try:
        birth_info = BirthInfoRequest(
            year=year,
            month=month,
            day=day,
            hour=hour,
            gender=gender
        )
        
        palja = saju_analyzer.extract_palja(birth_info)
        return {"palja": palja.dict()}
        
    except Exception as e:
        logger.error(f"사주팔자 추출 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/wuxing-only",
    summary="오행 분석만",
    description="사주팔자의 오행 분석만 수행합니다."
)
async def get_wuxing_only(
    year: int,
    month: int,
    day: int, 
    hour: int,
    gender: str
):
    """오행 분석만 수행"""
    try:
        birth_info = BirthInfoRequest(
            year=year,
            month=month,
            day=day,
            hour=hour,
            gender=gender
        )
        
        palja = saju_analyzer.extract_palja(birth_info)
        wuxing = saju_analyzer.analyze_wuxing(palja)
        
        return {
            "palja": palja.dict(),
            "wuxing": wuxing.dict()
        }
        
    except Exception as e:
        logger.error(f"오행 분석 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test_endpoint():
    """API 테스트용 엔드포인트"""
    return {
        "message": "사주 API가 정상적으로 작동중입니다.",
        "endpoints": [
            "/analyze - 완전한 사주 분석",
            "/palja-only - 사주팔자만 추출", 
            "/wuxing-only - 오행 분석만",
            "/test - 테스트"
        ]
    }