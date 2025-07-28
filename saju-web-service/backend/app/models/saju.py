from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class BirthInfoRequest(BaseModel):
    """사주 생성을 위한 출생 정보"""
    year: int = Field(..., ge=1900, le=2100, description="출생년도")
    month: int = Field(..., ge=1, le=12, description="출생월")
    day: int = Field(..., ge=1, le=31, description="출생일")
    hour: int = Field(..., ge=0, le=23, description="출생시간")
    gender: str = Field(..., pattern="^(male|female)$", description="성별 (male/female)")
    name: Optional[str] = Field(None, description="이름")

class SajuPaljaResponse(BaseModel):
    """사주팔자 응답"""
    year_gan: str = Field(..., description="년간")
    year_ji: str = Field(..., description="년지")
    month_gan: str = Field(..., description="월간")
    month_ji: str = Field(..., description="월지")
    day_gan: str = Field(..., description="일간")
    day_ji: str = Field(..., description="일지")
    hour_gan: str = Field(..., description="시간")
    hour_ji: str = Field(..., description="시지")

class WuXingAnalysis(BaseModel):
    """오행 분석 결과"""
    wood: int = Field(..., description="목 개수")
    fire: int = Field(..., description="화 개수")
    earth: int = Field(..., description="토 개수")
    metal: int = Field(..., description="금 개수")
    water: int = Field(..., description="수 개수")
    strength: str = Field(..., description="일간 강약 (strong/weak)")
    use_god: str = Field(..., description="용신")
    avoid_god: str = Field(..., description="기신")

class TenStarsAnalysis(BaseModel):
    """십성 분석 결과"""
    bijian: int = Field(0, description="비견")
    겁재: int = Field(0, description="겁재")
    식신: int = Field(0, description="식신")
    상관: int = Field(0, description="상관")
    편재: int = Field(0, description="편재")
    정재: int = Field(0, description="정재")
    편관: int = Field(0, description="편관")
    정관: int = Field(0, description="정관")
    편인: int = Field(0, description="편인")
    정인: int = Field(0, description="정인")

class SajuAnalysisResponse(BaseModel):
    """완전한 사주 분석 결과"""
    palja: SajuPaljaResponse
    wuxing: WuXingAnalysis
    ten_stars: TenStarsAnalysis
    personality: Dict[str, Any] = Field(..., description="성격 분석")
    career: Dict[str, Any] = Field(..., description="직업운")
    health: Dict[str, Any] = Field(..., description="건강운")
    relationship: Dict[str, Any] = Field(..., description="대인관계운")
    fortune: Dict[str, Any] = Field(..., description="재물운")

class ErrorResponse(BaseModel):
    """에러 응답"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 에러 정보")