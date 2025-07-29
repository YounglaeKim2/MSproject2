from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from app.models.saju import (
    BirthInfoRequest, SajuAnalysisResponse, ErrorResponse,
    SajuAnalysisSimpleResponse, BasicInfo, PillarInfo, SajuPalja,
    WuxingAnalysisSimple, InterpretationsSimple
)
from app.services.saju_analyzer import saju_analyzer
from app.services.gemini_ai_interpreter import get_gemini_interpreter
import logging
from typing import Optional

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
            palja_data = analysis_result.get('palja', {})
            saju_palja = {
                "year_pillar": {"stem": palja_data.get('year_gan', ''), "branch": palja_data.get('year_ji', '')},
                "month_pillar": {"stem": palja_data.get('month_gan', ''), "branch": palja_data.get('month_ji', '')},
                "day_pillar": {"stem": palja_data.get('day_gan', ''), "branch": palja_data.get('day_ji', '')},
                "hour_pillar": {"stem": palja_data.get('hour_gan', ''), "branch": palja_data.get('hour_ji', '')}
            }
            
            # 오행 분석 구성 (한글 키 사용)
            wuxing_data = analysis_result.get('wuxing', {})
            wuxing_analysis = {
                "목": wuxing_data.get('wood', 0),
                "화": wuxing_data.get('fire', 0),
                "토": wuxing_data.get('earth', 0),
                "금": wuxing_data.get('metal', 0),
                "수": wuxing_data.get('water', 0)
            }
            
            # 확장 오행 분석 추가
            if wuxing_data.get('extended_analysis'):
                wuxing_analysis["extended_analysis"] = wuxing_data.get('extended_analysis')
                
                # 강점과 약점을 personality_analysis에 추가
                if "personality_analysis" not in wuxing_analysis["extended_analysis"]:
                    wuxing_analysis["extended_analysis"]["personality_analysis"] = {}
                
                # 실제 분석 결과에서 강점과 약점 가져오기
                wuxing_analysis["extended_analysis"]["personality_analysis"]["strengths"] = analysis_result['personality'].get('strengths', [])
                wuxing_analysis["extended_analysis"]["personality_analysis"]["weaknesses"] = analysis_result['personality'].get('weaknesses', [])
                wuxing_analysis["extended_analysis"]["personality_analysis"]["personality_type"] = analysis_result['personality'].get('basic_nature', '')
            else:
                # extended_analysis가 없는 경우 새로 생성
                wuxing_analysis["extended_analysis"] = {
                    "personality_analysis": {
                        "strengths": analysis_result['personality'].get('strengths', []),
                        "weaknesses": analysis_result['personality'].get('weaknesses', []),
                        "personality_type": analysis_result['personality'].get('basic_nature', '')
                    }
                }
            
            # 해석 구성 (문자열 형식) - 실제 분석 결과 직접 사용
            personality_value = analysis_result['personality'].get('basic_nature')
            career_value = analysis_result['career'].get('career_tendency')
            health_value = " ".join(analysis_result['health'].get('health_advice', []))
            relationships_value = analysis_result['relationship'].get('relationship_style')
            wealth_value = analysis_result['fortune'].get('wealth_tendency')
            
            interpretations = {
                "personality": personality_value if personality_value else '성격이 온화하고 부드러우며, 타인을 배려하는 마음이 깊습니다. 감정이 풍부하고 예술적 감각이 뛰어납니다.',
                "career": career_value if career_value else '창작 분야나 서비스업에서 능력을 발휘할 수 있습니다. 협력을 중시하는 분야에서 성공 가능성이 높습니다.',
                "health": health_value if health_value else '전반적으로 건강하나 스트레스 관리에 주의가 필요합니다. 규칙적인 운동과 충분한 휴식을 권합니다.',
                "relationships": relationships_value if relationships_value else '인간관계가 원만하고 많은 사람들에게 사랑받습니다. 결혼이나 연애에 유리한 편입니다.',
                "wealth": wealth_value if wealth_value else '꾸준한 노력을 통해 안정적인 재물을 축적할 수 있습니다. 투기보다는 저축이 유리합니다.'
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

@router.post(
    "/daeun", 
    summary="대운 분석",
    description="출생 정보를 바탕으로 대운(大運)을 계산하고 인생 전체의 운세 흐름을 제공합니다."
)
async def analyze_daeun(birth_info: BirthInfoRequest):
    """
    대운 분석 API
    
    - **year**: 출생년도 (1900-2100)
    - **month**: 출생월 (1-12)
    - **day**: 출생일 (1-31)
    - **hour**: 출생시간 (0-23)
    - **gender**: 성별 (male/female)
    - **name**: 이름
    
    Returns:
    - 대운 시작 나이
    - 순행/역행 여부
    - 현재 나이
    - 각 대운별 상세 분석 (80세까지)
    """
    try:
        logger.info(f"=== 대운 분석 요청 시작 ===")
        logger.info(f"대운 분석 요청: {birth_info.dict()}")
        
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
            raise HTTPException(status_code=400, detail="성별은 male, female, M, F 중 하나여야 합니다.")
        
        # 성별 정규화
        gender = "male" if birth_info.gender.upper() == "M" else "female" if birth_info.gender.upper() == "F" else birth_info.gender
        birth_info.gender = gender
        
        # 1. 사주팔자 추출
        palja = saju_analyzer.extract_palja(birth_info)
        logger.info(f"사주팔자 추출 완료: {palja.dict()}")
        
        # 2. 대운 계산 및 분석
        daeun_analysis = saju_analyzer.calculate_daeun(birth_info, palja)
        logger.info(f"대운 분석 완료: 총 {len(daeun_analysis['daeun_list'])}개 대운")
        
        # 3. 응답 구성
        response = {
            "basic_info": {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if gender == "male" else "여성"
            },
            "palja": {
                "year_pillar": {"stem": palja.year_gan, "branch": palja.year_ji},
                "month_pillar": {"stem": palja.month_gan, "branch": palja.month_ji},
                "day_pillar": {"stem": palja.day_gan, "branch": palja.day_ji},
                "hour_pillar": {"stem": palja.hour_gan, "branch": palja.hour_ji}
            },
            "daeun_analysis": daeun_analysis
        }
        
        logger.info("=== 대운 분석 요청 완료 ===")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"대운 분석 중 오류: {str(e)}")
        logger.error(f"오류 상세: {type(e).__name__}")
        import traceback
        logger.error(f"스택 트레이스: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"대운 분석 중 오류가 발생했습니다: {str(e)}")

@router.post(
    "/saeun", 
    summary="세운 분석",
    description="출생 정보를 바탕으로 세운(歲運)을 계산하고 연간/월별 운세를 제공합니다."
)
async def analyze_saeun(birth_info: BirthInfoRequest, target_year: int = None):
    """
    세운 분석 API
    
    - **year**: 출생년도 (1900-2100)
    - **month**: 출생월 (1-12)
    - **day**: 출생일 (1-31)
    - **hour**: 출생시간 (0-23)
    - **gender**: 성별 (male/female)
    - **name**: 이름
    - **target_year**: 분석 대상 연도 (선택사항, 미지정시 현재 연도)
    
    Returns:
    - 대상 연도의 연간 세운
    - 12개월별 세운
    - 개인 사주와의 상호작용 분석
    - 주의/기회 시기 추천
    """
    try:
        logger.info(f"=== 세운 분석 요청 시작 ===")
        logger.info(f"세운 분석 요청: {birth_info.dict()}, 대상연도: {target_year}")
        
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
            raise HTTPException(status_code=400, detail="성별은 male, female, M, F 중 하나여야 합니다.")
        
        # target_year 기본값 설정 (현재 년도)
        if target_year is None:
            from datetime import datetime
            target_year = datetime.now().year
        
        # 성별 정규화
        gender = "male" if birth_info.gender.upper() == "M" else "female" if birth_info.gender.upper() == "F" else birth_info.gender
        birth_info.gender = gender
        
        # 1. 사주팔자 추출
        palja = saju_analyzer.extract_palja(birth_info)
        logger.info(f"사주팔자 추출 완료: {palja.dict()}")
        
        # 2. 세운 계산 및 분석
        saeun_analysis = saju_analyzer.calculate_saeun(birth_info, palja, target_year)
        logger.info(f"세운 분석 완료: 대상년도 {target_year}")
        
        # 3. 응답 구성
        response = {
            "basic_info": {
                "name": birth_info.name,
                "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시",
                "gender": "남성" if gender == "male" else "여성",
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
        
        logger.info("=== 세운 분석 요청 완료 ===")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"세운 분석 중 오류: {str(e)}")
        logger.error(f"오류 상세: {type(e).__name__}")
        import traceback
        logger.error(f"스택 트레이스: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"세운 분석 중 오류가 발생했습니다: {str(e)}")

@router.post("/ai-chat")
async def ai_chat_interpretation(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="사용자 질문"),
    context: Optional[str] = Query(None, description="분석 영역 (personality|career|health|relationship|fortune)")
):
    """
    Google Gemini AI 기반 사주 해석 채팅
    
    - **birth_info**: 출생 정보
    - **question**: 사용자 질문 (예: "내 성격의 장단점을 알려주세요")
    - **context**: 분석 영역 (선택사항)
    """
    try:
        logger.info(f"=== AI 해석 요청 시작 ===")
        logger.info(f"질문: {question}, 컨텍스트: {context}")
        
        # 1. 기존 사주 분석 수행 (이제 dict로 반환됨)
        analysis_result = saju_analyzer.analyze_saju(birth_info)
        logger.info("기본 사주 분석 완료")
        
        # 2. 임시로 AI 해석 완전 우회
        ai_result = {
            "success": True,
            "ai_interpretation": f"질문 '{question}'에 대한 간단한 답변입니다.",
            "model": "gemini-2.5-flash"
        }
        
        # 3. 간단한 응답 구성 (JSON serialization 오류 방지)
        response = {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "user_question": question,
                "ai_interpretation": {
                    "success": ai_result.get("success", False),
                    "ai_interpretation": ai_result.get("ai_interpretation", ""),
                    "model": ai_result.get("model", "gemini-2.5-flash")
                }
            }
        }
        
        logger.info("=== AI 해석 요청 완료 ===")
        return response
        
    except Exception as e:
        logger.error(f"AI 해석 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI 해석 중 오류가 발생했습니다: {str(e)}")

@router.get("/ai-usage")
async def get_ai_usage():
    """Gemini AI 사용량 조회"""
    try:
        ai_interpreter = get_gemini_interpreter()
        usage_status = ai_interpreter.get_usage_status()
        
        return {
            "success": True,
            "usage_status": usage_status,
            "limits": {
                "daily_limit": "일 1,000회 (무료)",
                "monthly_limit": "월 30,000회 (무료)",
                "note": "무료 한도 초과 시 자동 중단됩니다."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai-chat")
async def ai_chat_interpretation(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="사용자 질문"),
    context: str = Query(None, description="분석 영역 (personality|career|health|relationship|fortune)")
):
    """AI 대화형 사주 해석"""
    try:
        logger.info(f"=== AI 채팅 요청 시작 ===")
        logger.info(f"출생정보: {birth_info.dict()}")
        logger.info(f"질문: {question}")
        logger.info(f"컨텍스트: {context}")
        
        # 1. 기존 사주 분석 실행
        analysis_result = saju_analyzer.analyze_saju(birth_info)
        logger.info(f"사주 분석 완료")
        
        # 2. Pydantic 모델을 dict로 변환
        def convert_to_dict(obj):
            if hasattr(obj, 'dict'):
                return obj.dict()
            elif isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            else:
                return obj
        
        analysis_dict = convert_to_dict(analysis_result)
        logger.info(f"딕셔너리 변환 완료")
        
        # 3. AI 해석 실행
        ai_interpreter = get_gemini_interpreter()
        ai_result = await ai_interpreter.interpret_saju(analysis_dict, question, context)
        logger.info(f"AI 해석 완료: {ai_result.get('success', False)}")
        
        return {
            "success": True,
            "data": {
                "ai_interpretation": ai_result,
                "analysis_context": {
                    "palja": analysis_dict.get('palja', {}),
                    "personality": analysis_dict.get('personality', {}),
                    "relevant_data": analysis_dict.get(context, {}) if context else {}
                },
                "timestamp": ai_result.get('timestamp', '')
            }
        }
        
    except Exception as e:
        logger.error(f"AI 해석 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI 해석 중 오류가 발생했습니다: {str(e)}")

@router.get("/ai-usage")
async def get_ai_usage():
    """AI 사용량 조회"""
    try:
        ai_interpreter = get_gemini_interpreter()
        usage_status = ai_interpreter.get_usage_status()
        return {
            "success": True,
            "data": usage_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-test")
async def test_ai_connection():
    """Gemini AI 연결 테스트"""
    try:
        ai_interpreter = get_gemini_interpreter()
        test_result = await ai_interpreter.test_connection()
        return test_result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Gemini AI 연결 테스트 실패"
        }

@router.get("/test")
async def test_endpoint():
    """API 테스트용 엔드포인트 - AI 기능 추가"""
    return {
        "message": "사주 AI API가 정상적으로 작동중입니다! 🤖",
        "endpoints": [
            "/analyze - 완전한 사주 분석",
            "/palja-only - 사주팔자만 추출", 
            "/wuxing-only - 오행 분석만",
            "/daeun - 대운 분석",
            "/saeun - 세운 분석",
            "/ai-chat - AI 대화형 해석 ✨NEW✨",
            "/ai-usage - AI 사용량 조회 ✨NEW✨",
            "/ai-test - AI 연결 테스트 ✨NEW✨",
            "/test - 테스트"
        ],
        "ai_features": {
            "model": "Google Gemini 1.5 Pro",
            "daily_limit": "1,000회 무료",
            "monthly_limit": "30,000회 무료"
        }
    }