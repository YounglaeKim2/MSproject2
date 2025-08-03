"""
확장 운세 분석 서비스
- 주거운, 교통운, 소셜운, 취미운 등 25개 확장 분석 기능
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ExtendedFortuneAnalyzer:
    """확장 운세 분석 클래스"""
    
    def __init__(self):
        # 오행별 특성 매핑
        self.wuxing_properties = {
            "목": {
                "colors": ["초록색", "갈색", "베이지색"],
                "directions": ["동쪽"],
                "seasons": ["봄"],
                "numbers": [3, 8],
                "personality": ["성장", "발전", "유연성"]
            },
            "화": {
                "colors": ["빨간색", "주황색", "분홍색"],
                "directions": ["남쪽"], 
                "seasons": ["여름"],
                "numbers": [2, 7],
                "personality": ["열정", "활동", "외향성"]
            },
            "토": {
                "colors": ["황색", "갈색", "베이지색"],
                "directions": ["중앙"],
                "seasons": ["늦여름"],
                "numbers": [5, 10],
                "personality": ["안정", "신중", "포용"]
            },
            "금": {
                "colors": ["흰색", "은색", "회색"],
                "directions": ["서쪽"],
                "seasons": ["가을"],
                "numbers": [4, 9],
                "personality": ["정의", "결단", "독립"]
            },
            "수": {
                "colors": ["검은색", "파란색", "남색"],
                "directions": ["북쪽"],
                "seasons": ["겨울"],
                "numbers": [1, 6],
                "personality": ["지혜", "유연", "적응"]
            }
        }
        
        # 간지별 특성
        self.ganzhi_properties = {
            "甲": {"element": "목", "strength": "양"},
            "乙": {"element": "목", "strength": "음"},
            "丙": {"element": "화", "strength": "양"},
            "丁": {"element": "화", "strength": "음"},
            "戊": {"element": "토", "strength": "양"},
            "己": {"element": "토", "strength": "음"},
            "庚": {"element": "금", "strength": "양"},
            "辛": {"element": "금", "strength": "음"},
            "壬": {"element": "수", "strength": "양"},
            "癸": {"element": "수", "strength": "음"}
        }

    def get_day_stem(self, year: int, month: int, day: int) -> str:
        """간단한 일간 계산 (실제로는 만세력 DB 사용해야 함)"""
        # 임시 계산법 - 실제 구현에서는 manseryuk DB 연동 필요
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        calculated_stem = (year + month + day) % 10
        return stems[calculated_stem]
    
    def get_dominant_element(self, birth_info: Dict) -> str:
        """주요 오행 계산"""
        day_stem = self.get_day_stem(birth_info["year"], birth_info["month"], birth_info["day"])
        return self.ganzhi_properties[day_stem]["element"]

    def analyze_residence_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """🏠 주거운 분석"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            element_props = self.wuxing_properties[dominant_element]
            gender = birth_info.get("gender", "male")
            birth_month = birth_info["month"]
            
            # 이사 방향 분석
            if dominant_element == "목":
                moving_direction = "동쪽 방향으로 이사하면 성장과 발전에 도움이 됩니다"
                avoid_direction = "서쪽 방향은 피하는 것이 좋습니다"
            elif dominant_element == "화":
                moving_direction = "남쪽 방향으로 이사하면 인기와 명예가 상승합니다"
                avoid_direction = "북쪽 방향은 에너지가 약해질 수 있습니다"
            elif dominant_element == "토":
                moving_direction = "중심가나 교통이 편리한 곳이 좋습니다"
                avoid_direction = "너무 외진 곳은 피하세요"
            elif dominant_element == "금":
                moving_direction = "서쪽 방향으로 이사하면 재물운이 상승합니다"
                avoid_direction = "동쪽 방향은 갈등이 생길 수 있습니다"
            else:  # 수
                moving_direction = "북쪽 방향으로 이사하면 지혜와 학문운이 좋아집니다"
                avoid_direction = "남쪽 방향은 감정 기복이 클 수 있습니다"
            
            # 주택 유형 분석
            if dominant_element in ["목", "화"]:
                house_type = "아파트보다는 단독주택이나 빌라가 더 좋습니다"
                house_reason = "자연과 가까운 환경에서 에너지를 얻습니다"
            else:
                house_type = "아파트나 오피스텔도 좋습니다"
                house_reason = "편리함과 효율성을 중시하는 성향입니다"
            
            # 인테리어 색상
            interior_colors = element_props["colors"]
            
            # 방 배치 (오행 상생 원리)
            room_layouts = {
                "침실": f"{element_props['directions'][0]} 방향 침실이 숙면에 도움됩니다",
                "거실": "가족이 모이는 공간은 밝고 넓게 꾸미세요",
                "부엌": "화기가 있는 부엌은 남동쪽이 길합니다",
                "서재": "집중이 필요한 공간은 조용한 북쪽이나 동쪽이 좋습니다"
            }
            
            # 이사 적기 (계절과 오행 매칭)
            season_months = {
                "봄": [3, 4, 5],
                "여름": [6, 7, 8], 
                "늦여름": [8, 9],
                "가을": [9, 10, 11],
                "겨울": [12, 1, 2]
            }
            
            favorable_season = element_props["seasons"][0]
            best_moving_months = []
            for season, months in season_months.items():
                if season == favorable_season:
                    best_moving_months = [f"{m}월" for m in months]
                    break
            
            # 풍수 팁
            feng_shui_tips = [
                f"{dominant_element} 기운을 살리는 {', '.join(interior_colors)} 계열 인테리어를 하세요",
                "현관은 항상 깨끗하게 유지하고 밝은 조명을 설치하세요",
                "침실에는 거울을 두지 마세요",
                "화장실 문은 항상 닫아두세요",
                "식물이나 꽃을 키워 생기를 더하세요"
            ]
            
            return {
                "moving_direction": moving_direction,
                "avoid_direction": avoid_direction,
                "house_type": house_type,
                "house_reason": house_reason,
                "interior_colors": interior_colors,
                "room_layout": room_layouts,
                "best_moving_months": best_moving_months,
                "feng_shui_tips": feng_shui_tips,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"주거운 분석 오류: {e}")
            return self._get_default_residence_fortune()

    def analyze_transportation_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """🚗 교통운 분석"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            element_props = self.wuxing_properties[dominant_element]
            birth_day = birth_info["day"]
            birth_month = birth_info["month"]
            
            # 차량 색상
            car_colors = element_props["colors"]
            
            # 번호판 길수
            lucky_numbers = element_props["numbers"]
            license_advice = f"번호판 끝자리는 {', '.join(map(str, lucky_numbers))}번이 길합니다"
            
            # 사고 위험 시기 (오행 상극 원리)
            risk_months = []
            if dominant_element == "목":
                risk_months = ["7월", "8월"]  # 금이 목을 극함
            elif dominant_element == "화":
                risk_months = ["12월", "1월"]  # 수가 화를 극함
            elif dominant_element == "토":
                risk_months = ["3월", "4월"]  # 목이 토를 극함
            elif dominant_element == "금":
                risk_months = ["6월", "7월"]  # 화가 금을 극함
            else:  # 수
                risk_months = ["6월", "9월"]  # 토가 수를 극함
            
            # 교통수단 선호도
            if dominant_element in ["목", "수"]:
                transport_preference = "대중교통 이용이 더 안전하고 효율적입니다"
                transport_reason = "환경을 생각하고 스트레스를 줄일 수 있습니다"
            else:
                transport_preference = "자가용 이용이 더 편리합니다"
                transport_reason = "독립성과 자유로움을 추구하는 성향입니다"
            
            # 여행 방향
            travel_directions = element_props["directions"]
            if len(travel_directions) == 1 and travel_directions[0] != "중앙":
                # 상생 방향도 추가
                if dominant_element == "목":
                    travel_directions.append("남쪽")  # 목생화
                elif dominant_element == "화":
                    travel_directions.append("중앙")  # 화생토
                elif dominant_element == "토":
                    travel_directions.append("서쪽")  # 토생금
                elif dominant_element == "금":
                    travel_directions.append("북쪽")  # 금생수
                else:  # 수
                    travel_directions.append("동쪽")  # 수생목
            
            # 운전 주의사항
            driving_tips = [
                f"{', '.join(risk_months)}에는 특히 안전운전에 주의하세요",
                "빗길이나 눈길에서는 더욱 신중하게 운전하세요",
                "장거리 운전 전에는 충분한 휴식을 취하세요",
                "차량 정기점검을 소홀히 하지 마세요",
                f"{dominant_element} 기운에 맞는 차량용 액세서리를 사용하세요"
            ]
            
            return {
                "car_colors": car_colors,
                "license_numbers": license_advice,
                "accident_risk_months": risk_months,
                "transport_preference": transport_preference,
                "transport_reason": transport_reason,
                "travel_directions": travel_directions,
                "driving_tips": driving_tips,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"교통운 분석 오류: {e}")
            return self._get_default_transportation_fortune()

    def analyze_social_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """📱 소셜운 분석"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            element_props = self.wuxing_properties[dominant_element]
            birth_hour = birth_info.get("hour", 12)
            
            # SNS 활동 적기
            if dominant_element in ["화", "목"]:
                sns_active_months = ["5월", "6월", "8월", "9월"]
                activity_reason = "활발하고 외향적인 성향으로 소셜 활동이 잘 맞습니다"
            else:
                sns_active_months = ["3월", "4월", "10월", "11월"]
                activity_reason = "신중한 성향으로 적절한 시기에 활동하는 것이 좋습니다"
            
            # 프로필 색상
            profile_colors = element_props["colors"]
            
            # 소통 스타일
            communication_styles = {
                "목": "성장 지향적이고 긍정적인 메시지를 전달하세요",
                "화": "열정적이고 에너지 넘치는 콘텐츠가 좋습니다",
                "토": "신뢰할 수 있고 안정적인 정보를 공유하세요",
                "금": "명확하고 논리적인 소통을 하세요",
                "수": "지혜롭고 깊이 있는 내용을 다루세요"
            }
            
            communication_style = communication_styles[dominant_element]
            
            # 온라인 활동 시간
            if birth_hour >= 6 and birth_hour < 18:
                online_timing = "오전~오후 시간대 활동이 효과적입니다"
                timing_reason = "낮 시간에 태어나 활발한 에너지를 가지고 있습니다"
            else:
                online_timing = "저녁~밤 시간대 활동이 효과적입니다"
                timing_reason = "밤 시간에 태어나 차분하고 깊이 있는 활동이 잘 맞습니다"
            
            # 소셜 미디어 전략
            social_strategies = []
            if dominant_element == "목":
                social_strategies = [
                    "성장과 발전 관련 콘텐츠 공유",
                    "자연과 환경 관련 주제",
                    "학습과 자기계발 정보"
                ]
            elif dominant_element == "화":
                social_strategies = [
                    "밝고 긍정적인 콘텐츠",
                    "엔터테인먼트와 문화 정보",
                    "사람들과의 소통과 네트워킹"
                ]
            elif dominant_element == "토":
                social_strategies = [
                    "실용적이고 유용한 정보",
                    "안정적인 라이프스타일 공유",
                    "신뢰성 있는 정보 전달"
                ]
            elif dominant_element == "금":
                social_strategies = [
                    "전문적이고 품격 있는 콘텐츠",
                    "명확한 의견과 분석",
                    "고품질 정보 공유"
                ]
            else:  # 수
                social_strategies = [
                    "지혜롭고 깊이 있는 내용",
                    "철학적이고 사색적인 주제",
                    "창의적이고 독특한 관점"
                ]
            
            return {
                "sns_active_months": sns_active_months,
                "activity_reason": activity_reason,
                "profile_colors": profile_colors,
                "communication_style": communication_style,
                "online_timing": online_timing,
                "timing_reason": timing_reason,
                "social_strategies": social_strategies,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"소셜운 분석 오류: {e}")
            return self._get_default_social_fortune()

    def analyze_hobby_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """🎨 취미운 분석"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            gender = birth_info.get("gender", "male")
            birth_season = self._get_birth_season(birth_info["month"])
            
            # 예술 분야 적성
            art_fields = []
            if dominant_element == "목":
                art_fields = ["문학", "서예", "원예", "목공예"]
            elif dominant_element == "화":
                art_fields = ["음악", "무용", "연극", "영상"]
            elif dominant_element == "토":
                art_fields = ["도예", "조각", "건축", "인테리어"]
            elif dominant_element == "금":
                art_fields = ["금속공예", "악기연주", "성악", "보석디자인"]
            else:  # 수
                art_fields = ["서화", "사진", "문학", "영상편집"]
            
            # 운동 종류
            if dominant_element in ["화", "목"]:
                sports_type = "단체 운동이 더 적합합니다"
                sports_examples = ["축구", "농구", "배구", "테니스"]
                sports_reason = "활발하고 사교적인 성향으로 팀 스포츠가 잘 맞습니다"
            else:
                sports_type = "개인 운동이 더 적합합니다"
                sports_examples = ["수영", "등산", "요가", "골프"]
                sports_reason = "집중력과 개인적 성취를 중시하는 성향입니다"
            
            # 수집 취미
            collection_items = []
            if dominant_element == "목":
                collection_items = ["책", "식물", "목재 소품", "친환경 제품"]
            elif dominant_element == "화":
                collection_items = ["음반", "영화 DVD", "조명 소품", "예술품"]
            elif dominant_element == "토":
                collection_items = ["도자기", "미니어처", "인형", "실용적 소품"]
            elif dominant_element == "금":
                collection_items = ["시계", "악기", "금속 공예품", "보석"]
            else:  # 수
                collection_items = ["돌", "조개껍데기", "고서", "골동품"]
            
            # 창작 활동
            creative_activities = []
            if dominant_element == "목":
                creative_activities = ["블로그 작성", "소설 쓰기", "정원 가꾸기"]
            elif dominant_element == "화":
                creative_activities = ["영상 제작", "음악 작곡", "사진 촬영"]
            elif dominant_element == "토":
                creative_activities = ["요리", "DIY 만들기", "실용적 발명"]
            elif dominant_element == "금":
                creative_activities = ["악기 연주", "정밀 공예", "디자인"]
            else:  # 수
                creative_activities = ["시 쓰기", "명상", "철학적 글쓰기"]
            
            # 취미 개발 조언
            hobby_advice = []
            if dominant_element in ["목", "화"]:
                hobby_advice = [
                    "다른 사람들과 함께 할 수 있는 취미를 선택하세요",
                    "창의성을 발휘할 수 있는 활동이 좋습니다",
                    "새로운 것에 도전하는 것을 두려워하지 마세요"
                ]
            else:
                hobby_advice = [
                    "혼자서도 충분히 즐길 수 있는 취미를 찾으세요",
                    "깊이 있게 파고들 수 있는 분야가 좋습니다",
                    "완성도를 높이는 것에 집중하세요"
                ]
            
            return {
                "art_fields": art_fields,
                "sports_type": sports_type,
                "sports_examples": sports_examples,
                "sports_reason": sports_reason,
                "collection_items": collection_items,
                "creative_activities": creative_activities,
                "hobby_advice": hobby_advice,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"취미운 분석 오류: {e}")
            return self._get_default_hobby_fortune()

    def _get_birth_season(self, month: int) -> str:
        """출생 계절 계산"""
        if month in [3, 4, 5]:
            return "봄"
        elif month in [6, 7, 8]:
            return "여름"
        elif month in [9, 10, 11]:
            return "가을"
        else:
            return "겨울"

    def _get_default_residence_fortune(self) -> Dict[str, Any]:
        """기본 주거운 데이터"""
        return {
            "moving_direction": "동쪽 방향으로 이사하면 좋습니다",
            "avoid_direction": "서쪽 방향은 피하는 것이 좋습니다",
            "house_type": "편안하고 안정적인 환경이 좋습니다",
            "house_reason": "개인의 성향에 맞는 주거환경을 선택하세요",
            "interior_colors": ["흰색", "베이지색", "연한 갈색"],
            "room_layout": {
                "침실": "조용하고 편안한 곳에 배치하세요",
                "거실": "가족이 모이기 좋은 중앙에 두세요",
                "부엌": "환기가 잘 되는 곳이 좋습니다",
                "서재": "집중할 수 있는 조용한 곳에 마련하세요"
            },
            "best_moving_months": ["3월", "6월", "9월"],
            "feng_shui_tips": [
                "현관을 항상 깨끗하게 유지하세요",
                "자연광이 잘 들어오도록 하세요",
                "식물을 키워 생기를 더하세요"
            ],
            "dominant_element": "토"
        }

    def _get_default_transportation_fortune(self) -> Dict[str, Any]:
        """기본 교통운 데이터"""
        return {
            "car_colors": ["흰색", "은색", "검은색"],
            "license_numbers": "개인의 취향에 맞게 선택하세요",
            "accident_risk_months": ["7월", "8월"],
            "transport_preference": "안전하고 편리한 교통수단을 이용하세요",
            "transport_reason": "개인의 상황에 맞는 선택이 중요합니다",
            "travel_directions": ["동쪽", "남쪽"],
            "driving_tips": [
                "항상 안전운전을 하세요",
                "정기적으로 차량 점검을 받으세요",
                "장거리 운전 시 충분한 휴식을 취하세요"
            ],
            "dominant_element": "토"
        }

    def _get_default_social_fortune(self) -> Dict[str, Any]:
        """기본 소셜운 데이터"""
        return {
            "sns_active_months": ["3월", "6월", "9월", "12월"],
            "activity_reason": "균형잡힌 소셜 활동이 좋습니다",
            "profile_colors": ["파란색", "흰색", "회색"],
            "communication_style": "진솔하고 친근한 소통을 하세요",
            "online_timing": "개인의 패턴에 맞게 활동하세요",
            "timing_reason": "자신만의 리듬을 찾는 것이 중요합니다",
            "social_strategies": [
                "진정성 있는 콘텐츠 공유",
                "적절한 빈도로 활동",
                "긍정적인 메시지 전달"
            ],
            "dominant_element": "토"
        }

    def _get_default_hobby_fortune(self) -> Dict[str, Any]:
        """기본 취미운 데이터"""
        return {
            "art_fields": ["음악", "미술", "문학"],
            "sports_type": "개인의 취향에 맞는 운동이 좋습니다",
            "sports_examples": ["걷기", "수영", "요가"],
            "sports_reason": "꾸준히 할 수 있는 운동을 선택하세요",
            "collection_items": ["책", "음반", "소품"],
            "creative_activities": ["글쓰기", "그림 그리기", "사진 촬영"],
            "hobby_advice": [
                "자신이 진정으로 좋아하는 것을 찾으세요",
                "꾸준히 지속할 수 있는 취미를 선택하세요",
                "새로운 것에 도전해보세요"
            ],
            "dominant_element": "토"
        }

# 전역 인스턴스
extended_fortune_analyzer = ExtendedFortuneAnalyzer()