from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
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
        logger.info(f"=== 새로운 사주 분석 요청 시작 ===")
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
        logger.info("분석기 호출 시작")
        analysis_result = saju_analyzer.analyze_saju(birth_info)
        logger.info(f"분석기 결과 타입: {type(analysis_result)}")
        logger.info(f"분석기 결과 키들: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not dict'}")
        
        # 프론트엔드 호환을 위해 SimpleResponse 형식으로 변환
        if isinstance(analysis_result, dict):
            # 기본 정보 구성
            basic_info = {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성"
            }
            
            # 사주팔자 구성 (프론트엔드 형식)
            saju_palja = {
                "year_pillar": {"stem": analysis_result['palja'].year_gan, "branch": analysis_result['palja'].year_ji},
                "month_pillar": {"stem": analysis_result['palja'].month_gan, "branch": analysis_result['palja'].month_ji},
                "day_pillar": {"stem": analysis_result['palja'].day_gan, "branch": analysis_result['palja'].day_ji},
                "hour_pillar": {"stem": analysis_result['palja'].hour_gan, "branch": analysis_result['palja'].hour_ji}
            }
            
            # 오행 분석 구성 (한글 키 사용)
            wuxing_analysis = {
                "목": analysis_result['wuxing'].wood,
                "화": analysis_result['wuxing'].fire,
                "토": analysis_result['wuxing'].earth,
                "금": analysis_result['wuxing'].metal,
                "수": analysis_result['wuxing'].water
            }
            
            # 확장 오행 분석 추가
            if hasattr(analysis_result['wuxing'], 'extended_analysis') and analysis_result['wuxing'].extended_analysis:
                wuxing_analysis["extended_analysis"] = analysis_result['wuxing'].extended_analysis
            
            # 해석 구성 (문자열 형식)
            interpretations = {
                "personality": analysis_result['personality'].get('description', '성격이 온화하고 부드러우며, 타인을 배려하는 마음이 깊습니다. 감정이 풍부하고 예술적 감각이 뛰어납니다.'),
                "career": analysis_result['career'].get('description', '창작 분야나 서비스업에서 능력을 발휘할 수 있습니다. 협력을 중시하는 분야에서 성공 가능성이 높습니다.'),
                "health": analysis_result['health'].get('description', '전반적으로 건강하나 스트레스 관리에 주의가 필요합니다. 규칙적인 운동과 충분한 휴식을 권합니다.'),
                "relationships": analysis_result['relationship'].get('description', '인간관계가 원만하고 많은 사람들에게 사랑받습니다. 결혼이나 연애에 유리한 편입니다.'),
                "wealth": analysis_result['fortune'].get('description', '꾸준한 노력을 통해 안정적인 재물을 축적할 수 있습니다. 투기보다는 저축이 유리합니다.')
            }
            
            response = {
                "basic_info": basic_info,
                "saju_palja": saju_palja,
                "wuxing_analysis": wuxing_analysis,
                "interpretations": interpretations
            }
            
            logger.info("프론트엔드 호환 형식 변환 완료")
            logger.info(f"응답 구조: {list(response.keys())}")
            if "extended_analysis" in wuxing_analysis:
                logger.info("확장 분석 포함됨")
            
            return JSONResponse(content=response)
        else:
            logger.info("기존 형식 그대로 반환")
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
    gender: str,
    name: str = "테스트"
):
    """오행 분석만 수행"""
    try:
        birth_info = BirthInfoRequest(
            year=year,
            month=month,
            day=day,
            hour=hour,
            gender=gender,
            name=name
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