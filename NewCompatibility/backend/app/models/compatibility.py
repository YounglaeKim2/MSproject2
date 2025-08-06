"""
API 요청/응답 모델 정의
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

class BirthInfoRequest(BaseModel):
    """출생 정보 요청 모델"""
    year: int = Field(..., description="출생년도", ge=1900, le=2030)
    month: int = Field(..., description="출생월", ge=1, le=12)
    day: int = Field(..., description="출생일", ge=1, le=31)
    hour: int = Field(..., description="출생시간", ge=0, le=23)
    gender: str = Field(..., description="성별", pattern="^(male|female)$")
    name: str = Field(..., description="이름", min_length=1, max_length=20)

class CompatibilityRequest(BaseModel):
    """궁합 분석 요청 모델"""
    person1: BirthInfoRequest = Field(..., description="첫 번째 사람 정보")
    person2: BirthInfoRequest = Field(..., description="두 번째 사람 정보")

class SajuAnalysisResponse(BaseModel):
    """사주 분석 응답 모델"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None
    response_time: Optional[float] = None
    timestamp: Optional[str] = None

class CompatibilityScore(BaseModel):
    """궁합 점수"""
    overall: int = Field(..., description="전체 점수", ge=0, le=100)
    love: int = Field(..., description="연애 궁합", ge=0, le=100)
    marriage: int = Field(..., description="결혼 궁합", ge=0, le=100)
    communication: int = Field(..., description="소통 궁합", ge=0, le=100)
    values: int = Field(..., description="가치관 궁합", ge=0, le=100)

class CompatibilityDetail(BaseModel):
    """궁합 상세 분석"""
    strengths: List[str] = Field(default_factory=list, description="강점")
    weaknesses: List[str] = Field(default_factory=list, description="약점")
    advice: List[str] = Field(default_factory=list, description="조언")
    relationship_tips: List[str] = Field(default_factory=list, description="관계 팁")

class CompatibilityAnalysisResponse(BaseModel):
    """궁합 분석 응답 모델"""
    success: bool
    person1_name: Optional[str] = None
    person2_name: Optional[str] = None
    compatibility_score: Optional[CompatibilityScore] = None
    analysis_details: Optional[CompatibilityDetail] = None
    summary: Optional[str] = None
    detailed_analysis: Optional[str] = None
    analysis_time: Optional[str] = None
    error: Optional[str] = None
    message: Optional[str] = None

class HealthCheckResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    service: str = "NewCompatibility"
    version: str = "1.0.0"
    timestamp: str
    dependencies: Optional[Dict[str, Any]] = None

class ServiceInfoResponse(BaseModel):
    """서비스 정보 응답 모델"""
    name: str = "NewCompatibility API"
    version: str = "1.0.0"
    description: str = "SAJU API 기반 궁합 분석 서비스"
    endpoints: List[str] = Field(default_factory=list)
    dependencies: Dict[str, str] = Field(default_factory=dict)
