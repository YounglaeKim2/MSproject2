from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class BirthRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    gender: str
    name: str

@router.post("/analyze")
async def analyze_saju_simple(data: BirthRequest):
    """간단한 사주 분석 API"""
    try:
        logger.info(f"사주 분석 요청: {data.dict()}")
        
        # 고정된 응답 반환 (테스트용)
        result = {
            "basic_info": {
                "name": data.name,
                "birth_date": f"{data.year}년 {data.month}월 {data.day}일 {data.hour}시",
                "gender": "남성" if data.gender == "male" else "여성"
            },
            "saju_palja": {
                "year_pillar": {"stem": "갑", "branch": "자"},
                "month_pillar": {"stem": "을", "branch": "축"},
                "day_pillar": {"stem": "병", "branch": "인"},
                "hour_pillar": {"stem": "정", "branch": "묘"}
            },
            "wuxing_analysis": {
                "목": 2, "화": 1, "토": 1, "금": 2, "수": 2
            },
            "interpretations": {
                "personality": "성격이 온화하고 부드러우며, 타인을 배려하는 마음이 깊습니다. 감정이 풍부하고 예술적 감각이 뛰어납니다.",
                "career": "창작 분야나 서비스업에서 능력을 발휘할 수 있습니다. 협력을 중시하는 분야에서 성공 가능성이 높습니다.",
                "health": "전반적으로 건강하나 스트레스 관리에 주의가 필요합니다. 규칙적인 운동과 충분한 휴식을 권합니다.",
                "relationships": "인간관계가 원만하고 많은 사람들에게 사랑받습니다. 결혼운도 양호한 편입니다.",
                "wealth": "꾸준한 노력을 통해 안정적인 재물을 축적할 수 있습니다. 투기보다는 저축이 유리합니다."
            }
        }
        
        logger.info("사주 분석 완료")
        return result
        
    except Exception as e:
        logger.error(f"사주 분석 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@router.get("/test")
async def test_simple():
    """테스트 엔드포인트"""
    return {"message": "간단한 사주 API가 작동 중입니다."}