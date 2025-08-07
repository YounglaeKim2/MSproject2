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
from app.services.ai_interpreter_factory import get_unified_ai_interpreter, AIInterpreterFactory
from app.services.extended_fortune_analyzer import extended_fortune_analyzer
import logging
from typing import Optional, Dict, Any
import traceback

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# ==================== 헬퍼 함수들 ====================

async def _generate_ai_questions(analysis_dict: Dict[str, Any], birth_info: BirthInfoRequest, ai_provider: str = "azure") -> Dict[str, Any]:
    """AI를 사용한 질문 생성"""
    ai_interpreter = get_unified_ai_interpreter(ai_provider)
    return await ai_interpreter.generate_suggested_questions(analysis_dict, birth_info.dict())

def _generate_rule_based_questions(analysis_dict: Dict[str, Any], birth_info: BirthInfoRequest) -> Dict[str, Any]:
    """룰 기반 질문 생성"""
    from datetime import datetime
    
    questions = []
    
    # 오행 분석 기반 질문
    wuxing = analysis_dict.get('wuxing', {})
    wuxing_dist = wuxing.get('distribution', {})
    
    if wuxing_dist.get('wood', 0) > 30:
        questions.append({
            "question": "목기가 강한 당신, 올해 창업 적기는?",
            "category": "직업", 
            "priority": "high",
            "icon": "🌱"
        })
    elif wuxing_dist.get('fire', 0) > 30:
        questions.append({
            "question": "화기가 왕성한 시기, 인맥 확장 방법은?",
            "category": "인간관계",
            "priority": "high", 
            "icon": "🔥"
        })
    elif wuxing_dist.get('earth', 0) > 30:
        questions.append({
            "question": "토기가 풍부한 당신, 부동산 투자는?",
            "category": "재물",
            "priority": "medium",
            "icon": "🏠"
        })
    elif wuxing_dist.get('metal', 0) > 30:
        questions.append({
            "question": "금기가 강한 시기, 결단력 발휘할 때는?",
            "category": "성격",
            "priority": "medium",
            "icon": "⚔️"
        })
    else:  # water 또는 균형잡힌 경우
        questions.append({
            "question": "수기로 지혜로운 당신, 학습 적기는?",
            "category": "자기계발",
            "priority": "medium", 
            "icon": "💧"
        })
    
    # 십성 분석 기반 질문  
    ten_stars = analysis_dict.get('ten_stars', {})
    dominant_stars = ten_stars.get('dominant_stars', [])
    
    if '정관' in str(dominant_stars):
        questions.append({
            "question": "정관운이 나타나는데, 승진 가능성은?",
            "category": "직업",
            "priority": "high",
            "icon": "👑"
        })
    elif '편재' in str(dominant_stars):
        questions.append({
            "question": "편재가 강한 시기, 부업 시작하면?",
            "category": "재물", 
            "priority": "high",
            "icon": "💰"
        })
    elif '식신' in str(dominant_stars):
        questions.append({
            "question": "식신으로 창의력이 높은데, 예술 분야는?",
            "category": "취미",
            "priority": "medium",
            "icon": "🎨"
        })
    else:
        questions.append({
            "question": "현재 운세의 특징과 활용법은?",
            "category": "운세",
            "priority": "medium", 
            "icon": "🔮"
        })
    
    # 성격 분석 기반 질문
    personality = analysis_dict.get('personality', {})
    strengths = personality.get('strengths', [])
    
    if '리더십' in str(strengths):
        questions.append({
            "question": "타고난 리더십, 언제 발휘하면 좋을까?",
            "category": "인간관계",
            "priority": "medium",
            "icon": "👥"
        })
    elif '창의성' in str(strengths):
        questions.append({
            "question": "창의적 능력을 활용한 부업은?",
            "category": "직업",
            "priority": "medium", 
            "icon": "💡"
        })
    else:
        questions.append({
            "question": "내 숨겨진 재능을 발견하려면?",
            "category": "성격",
            "priority": "low",
            "icon": "✨"
        })
    
    # 연애/건강 기본 질문 추가
    if len(questions) < 4:
        questions.append({
            "question": f"올해 {birth_info.name}님의 연애운은?",
            "category": "연애",
            "priority": "high" if birth_info.gender.lower() in ['male', 'm'] else "medium",
            "icon": "💕"
        })
    
    if len(questions) < 5:
        questions.append({
            "question": "건강 관리에서 주의할 점은?",
            "category": "건강", 
            "priority": "medium",
            "icon": "🏥"
        })
    
    # 5개 제한
    questions = questions[:5]
    
    return {
        "suggested_questions": questions,
        "generation_method": "rules",
        "timestamp": datetime.now().isoformat(),
        "total_questions": len(questions)
    }

