"""
궁합 분석을 위한 핵심 사주 분석 기능
SAJU 서비스의 핵심 기능만 추출
"""
from typing import Dict, Any
from app.database.connection import get_manseryuk_db

class SajuCore:
    """궁합 분석을 위한 사주 핵심 기능"""
    
    # 오행 정보
    WUXING_MAP = {
        '甲': '목', '乙': '목',  # 천간
        '丙': '화', '丁': '화',
        '戊': '토', '己': '토',
        '庚': '금', '辛': '금',
        '壬': '수', '癸': '수',
        '寅': '목', '卯': '목',  # 지지
        '巳': '화', '午': '화',
        '辰': '토', '戌': '토', '丑': '토', '未': '토',
        '申': '금', '酉': '금',
        '子': '수', '亥': '수'
    }
    
    def __init__(self):
        self.db = get_manseryuk_db()
    
    def get_palja(self, year: int, month: int, day: int, hour: int, gender: str) -> Dict[str, str]:
        """사주팔자 계산"""
        try:
            # 만세력 DB에서 출생일 데이터 가져오기
            birth_data = self.db.GetBirth(year, month, day)
            if not birth_data:
                raise ValueError(f"만세력 데이터를 찾을 수 없습니다: {year}-{month}-{day}")
            
            # 첫 번째 레코드 사용
            data = birth_data[0]
            
            # 시간 변환
            time_ji = self.db.GetTime(hour)
            if not time_ji:
                raise ValueError(f"잘못된 시간입니다: {hour}")
            
            # 기본적인 사주팔자 구성 (간단화)
            return {
                "year_gan": data[4],   # 년간
                "year_ji": data[5],    # 년지
                "month_gan": data[6],  # 월간
                "month_ji": data[7],   # 월지
                "day_gan": data[8],    # 일간
                "day_ji": data[9],     # 일지
                "hour_gan": self._get_hour_gan(data[8], hour),  # 시간
                "hour_ji": time_ji[0]  # 시지
            }
        except Exception as e:
            raise ValueError(f"사주팔자 계산 실패: {e}")
    
    def get_wuxing(self, palja: Dict[str, str]) -> Dict[str, int]:
        """오행 분석"""
        wuxing_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
        
        # 사주팔자의 각 요소를 오행으로 변환
        elements = [
            palja["year_gan"], palja["year_ji"],
            palja["month_gan"], palja["month_ji"], 
            palja["day_gan"], palja["day_ji"],
            palja["hour_gan"], palja["hour_ji"]
        ]
        
        for element in elements:
            if element in self.WUXING_MAP:
                wuxing = self.WUXING_MAP[element]
                wuxing_count[wuxing] += 1
        
        return wuxing_count
    
    def get_ten_stars(self, palja: Dict[str, str]) -> Dict[str, Any]:
        """십성 분석 (간단화)"""
        day_gan = palja["day_gan"]
        day_wuxing = self.WUXING_MAP.get(day_gan, "목")
        
        return {
            "day_master": day_gan,
            "day_master_wuxing": day_wuxing,
            "strength": "중간",  # 간단화
            "main_stars": ["정관", "정재"]  # 간단화
        }
    
    def _get_hour_gan(self, day_gan: str, hour: int) -> str:
        """시간에 따른 천간 계산 (간단화)"""
        # 실제로는 복잡한 계산이 필요하지만 간단화
        gan_cycle = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        day_index = gan_cycle.index(day_gan) if day_gan in gan_cycle else 0
        hour_index = (day_index * 2 + hour // 2) % 10
        return gan_cycle[hour_index]

# 전역 인스턴스
saju_core = SajuCore()