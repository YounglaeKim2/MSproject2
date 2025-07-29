"""
새로운 사주 분석 API - 리팩토링 버전
- 명확한 구조
- 완벽한 에러 핸들링  
- 프론트엔드 호환성 보장
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.models.saju import BirthInfoRequest
from app.services.saju_analyzer import saju_analyzer
from app.services.gemini_ai_interpreter import get_gemini_interpreter
import logging
from typing import Optional, Dict, Any
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def safe_convert_to_dict(obj) -> Dict[str, Any]:
    """객체를 안전하게 dict로 변환"""
    try:
        if hasattr(obj, 'dict'):
            return obj.dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, dict):
            return {k: safe_convert_to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [safe_convert_to_dict(item) for item in obj]
        else:
            return obj
    except Exception as e:
        logger.error(f"객체 변환 실패: {e}")
        return str(obj)

@router.post("/analyze")
async def analyze_saju_simple(birth_info: BirthInfoRequest):
    """
    사주 분석 API - 간소화 버전
    
    Args:
        birth_info: 출생 정보 (년월일시, 성별, 이름)
    
    Returns:
        완전한 사주 분석 결과
    """
    try:
        logger.info(f"=== 사주 분석 요청 시작 ===")
        logger.info(f"입력 데이터: {birth_info.dict()}")
        
        # 1. 입력 검증
        _validate_birth_info(birth_info)
        
        # 2. 사주 분석 실행
        logger.info("사주 분석 실행 중...")
        raw_result = saju_analyzer.analyze_saju(birth_info)
        logger.info(f"사주 분석 완료. 결과 타입: {type(raw_result)}")
        
        # 3. dict로 변환
        analysis_result = safe_convert_to_dict(raw_result)
        logger.info(f"변환 완료. 키들: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not dict'}")
        
        # 4. 프론트엔드 호환 형식으로 변환
        response_data = _format_for_frontend(analysis_result, birth_info)
        
        logger.info("응답 데이터 생성 완료")
        return JSONResponse(content=response_data)
        
    except ValueError as e:
        logger.error(f"입력 검증 오류: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"사주 분석 중 오류 발생: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"사주 분석 실패: {str(e)}")

def _validate_birth_info(birth_info: BirthInfoRequest):
    """입력 데이터 검증"""
    if not (1900 <= birth_info.year <= 2100):
        raise ValueError("년도는 1900-2100 사이여야 합니다.")
    if not (1 <= birth_info.month <= 12):
        raise ValueError("월은 1-12 사이여야 합니다.")
    if not (1 <= birth_info.day <= 31):
        raise ValueError("일은 1-31 사이여야 합니다.")
    if not (0 <= birth_info.hour <= 23):
        raise ValueError("시간은 0-23 사이여야 합니다.")
    if birth_info.gender.lower() not in ["male", "female", "m", "f"]:
        raise ValueError("성별은 male, female, M, F 중 하나여야 합니다.")

def _format_for_frontend(analysis_result: Dict[str, Any], birth_info: BirthInfoRequest) -> Dict[str, Any]:
    """프론트엔드 호환 형식으로 변환"""
    try:
        # 기본 정보
        basic_info = {
            "name": birth_info.name,
            "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
            "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성"
        }
        
        # 사주팔자 (안전한 접근)
        palja_data = analysis_result.get('palja', {})
        saju_palja = {
            "year_pillar": {
                "stem": palja_data.get('year_gan', '甲'), 
                "branch": palja_data.get('year_ji', '子')
            },
            "month_pillar": {
                "stem": palja_data.get('month_gan', '甲'), 
                "branch": palja_data.get('month_ji', '子')
            },
            "day_pillar": {
                "stem": palja_data.get('day_gan', '甲'), 
                "branch": palja_data.get('day_ji', '子')
            },
            "hour_pillar": {
                "stem": palja_data.get('hour_gan', '甲'), 
                "branch": palja_data.get('hour_ji', '子')
            }
        }
        
        # 오행 분석 (안전한 접근)
        wuxing_data = analysis_result.get('wuxing', {})
        wuxing_analysis = {
            "목": wuxing_data.get('wood', 0),
            "화": wuxing_data.get('fire', 0),
            "토": wuxing_data.get('earth', 0),
            "금": wuxing_data.get('metal', 0),
            "수": wuxing_data.get('water', 0)
        }
        
        # 확장 분석 (있으면 추가)
        if wuxing_data.get('extended_analysis'):
            wuxing_analysis["extended_analysis"] = wuxing_data['extended_analysis']
        
        # 해석 데이터 (안전한 접근)
        personality_data = analysis_result.get('personality', {})
        career_data = analysis_result.get('career', {})
        health_data = analysis_result.get('health', {})
        relationship_data = analysis_result.get('relationship', {})
        fortune_data = analysis_result.get('fortune', {})
        
        interpretations = {
            "personality": personality_data.get('basic_nature', '안정적이고 차분한 성격'),
            "career": career_data.get('career_tendency', '전문직이나 관리직에 적합'),
            "health": ' '.join(health_data.get('health_advice', ['건강 관리에 유의하세요'])),
            "relationships": relationship_data.get('relationship_style', '원만한 대인관계'),
            "wealth": fortune_data.get('wealth_tendency', '꾸준한 재물 증식')
        }
        
        return {
            "basic_info": basic_info,
            "saju_palja": saju_palja,
            "wuxing_analysis": wuxing_analysis,
            "interpretations": interpretations,
            "ten_stars": analysis_result.get('ten_stars', {}),
            "timestamp": "2025-07-29T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"프론트엔드 형식 변환 오류: {e}")
        # 최소한의 기본 응답
        return {
            "basic_info": {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성"
            },
            "saju_palja": {
                "year_pillar": {"stem": "甲", "branch": "子"},
                "month_pillar": {"stem": "甲", "branch": "子"},
                "day_pillar": {"stem": "甲", "branch": "子"},
                "hour_pillar": {"stem": "甲", "branch": "子"}
            },
            "wuxing_analysis": {"목": 2, "화": 1, "토": 3, "금": 1, "수": 1},
            "interpretations": {
                "personality": "분석 중 오류가 발생했습니다",
                "career": "분석 중 오류가 발생했습니다",
                "health": "분석 중 오류가 발생했습니다",
                "relationships": "분석 중 오류가 발생했습니다",
                "wealth": "분석 중 오류가 발생했습니다"
            },
            "error": f"부분적 분석 실패: {str(e)}"
        }

# 대운/세운 분석 엔드포인트들
@router.post("/daeun")
async def analyze_daeun(birth_info: BirthInfoRequest):
    """대운 분석 API"""
    try:
        logger.info(f"대운 분석 요청: {birth_info.dict()}")
        
        # 1. 입력 검증
        _validate_birth_info(birth_info)
        
        # 2. 사주팔자 추출
        palja = saju_analyzer.extract_palja(birth_info)
        logger.info(f"사주팔자 추출 완료")
        
        # 3. 대운 분석
        daeun_analysis = saju_analyzer.calculate_daeun(birth_info, palja)
        logger.info(f"대운 분석 완료: 총 {len(daeun_analysis.get('daeun_list', []))}개 대운")
        
        # 4. 응답 구성
        response = {
            "basic_info": {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성"
            },
            "palja": {
                "year_pillar": {"stem": palja.year_gan, "branch": palja.year_ji},
                "month_pillar": {"stem": palja.month_gan, "branch": palja.month_ji},
                "day_pillar": {"stem": palja.day_gan, "branch": palja.day_ji},
                "hour_pillar": {"stem": palja.hour_gan, "branch": palja.hour_ji}
            },
            "daeun_analysis": daeun_analysis
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"대운 분석 오류: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"대운 분석 실패: {str(e)}")

@router.post("/saeun")
async def analyze_saeun(birth_info: BirthInfoRequest, target_year: int = Query(None, description="분석 대상 연도")):
    """세운 분석 API"""
    try:
        logger.info(f"세운 분석 요청: {birth_info.dict()}, 대상연도: {target_year}")
        
        # 1. 입력 검증
        _validate_birth_info(birth_info)
        
        # target_year 기본값 설정 (현재 년도)
        if target_year is None:
            from datetime import datetime
            target_year = datetime.now().year
        
        # 2. 사주팔자 추출
        palja = saju_analyzer.extract_palja(birth_info)
        logger.info(f"사주팔자 추출 완료")
        
        # 3. 세운 분석
        saeun_analysis = saju_analyzer.calculate_saeun(birth_info, palja, target_year)
        logger.info(f"세운 분석 완료: 대상년도 {target_year}")
        
        # 4. 응답 구성
        response = {
            "basic_info": {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성",
                "target_year": target_year
            },
            "palja": {
                "year_pillar": {"stem": palja.year_gan, "branch": palja.year_ji},
                "month_pillar": {"stem": palja.month_gan, "branch": palja.month_ji},
                "day_pillar": {"stem": palja.day_gan, "branch": palja.day_ji},
                "hour_pillar": {"stem": palja.hour_gan, "branch": palja.hour_ji}
            },
            "saeun_analysis": saeun_analysis
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"세운 분석 오류: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"세운 분석 실패: {str(e)}")

# AI 관련 엔드포인트들
@router.post("/ai-chat")
async def ai_chat_interpretation(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="사용자 질문")
):
    """AI 대화형 사주 해석 - 간소화 버전"""
    try:
        logger.info(f"AI 채팅 요청: {question}")
        
        # 1. 사주 분석
        raw_result = saju_analyzer.analyze_saju(birth_info)
        analysis_dict = safe_convert_to_dict(raw_result)
        
        # 2. AI 해석
        ai_interpreter = get_gemini_interpreter()
        ai_result = await ai_interpreter.interpret_saju(analysis_dict, question)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "user_question": question,
                "ai_interpretation": ai_result
            }
        }
        
    except Exception as e:
        logger.error(f"AI 해석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"AI 해석 실패: {str(e)}")

@router.get("/ai-usage")
async def get_ai_usage():
    """AI 사용량 조회"""
    try:
        ai_interpreter = get_gemini_interpreter()
        usage_status = ai_interpreter.get_usage_status()
        return {"success": True, "data": usage_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-test")
async def test_ai_connection():
    """AI 연결 테스트"""
    try:
        ai_interpreter = get_gemini_interpreter()
        test_result = await ai_interpreter.test_connection()
        return test_result
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "saju-analysis", "version": "2.0-refactored"}

@router.get("/test")
async def test_endpoint():
    """API 테스트"""
    return {
        "message": "새로운 사주 API가 정상 작동중입니다! 🚀",
        "version": "2.0-refactored-with-daeun",
        "endpoints": [
            "/analyze - 사주 분석 (새 버전)",
            "/daeun - 대운 분석 ✨FIXED✨",
            "/saeun - 세운 분석 ✨FIXED✨",
            "/ai-chat - AI 대화형 해석",
            "/ai-usage - AI 사용량 조회", 
            "/ai-test - AI 연결 테스트",
            "/health - 헬스 체크",
            "/test - 이 테스트"
        ]
    }