def _get_fallback_questions() -> list:
    """최후 폴백용 기본 질문들"""
    return [
        {"question": "내 성격의 장단점은 무엇인가요?", "category": "성격", "priority": "high", "icon": "🤔"},
        {"question": "올해 전체 운세는 어떤가요?", "category": "운세", "priority": "high", "icon": "🔮"},
        {"question": "직업운에 대해 알려주세요", "category": "직업", "priority": "medium", "icon": "💼"},
        {"question": "연애운은 어떤가요?", "category": "연애", "priority": "medium", "icon": "💕"},
        {"question": "건강 관리 포인트는?", "category": "건강", "priority": "low", "icon": "🏥"}
    ]

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
async def analyze_saju_simple(birth_info: BirthInfoRequest, ai_provider: str = Query("azure", description="AI provider: azure or gemini")):
    """
    사주 분석 API - 간소화 버전
    
    Args:
        birth_info: 출생 정보 (년월일시, 성별, 이름)
        ai_provider: AI 제공자 선택 ("azure" 또는 "gemini", 기본값: "azure")
    
    Returns:
        완전한 사주 분석 결과
    """
    try:
        logger.info(f"=== 사주 분석 요청 시작 ===")
        logger.info(f"입력 데이터: {birth_info.dict()}, AI Provider: {ai_provider}")
        
        # 1. 입력 검증
        _validate_birth_info(birth_info)
        
        # AI provider 검증
        if ai_provider.lower() not in ["azure", "gemini"]:
            logger.warning(f"잘못된 AI provider: {ai_provider}. 기본값 azure 사용")
            ai_provider = "azure"
        
        # 2. 사주 분석 실행
        logger.info("사주 분석 실행 중...")
        raw_result = saju_analyzer.analyze_saju(birth_info)
        logger.info(f"사주 분석 완료. 결과 타입: {type(raw_result)}")
        
        # 3. dict로 변환
        analysis_result = safe_convert_to_dict(raw_result)
        logger.info(f"변환 완료. 키들: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not dict'}")
        
        # 4. 프론트엔드 호환 형식으로 변환
        response_data = _format_for_frontend(analysis_result, birth_info, ai_provider)
        
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

