"""
궁합 분석 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.compatibility import CompatibilityRequest, CompatibilityResponse
from app.services.compatibility_analyzer import compatibility_analyzer
import logging
from typing import Dict, Any
import traceback
from datetime import datetime

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
async def analyze_compatibility(request: CompatibilityRequest):
    """
    궁합 분석 API
    
    Args:
        request: 두 사람의 출생 정보
    
    Returns:
        궁합 분석 결과
    """
    try:
        logger.info(f"=== 궁합 분석 요청 시작 ===")
        logger.info(f"Person1: {request.person1.name} ({request.person1.year}.{request.person1.month}.{request.person1.day})")
        logger.info(f"Person2: {request.person2.name} ({request.person2.year}.{request.person2.month}.{request.person2.day})")
        
        # 1. 입력 검증
        _validate_compatibility_request(request)
        
        # 2. 궁합 분석 실행
        logger.info("궁합 분석 실행 중...")
        analysis_result = compatibility_analyzer.analyze_compatibility(request)
        logger.info(f"궁합 분석 완료. 총점: {analysis_result.total_score}점")
        
        # 3. dict로 변환
        analysis_dict = safe_convert_to_dict(analysis_result)
        logger.info(f"변환 완료. 등급: {analysis_result.grade}")
        
        # 4. 응답 데이터 구성
        response_data = {
            "success": True,
            "data": analysis_dict,
            "persons_info": {
                "person1": {
                    "name": request.person1.name,
                    "birth_date": f"{request.person1.year}년 {request.person1.month}월 {request.person1.day}일 {request.person1.hour}시",
                    "gender": "남성" if request.person1.gender.lower() in ["male", "m"] else "여성"
                },
                "person2": {
                    "name": request.person2.name,
                    "birth_date": f"{request.person2.year}년 {request.person2.month}월 {request.person2.day}일 {request.person2.hour}시",
                    "gender": "남성" if request.person2.gender.lower() in ["male", "m"] else "여성"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("궁합 분석 응답 데이터 생성 완료")
        return JSONResponse(content=response_data)
        
    except ValueError as e:
        logger.error(f"입력 검증 오류: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"궁합 분석 중 오류 발생: {e}")
        logger.error(f"상세 에러: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"궁합 분석 실패: {str(e)}")

def _validate_compatibility_request(request: CompatibilityRequest):
    """궁합 분석 요청 검증"""
    # Person1 검증
    _validate_person_info(request.person1, "첫 번째 사람")
    
    # Person2 검증  
    _validate_person_info(request.person2, "두 번째 사람")
    
    # 동일인 체크
    if (request.person1.year == request.person2.year and
        request.person1.month == request.person2.month and
        request.person1.day == request.person2.day and
        request.person1.hour == request.person2.hour):
        raise ValueError("같은 사람의 정보를 입력할 수 없습니다.")

def _validate_person_info(person, person_label: str):
    """개인 정보 검증"""
    if not (1900 <= person.year <= 2100):
        raise ValueError(f"{person_label} 년도는 1900-2100 사이여야 합니다.")
    if not (1 <= person.month <= 12):
        raise ValueError(f"{person_label} 월은 1-12 사이여야 합니다.")
    if not (1 <= person.day <= 31):
        raise ValueError(f"{person_label} 일은 1-31 사이여야 합니다.")
    if not (0 <= person.hour <= 23):
        raise ValueError(f"{person_label} 시간은 0-23 사이여야 합니다.")
    if person.gender.lower() not in ["male", "female", "m", "f"]:
        raise ValueError(f"{person_label} 성별은 male, female, M, F 중 하나여야 합니다.")

@router.get("/test")
async def test_endpoint():
    """API 테스트"""
    return {
        "message": "궁합 분석 API가 정상 작동중입니다! 💕",
        "version": "1.0.0",
        "endpoints": [
            "/analyze - 궁합 분석",
            "/test - 이 테스트"
        ],
        "sample_request": {
            "person1": {
                "name": "홍길동",
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 14,
                "gender": "male"
            },
            "person2": {
                "name": "김영희",
                "year": 1992,
                "month": 8, 
                "day": 20,
                "hour": 10,
                "gender": "female"
            }
        }
    }

@router.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "compatibility-analysis", "version": "1.0.0"}