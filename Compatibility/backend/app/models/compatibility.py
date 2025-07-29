from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime

class PersonInfo(BaseModel):
    """개인 정보"""
    name: str = Field(..., description="이름")
    year: int = Field(..., ge=1900, le=2100, description="출생년도")
    month: int = Field(..., ge=1, le=12, description="출생월")
    day: int = Field(..., ge=1, le=31, description="출생일")
    hour: int = Field(..., ge=0, le=23, description="출생시간")
    gender: str = Field(..., pattern="^(male|female|M|F)$", description="성별")

class CompatibilityRequest(BaseModel):
    """궁합 분석 요청"""
    person1: PersonInfo = Field(..., description="첫 번째 사람")
    person2: PersonInfo = Field(..., description="두 번째 사람")
    
class PillarCompatibility(BaseModel):
    """사주팔자 궁합"""
    year_compatibility: float = Field(..., description="년주 궁합 점수")
    month_compatibility: float = Field(..., description="월주 궁합 점수")
    day_compatibility: float = Field(..., description="일주 궁합 점수")
    hour_compatibility: float = Field(..., description="시주 궁합 점수")
    overall_score: float = Field(..., description="전체 궁합 점수")

class WuxingCompatibility(BaseModel):
    """오행 궁합"""
    balance_score: float = Field(..., description="오행 균형 점수")
    harmony_elements: List[str] = Field(..., description="조화로운 오행")
    conflict_elements: List[str] = Field(..., description="충돌하는 오행")
    compatibility_type: str = Field(..., description="궁합 유형")

class TenStarsCompatibility(BaseModel):
    """십성 궁합"""
    dominant_relationship: str = Field(..., description="주도적 관계")
    support_level: float = Field(..., description="지원 정도")
    conflict_level: float = Field(..., description="갈등 정도")
    harmony_score: float = Field(..., description="조화 점수")

class CompatibilityAnalysis(BaseModel):
    """종합 궁합 분석 결과"""
    total_score: float = Field(..., description="총 궁합 점수")
    grade: str = Field(..., description="궁합 등급")
    pillar_compatibility: PillarCompatibility
    wuxing_compatibility: WuxingCompatibility
    ten_stars_compatibility: TenStarsCompatibility
    
    # 상세 해석
    strengths: List[str] = Field(..., description="궁합의 장점")
    weaknesses: List[str] = Field(..., description="주의할 점")
    advice: List[str] = Field(..., description="관계 개선 조언")
    
    # 분야별 궁합
    love_compatibility: float = Field(..., description="연애 궁합")
    marriage_compatibility: float = Field(..., description="결혼 궁합")
    business_compatibility: float = Field(..., description="사업 궁합")
    friendship_compatibility: float = Field(..., description="우정 궁합")

class CompatibilityResponse(BaseModel):
    """궁합 분석 응답"""
    success: bool = Field(True, description="성공 여부")
    data: Optional[CompatibilityAnalysis] = Field(None, description="분석 결과")
    persons_info: Optional[Dict[str, Any]] = Field(None, description="분석 대상자 정보")
    timestamp: Optional[str] = Field(None, description="분석 시각")
    
class AICompatibilityInterpretation(BaseModel):
    """AI 궁합 해석"""
    summary: str = Field(..., description="궁합 종합 요약")
    detailed_analysis: str = Field(..., description="상세 분석")
    relationship_advice: str = Field(..., description="관계 조언")
    future_outlook: str = Field(..., description="미래 전망")
    compatibility_keywords: List[str] = Field(..., description="궁합 키워드")