def _format_for_frontend(analysis_result: Dict[str, Any], birth_info: BirthInfoRequest, ai_provider: str = "azure") -> Dict[str, Any]:
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
    question: str = Query(..., description="사용자 질문"),
    ai_provider: str = Query("azure", description="AI provider: azure or gemini")
):
    """AI 대화형 사주 해석 - 간소화 버전"""
    try:
        logger.info(f"AI 채팅 요청: {question}, AI Provider: {ai_provider}")
        
        # 1. 사주 분석
        raw_result = saju_analyzer.analyze_saju(birth_info)
        analysis_dict = safe_convert_to_dict(raw_result)
        
        # 2. AI 해석
        ai_interpreter = get_unified_ai_interpreter(ai_provider)
        ai_result = await ai_interpreter.interpret_saju(analysis_dict, question, None)
        
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
async def get_ai_usage(ai_provider: str = Query("gemini", description="AI provider: azure or gemini")):
    """AI 사용량 조회 (Gemini만 지원)"""
    try:
        if ai_provider.lower() == "gemini":
            ai_interpreter = get_gemini_interpreter()
            usage_status = ai_interpreter.get_usage_status()
            return {"success": True, "data": usage_status, "provider": "gemini"}
        else:
            return {
                "success": True, 
                "message": "Azure OpenAI는 별도 사용량 제한 없음",
                "data": {"unlimited": True},
                "provider": "azure"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-providers")
async def get_ai_providers():
    """사용 가능한 AI Provider 목록 조회"""
    try:
        providers = AIInterpreterFactory.get_available_providers()
        default_provider = AIInterpreterFactory.get_default_provider()
        
        return {
            "success": True,
            "data": {
                "providers": providers,
                "default_provider": default_provider
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggested-questions")
async def generate_suggested_questions(
    birth_info: BirthInfoRequest,
    method: str = Query("hybrid", description="질문 생성 방식: ai|rules|hybrid"),
    ai_provider: str = Query("azure", description="AI provider: azure or gemini")
):
    """사주 분석 결과 기반 개인화된 예상 질문 생성 - 하이브리드 방식"""
    try:
        logger.info(f"예상 질문 생성 요청: {birth_info.name}, 방식: {method}, AI Provider: {ai_provider}")
        
        # 1. 사주 분석 (기존 로직 재사용)
        raw_result = saju_analyzer.analyze_saju(birth_info)
        analysis_dict = safe_convert_to_dict(raw_result)
        
        # 2. 하이브리드 방식으로 질문 생성
        if method == "ai":
            # AI 방식만 사용
            questions_result = await _generate_ai_questions(analysis_dict, birth_info, ai_provider)
        elif method == "rules":
            # 룰 기반 방식만 사용
            questions_result = _generate_rule_based_questions(analysis_dict, birth_info)
        else:  # hybrid (기본값)
            # AI 시도 → 실패 시 룰 기반 폴백
            try:
                logger.info("AI 질문 생성 시도")
                questions_result = await _generate_ai_questions(analysis_dict, birth_info, ai_provider)
                questions_result["generation_method"] = "ai"
            except Exception as e:
                logger.warning(f"AI 질문 생성 실패, 룰 기반으로 폴백: {e}")
                questions_result = _generate_rule_based_questions(analysis_dict, birth_info)
                questions_result["generation_method"] = "rules_fallback"
        
        return JSONResponse({
            "success": True,
            "data": questions_result
        })
        
    except Exception as e:
        logger.error(f"질문 생성 실패: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        
        # 최후 폴백: 기본 질문들
        fallback_questions = _get_fallback_questions()
        return JSONResponse({
            "success": True,
            "data": {
                "suggested_questions": fallback_questions,
                "generation_method": "fallback",
                "timestamp": "emergency_fallback"
            }
        })

@router.get("/ai-test")
async def test_ai_connection(ai_provider: str = Query("azure", description="AI provider: azure or gemini")):
    """AI 연결 테스트"""
    try:
        ai_interpreter = get_unified_ai_interpreter(ai_provider)
        test_result = await ai_interpreter.test_connection()
        return test_result
    except Exception as e:
        return {"success": False, "error": str(e), "provider": ai_provider}

@router.post("/extended-fortune")
async def analyze_extended_fortune(birth_info: BirthInfoRequest):
    """
    확장 운세 분석 API (1단계: 4개 운세)
    
    Args:
        birth_info: 출생 정보 (년월일시, 성별, 이름)
    
    Returns:
        주거운, 교통운, 소셜운, 취미운 분석 결과
    """
    try:
        logger.info(f"확장 운세 분석 요청: {birth_info.name}({birth_info.gender})")
        
        # 출생 정보를 dict로 변환
        birth_data = {
            "year": birth_info.year,
            "month": birth_info.month,
            "day": birth_info.day,
            "hour": birth_info.hour,
            "gender": birth_info.gender,
            "name": birth_info.name
        }
        
        # 각 운세 분석 실행
        residence_result = extended_fortune_analyzer.analyze_residence_fortune(birth_data)
        transportation_result = extended_fortune_analyzer.analyze_transportation_fortune(birth_data)
        social_result = extended_fortune_analyzer.analyze_social_fortune(birth_data)
        hobby_result = extended_fortune_analyzer.analyze_hobby_fortune(birth_data)
        
        # 성공적인 분석 결과 반환
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "residence_fortune": residence_result,
                "transportation_fortune": transportation_result,
                "social_fortune": social_result,
                "hobby_fortune": hobby_result
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"확장 운세 분석 오류: {e}")
        logger.error(f"상세 오류: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"확장 운세 분석 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/residence-fortune")
async def analyze_residence_fortune_only(birth_info: BirthInfoRequest):
    """
    주거운 분석 API
    
    Args:
        birth_info: 출생 정보
    
    Returns:
        주거운 분석 결과 (이사방향, 인테리어, 풍수 등)
    """
    try:
        logger.info(f"주거운 분석 요청: {birth_info.name}")
        
        birth_data = {
            "year": birth_info.year,
            "month": birth_info.month,
            "day": birth_info.day,
            "hour": birth_info.hour,
            "gender": birth_info.gender,
            "name": birth_info.name
        }
        
        result = extended_fortune_analyzer.analyze_residence_fortune(birth_data)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일"
                },
                "residence_fortune": result
            }
        }
        
    except Exception as e:
        logger.error(f"주거운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"주거운 분석 실패: {str(e)}")

@router.post("/transportation-fortune")
async def analyze_transportation_fortune_only(birth_info: BirthInfoRequest):
    """교통운 분석 API"""
    try:
        birth_data = {
            "year": birth_info.year,
            "month": birth_info.month,
            "day": birth_info.day,
            "hour": birth_info.hour,
            "gender": birth_info.gender,
            "name": birth_info.name
        }
        
        result = extended_fortune_analyzer.analyze_transportation_fortune(birth_data)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일"
                },
                "transportation_fortune": result
            }
        }
        
    except Exception as e:
        logger.error(f"교통운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"교통운 분석 실패: {str(e)}")

@router.post("/social-fortune")
async def analyze_social_fortune_only(birth_info: BirthInfoRequest):
    """소셜운 분석 API"""
    try:
        birth_data = {
            "year": birth_info.year,
            "month": birth_info.month,
            "day": birth_info.day,
            "hour": birth_info.hour,
            "gender": birth_info.gender,
            "name": birth_info.name
        }
        
        result = extended_fortune_analyzer.analyze_social_fortune(birth_data)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일"
                },
                "social_fortune": result
            }
        }
        
    except Exception as e:
        logger.error(f"소셜운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"소셜운 분석 실패: {str(e)}")

@router.post("/hobby-fortune")
async def analyze_hobby_fortune_only(birth_info: BirthInfoRequest):
    """취미운 분석 API"""
    try:
        birth_data = {
            "year": birth_info.year,
            "month": birth_info.month,
            "day": birth_info.day,
            "hour": birth_info.hour,
            "gender": birth_info.gender,
            "name": birth_info.name
        }
        
        result = extended_fortune_analyzer.analyze_hobby_fortune(birth_data)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일"
                },
                "hobby_fortune": result
            }
        }
        
    except Exception as e:
        logger.error(f"취미운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"취미운 분석 실패: {str(e)}")

@router.post("/love-fortune")
async def analyze_love_fortune(birth_info: BirthInfoRequest):
    """
    연애운 상세 분석 API
    
    Args:
        birth_info: 출생 정보 (년월일시, 성별, 이름)
    
    Returns:
        연애운 상세 분석 결과 (이상형, 연애스타일, 결혼적령기, 월별운세)
    """
    try:
        logger.info(f"연애운 분석 요청: {birth_info.name}({birth_info.gender})")
        
        # 간단한 연애운 분석 (생년월일 기반)
        # 년도와 월일을 기반으로 일간 추정 (간소화 버전)
        year_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        day_stem = year_stems[(birth_info.year + birth_info.month + birth_info.day) % 10]
        gender = birth_info.gender
        
        # 이상형 분석 (일간 기반)
        ideal_type_analysis = {
            "甲": "활동적이고 밝은 성격의 사람을 선호합니다. 리더십이 있고 진취적인 상대에게 매력을 느낍니다.",
            "乙": "부드럽고 섬세한 성격의 사람을 좋아합니다. 예술적 감각이 있고 따뜻한 마음을 가진 상대를 원합니다.",
            "丙": "열정적이고 밝은 에너지를 가진 사람에게 끌립니다. 사교적이고 활발한 성격의 상대를 선호합니다.",
            "丁": "차분하고 지적인 매력을 가진 사람을 좋아합니다. 세심하고 배려심 깊은 상대에게 매력을 느낍니다.",
            "戊": "안정적이고 믿을 수 있는 사람을 선호합니다. 현실적이고 책임감 있는 상대를 원합니다.",
            "己": "친근하고 따뜻한 성격의 사람을 좋아합니다. 가정적이고 포용력 있는 상대에게 끌립니다.",
            "庚": "당당하고 정직한 사람을 선호합니다. 명확하고 솔직한 성격의 상대를 좋아합니다.",
            "辛": "세련되고 우아한 매력을 가진 사람에게 끌립니다. 품격 있고 감각적인 상대를 원합니다.",
            "壬": "자유롭고 개방적인 성격의 사람을 좋아합니다. 지혜롭고 적응력이 뛰어난 상대를 선호합니다.",
            "癸": "깊이 있고 신비로운 매력을 가진 사람에게 끌립니다. 내면이 깊고 이해심 많은 상대를 원합니다."
        }
        
        # 연애 스타일 분석
        love_style_analysis = {
            "甲": "직접적이고 적극적인 어프로치를 선호합니다. 솔직하게 마음을 표현하는 스타일입니다.",
            "乙": "은은하고 섬세한 연애를 좋아합니다. 서서히 감정을 쌓아가는 스타일입니다.",
            "丙": "열정적이고 로맨틱한 연애를 추구합니다. 화려하고 드라마틱한 관계를 선호합니다.",
            "丁": "깊이 있고 진지한 연애를 원합니다. 정신적 교감을 중시하는 스타일입니다.",
            "戊": "안정적이고 현실적인 연애를 선호합니다. 장기적인 관계를 지향하는 스타일입니다.",
            "己": "부드럽고 배려심 넘치는 연애를 좋아합니다. 상대방을 감싸주는 스타일입니다.",
            "庚": "명확하고 결단력 있는 연애를 합니다. 확실한 관계를 선호하는 스타일입니다.",
            "辛": "세련되고 우아한 연애를 추구합니다. 품격 있는 관계를 중시하는 스타일입니다.",
            "壬": "자유롭고 개방적인 연애를 좋아합니다. 속박받지 않는 관계를 선호하는 스타일입니다.",
            "癸": "깊고 내밀한 연애를 원합니다. 영혼의 교감을 중시하는 스타일입니다."
        }
        
        # 결혼 적령기 (성별 고려)
        base_marriage_age = {
            "甲": {"early": 25, "ideal": 29, "late": 35},
            "乙": {"early": 24, "ideal": 28, "late": 34},
            "丙": {"early": 23, "ideal": 27, "late": 33},
            "丁": {"early": 26, "ideal": 30, "late": 36},
            "戊": {"early": 27, "ideal": 31, "late": 37},
            "己": {"early": 25, "ideal": 29, "late": 35},
            "庚": {"early": 28, "ideal": 32, "late": 38},
            "辛": {"early": 24, "ideal": 28, "late": 34},
            "壬": {"early": 26, "ideal": 30, "late": 36},
            "癸": {"early": 27, "ideal": 31, "late": 37}
        }
        
        marriage_timing = base_marriage_age.get(day_stem, {"early": 25, "ideal": 29, "late": 35})
        if gender == "female":  # 여성은 평균 2-3년 빠름
            marriage_timing = {k: v - 2 for k, v in marriage_timing.items()}
        
        love_fortune_result = {
            "ideal_type": {
                "description": ideal_type_analysis.get(day_stem, "매력적인 사람을 선호합니다."),
                "key_traits": ["매력적인 외모", "좋은 성격", "가치관 일치"]
            },
            "love_style": {
                "description": love_style_analysis.get(day_stem, "자연스러운 연애를 추구합니다."),
                "approach": "진심 어린 마음으로 다가가세요",
                "strengths": ["진실한 마음", "깊은 애정"],
                "advice": "자신만의 매력을 발휘하여 좋은 인연을 만들어보세요."
            },
            "marriage_timing": marriage_timing,
            "monthly_fortune": {
                "best_months": ["5월", "8월", "10월"],
                "caution_months": ["2월", "7월"],
                "advice": "긍정적인 마음으로 새로운 만남에 열려있으세요."
            }
        }
        
        # 성공적인 분석 결과 반환
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "love_fortune_analysis": love_fortune_result
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"연애운 분석 오류: {e}")
        logger.error(f"상세 오류: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"연애운 분석 실패: {str(e)}")

# Phase 2 확장 운세 엔드포인트들
@router.post("/career-fortune")
async def analyze_career_fortune(birth_info: BirthInfoRequest):
    """💼 직업운 상세 분석 API"""
    try:
        logger.info(f"직업운 분석 요청: {birth_info.dict()}")
        _validate_birth_info(birth_info)
        
        # 직업운 분석 실행
        career_result = extended_fortune_analyzer.analyze_career_fortune(birth_info.dict())
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "career_fortune": career_result
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"직업운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"직업운 분석 실패: {str(e)}")

@router.post("/health-fortune")
async def analyze_health_fortune(birth_info: BirthInfoRequest):
    """🏥 건강운 세분화 API"""
    try:
        logger.info(f"건강운 분석 요청: {birth_info.dict()}")
        _validate_birth_info(birth_info)
        
        # 건강운 분석 실행
        health_result = extended_fortune_analyzer.analyze_health_fortune(birth_info.dict())
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "health_fortune": health_result
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"건강운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"건강운 분석 실패: {str(e)}")

@router.post("/study-fortune")
async def analyze_study_fortune(birth_info: BirthInfoRequest):
    """📚 학업/자기계발운 API"""
    try:
        logger.info(f"학업운 분석 요청: {birth_info.dict()}")
        _validate_birth_info(birth_info)
        
        # 학업운 분석 실행
        study_result = extended_fortune_analyzer.analyze_study_fortune(birth_info.dict())
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "study_fortune": study_result
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"학업운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"학업운 분석 실패: {str(e)}")

@router.post("/family-fortune")
async def analyze_family_fortune(birth_info: BirthInfoRequest):
    """👨‍👩‍👧‍👦 가족운 API"""
    try:
        logger.info(f"가족운 분석 요청: {birth_info.dict()}")
        _validate_birth_info(birth_info)
        
        # 가족운 분석 실행
        family_result = extended_fortune_analyzer.analyze_family_fortune(birth_info.dict())
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "family_fortune": family_result
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"가족운 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"가족운 분석 실패: {str(e)}")

# Phase 2 통합 확장 운세 API
@router.post("/extended-fortune-phase2")
async def analyze_extended_fortune_phase2(birth_info: BirthInfoRequest):
    """🔮 Phase 2 확장 운세 통합 분석 API (4개 운세)"""
    try:
        logger.info(f"Phase 2 확장 운세 분석 요청: {birth_info.dict()}")
        _validate_birth_info(birth_info)
        
        birth_data = birth_info.dict()
        
        # Phase 2 4개 운세 동시 분석
        career_result = extended_fortune_analyzer.analyze_career_fortune(birth_data)
        health_result = extended_fortune_analyzer.analyze_health_fortune(birth_data)
        study_result = extended_fortune_analyzer.analyze_study_fortune(birth_data)
        family_result = extended_fortune_analyzer.analyze_family_fortune(birth_data)
        
        return {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": birth_info.gender,
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "phase2_fortune": {
                    "career_fortune": career_result,
                    "health_fortune": health_result,
                    "study_fortune": study_result,
                    "family_fortune": family_result
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Phase 2 확장 운세 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"Phase 2 확장 운세 분석 실패: {str(e)}")

@router.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "saju-analysis", "version": "2.0-refactored-phase2"}

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
            "/love-fortune - 연애운 상세 분석 ✨NEW✨",
            "/extended-fortune - 확장 운세 분석 (4개 운세) ✨1단계✨",
            "/residence-fortune - 주거운 분석 🏠",
            "/transportation-fortune - 교통운 분석 🚗",
            "/social-fortune - 소셜운 분석 📱",
            "/hobby-fortune - 취미운 분석 🎨",
            "/career-fortune - 직업운 상세 분석 💼 ✨Phase2✨",
            "/health-fortune - 건강운 세분화 🏥 ✨Phase2✨",
            "/study-fortune - 학업/자기계발운 📚 ✨Phase2✨",
            "/family-fortune - 가족운 👨‍👩‍👧‍👦 ✨Phase2✨",
            "/extended-fortune-phase2 - Phase 2 통합 분석 🔮 ✨Phase2✨",
            "/ai-chat - AI 대화형 해석",
            "/suggested-questions - 개인화된 예상 질문 생성 🤖 ✨NEW✨",
            "/ai-usage - AI 사용량 조회", 
            "/ai-test - AI 연결 테스트",
            "/health - 헬스 체크",
            "/test - 이 테스트"
        ]
    }