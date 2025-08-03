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

    def analyze_career_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """💼 직업운 상세 분석"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            element_props = self.wuxing_properties[dominant_element]
            birth_year = birth_info["year"]
            current_year = datetime.now().year
            age = current_year - birth_year
            
            # 이직 시기 분석
            if dominant_element in ["목", "화"]:
                job_change_months = ["3월", "6월", "9월"]
                change_reason = "성장과 발전을 추구하는 성향으로 새로운 도전이 좋습니다"
            else:
                job_change_months = ["1월", "4월", "10월"]
                change_reason = "신중한 성향으로 충분한 준비 후 이직하는 것이 좋습니다"
            
            # 승진운 분석
            if age < 30:
                promotion_advice = "실무 능력을 키우고 인맥을 넓히는 시기입니다"
                promotion_timing = "올해 하반기부터 기회가 보입니다"
            elif age < 40:
                promotion_advice = "리더십을 발휘하고 책임감을 보이는 시기입니다"
                promotion_timing = "내년이 승진의 적기입니다"
            else:
                promotion_advice = "경험과 지혜를 바탕으로 후배를 이끄는 시기입니다"
                promotion_timing = "안정적인 위치에서 영향력을 발휘하세요"
            
            # 창업운 분석
            if dominant_element in ["화", "금"]:
                startup_suitability = "창업에 적합한 기운을 가지고 있습니다"
                startup_fields = ["서비스업", "IT", "컨설팅", "디자인"]
                startup_timing = "올해 말~내년 초가 창업하기 좋은 시기입니다"
            else:
                startup_suitability = "안정적인 직장에서 경력을 쌓는 것이 더 좋습니다"
                startup_fields = ["교육", "제조", "유통", "부동산"]
                startup_timing = "충분한 경험과 자본을 준비한 후 도전하세요"
            
            # 부업 추천
            side_jobs = []
            if dominant_element == "목":
                side_jobs = ["온라인 강의", "블로그 운영", "식물 판매", "편집/교정"]
            elif dominant_element == "화":
                side_jobs = ["유튜브 크리에이터", "이벤트 기획", "사진/영상", "온라인 쇼핑몰"]
            elif dominant_element == "토":
                side_jobs = ["부동산 투자", "요리 클래스", "핸드메이드", "펜션 운영"]
            elif dominant_element == "금":
                side_jobs = ["투자 상담", "온라인 쇼핑몰", "귀금속 거래", "악기 레슨"]
            else:  # 수
                side_jobs = ["번역", "온라인 강의", "컨설팅", "투자"]
            
            # 직장 인간관계
            if dominant_element in ["화", "목"]:
                relationship_style = "적극적으로 소통하고 협력하는 스타일이 좋습니다"
                networking_advice = "다양한 사람들과 네트워킹을 확대하세요"
            else:
                relationship_style = "신뢰할 수 있는 소수와 깊은 관계를 맺는 것이 좋습니다"
                networking_advice = "품질 높은 인맥을 만들어가세요"
            
            return {
                "job_change_months": job_change_months,
                "change_reason": change_reason,
                "promotion_advice": promotion_advice,
                "promotion_timing": promotion_timing,
                "startup_suitability": startup_suitability,
                "startup_fields": startup_fields,
                "startup_timing": startup_timing,
                "side_jobs": side_jobs,
                "relationship_style": relationship_style,
                "networking_advice": networking_advice,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"직업운 분석 오류: {e}")
            return self._get_default_career_fortune()

    def analyze_health_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """🏥 건강운 세분화"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            birth_month = birth_info["month"]
            gender = birth_info.get("gender", "male")
            
            # 장기별 건강 주의사항
            organ_care = {}
            if dominant_element == "목":
                organ_care = {
                    "간담": "간 건강에 주의하고 스트레스 관리가 중요합니다",
                    "눈": "눈의 피로를 줄이고 충분한 수면을 취하세요",
                    "근육": "유연성 운동과 스트레칭을 꾸준히 하세요"
                }
            elif dominant_element == "화":
                organ_care = {
                    "심장": "심혈관 건강을 위해 규칙적인 운동을 하세요",
                    "혈액순환": "혈액순환을 위해 따뜻하게 보온하세요",
                    "신경": "과도한 흥분을 피하고 마음의 안정을 찾으세요"
                }
            elif dominant_element == "토":
                organ_care = {
                    "소화기": "규칙적인 식사와 소화에 좋은 음식을 드세요",
                    "비장": "단 음식을 적당히 섭취하고 과식을 피하세요",
                    "근육": "근력 운동으로 체력을 기르세요"
                }
            elif dominant_element == "금":
                organ_care = {
                    "폐": "호흡기 건강을 위해 공기 좋은 곳에서 운동하세요",
                    "대장": "섬유질이 풍부한 음식을 섭취하세요",
                    "피부": "건조하지 않게 보습에 신경 쓰세요"
                }
            else:  # 수
                organ_care = {
                    "신장": "수분 섭취를 충분히 하고 염분을 줄이세요",
                    "방광": "요로 건강을 위해 청결을 유지하세요",
                    "뼈": "칼슘 섭취와 골밀도 검사를 정기적으로 받으세요"
                }
            
            # 운동 추천
            exercise_recommendations = []
            if dominant_element in ["목", "화"]:
                exercise_recommendations = [
                    "유산소 운동 (달리기, 자전거, 수영)",
                    "팀 스포츠 (축구, 농구, 배구)",
                    "댄스나 에어로빅",
                    "등산이나 트레킹"
                ]
            else:
                exercise_recommendations = [
                    "요가나 태극권",
                    "근력 운동 (웨이트 트레이닝)",
                    "산책이나 가벼운 조깅",
                    "수영이나 아쿠아로빅"
                ]
            
            # 식단 조언
            diet_advice = []
            if dominant_element == "목":
                diet_advice = [
                    "신선한 채소와 과일을 많이 섭취하세요",
                    "신맛이 나는 음식이 도움됩니다",
                    "과도한 음주는 피하세요"
                ]
            elif dominant_element == "화":
                diet_advice = [
                    "쓴맛이 나는 음식을 적당히 드세요",
                    "매운 음식은 적당히 조절하세요",
                    "충분한 수분 섭취가 중요합니다"
                ]
            elif dominant_element == "토":
                diet_advice = [
                    "단맛이 나는 자연 식품을 드세요",
                    "소화가 잘 되는 음식을 선택하세요",
                    "규칙적인 식사 시간을 지키세요"
                ]
            elif dominant_element == "금":
                diet_advice = [
                    "매운맛 음식을 적당히 드세요",
                    "호흡기에 좋은 배, 도라지 등을 섭취하세요",
                    "기름진 음식은 줄이세요"
                ]
            else:  # 수
                diet_advice = [
                    "짠맛을 적당히 조절하세요",
                    "신장에 좋은 검은콩, 검은깨를 드세요",
                    "찬 음식보다는 따뜻한 음식을 선택하세요"
                ]
            
            # 수면 패턴
            if birth_month in [3, 4, 5, 6, 7, 8]:  # 봄여름생
                sleep_pattern = "밤 11시 이전에 잠자리에 들고 7시간 이상 수면하세요"
                sleep_reason = "양기가 강한 시기에 태어나 충분한 휴식이 필요합니다"
            else:  # 가을겨울생
                sleep_pattern = "밤 10시 이전에 잠자리에 들고 8시간 이상 수면하세요"
                sleep_reason = "음기가 강한 시기에 태어나 깊은 잠이 중요합니다"
            
            # 건강검진 시기
            if dominant_element in ["목", "화"]:
                checkup_timing = ["3월", "9월"]
                checkup_focus = "간기능, 심혈관 검사를 중심으로 받으세요"
            else:
                checkup_timing = ["6월", "12월"]
                checkup_focus = "소화기, 호흡기 검사를 중심으로 받으세요"
            
            return {
                "organ_care": organ_care,
                "exercise_recommendations": exercise_recommendations,
                "diet_advice": diet_advice,
                "sleep_pattern": sleep_pattern,
                "sleep_reason": sleep_reason,
                "checkup_timing": checkup_timing,
                "checkup_focus": checkup_focus,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"건강운 분석 오류: {e}")
            return self._get_default_health_fortune()

    def analyze_study_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """📚 학업/자기계발운"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            birth_hour = birth_info.get("hour", 12)
            age = datetime.now().year - birth_info["year"]
            
            # 학습 적기
            if dominant_element in ["목", "수"]:
                study_months = ["2월", "3월", "9월", "10월"]
                study_reason = "집중력이 높아지는 시기로 깊이 있는 학습이 가능합니다"
            else:
                study_months = ["4월", "5월", "8월", "11월"]
                study_reason = "활발한 에너지로 다양한 분야 학습이 효과적입니다"
            
            # 시험운
            if birth_hour >= 9 and birth_hour <= 15:  # 오전~오후
                exam_timing = "오전 시간대 시험이 유리합니다"
                exam_preparation = "아침 일찍 일어나서 공부하는 습관을 기르세요"
            else:
                exam_timing = "오후~저녁 시간대 시험이 유리합니다"
                exam_preparation = "저녁 시간에 집중해서 공부하는 것이 좋습니다"
            
            # 자격증 추천
            certifications = []
            if dominant_element == "목":
                certifications = [
                    "교육 관련 자격증 (교원자격증, 평생교육사)",
                    "환경 관련 자격증 (환경기사, 조경기사)",
                    "언어 관련 자격증 (토익, 토플, 번역사)",
                    "상담 관련 자격증 (상담심리사, 청소년상담사)"
                ]
            elif dominant_element == "화":
                certifications = [
                    "IT 관련 자격증 (정보처리기사, 컴활)",
                    "문화예술 자격증 (문화예술교육사, 큐레이터)",
                    "방송통신 자격증 (방송통신기사, PD)",
                    "마케팅 자격증 (디지털마케팅, 광고기획)"
                ]
            elif dominant_element == "토":
                certifications = [
                    "부동산 자격증 (공인중개사, 감정평가사)",
                    "건설 관련 자격증 (건축기사, 토목기사)",
                    "요리 자격증 (조리기능사, 영양사)",
                    "경영 자격증 (경영지도사, 회계사)"
                ]
            elif dominant_element == "금":
                certifications = [
                    "금융 자격증 (은행FP, 투자상담사)",
                    "법률 자격증 (법무사, 변리사)",
                    "기계 자격증 (기계기사, 설비기사)",
                    "음악 자격증 (음악치료사, 실용음악)"
                ]
            else:  # 수
                certifications = [
                    "물류 자격증 (물류관리사, 유통관리사)",
                    "수산업 자격증 (수산기사, 해양기사)",
                    "의료 자격증 (간호사, 물리치료사)",
                    "철학/종교 자격증 (종교지도자, 상담사)"
                ]
            
            # 독서 추천
            reading_genres = []
            if dominant_element == "목":
                reading_genres = ["자기계발서", "교육학", "심리학", "환경과학"]
            elif dominant_element == "화":
                reading_genres = ["경영서", "마케팅", "IT기술서", "예술서"]
            elif dominant_element == "토":
                reading_genres = ["실용서", "요리책", "건강서", "부동산"]
            elif dominant_element == "금":
                reading_genres = ["경제서", "투자서", "법률서", "음악서"]
            else:  # 수
                reading_genres = ["철학서", "역사서", "과학서", "종교서"]
            
            # 어학 학습
            if dominant_element in ["목", "수"]:
                language_aptitude = "언어 학습 능력이 뛰어납니다"
                language_methods = [
                    "읽기와 쓰기 중심 학습",
                    "문법과 구조 이해에 집중",
                    "독서를 통한 자연스러운 습득"
                ]
            else:
                language_aptitude = "말하기와 듣기 학습이 더 효과적입니다"
                language_methods = [
                    "회화와 듣기 중심 학습",
                    "실제 대화 상황 연습",
                    "미디어를 활용한 학습"
                ]
            
            return {
                "study_months": study_months,
                "study_reason": study_reason,
                "exam_timing": exam_timing,
                "exam_preparation": exam_preparation,
                "certifications": certifications,
                "reading_genres": reading_genres,
                "language_aptitude": language_aptitude,
                "language_methods": language_methods,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"학업운 분석 오류: {e}")
            return self._get_default_study_fortune()

    def analyze_family_fortune(self, birth_info: Dict) -> Dict[str, Any]:
        """👨‍👩‍👧‍👦 가족운"""
        try:
            dominant_element = self.get_dominant_element(birth_info)
            gender = birth_info.get("gender", "male")
            birth_month = birth_info["month"]
            
            # 부모 관계
            if dominant_element in ["목", "수"]:
                parent_relationship = "부모님과 깊이 있는 소통을 하는 것이 좋습니다"
                parent_advice = [
                    "정기적으로 안부를 묻고 대화 시간을 가지세요",
                    "부모님의 지혜와 경험을 존중하세요",
                    "효도는 마음보다 실천이 중요합니다"
                ]
            else:
                parent_relationship = "부모님과 활발한 교류를 하는 것이 좋습니다"
                parent_advice = [
                    "함께 여행이나 외출을 계획하세요",
                    "부모님께 새로운 경험을 제안해보세요",
                    "자주 만나서 즐거운 시간을 보내세요"
                ]
            
            # 형제자매 관계
            if dominant_element in ["화", "목"]:
                sibling_relationship = "형제자매와 협력적인 관계를 만들어가세요"
                sibling_advice = "서로 도움을 주고받으며 가족의 화합을 이루세요"
            else:
                sibling_relationship = "형제자매와 적당한 거리를 유지하는 것이 좋습니다"
                sibling_advice = "각자의 독립성을 존중하며 필요할 때 지원하세요"
            
            # 자녀운 (결혼한 경우)
            if gender == "male":
                children_timing = ["봄", "가을"] if dominant_element in ["목", "금"] else ["여름", "겨울"]
                children_advice = "자녀와의 소통에서 아버지의 역할을 충실히 하세요"
                parenting_style = "규칙과 원칙을 세우되 사랑으로 이끌어주세요"
            else:
                children_timing = ["여름", "겨울"] if dominant_element in ["화", "수"] else ["봄", "가을"]
                children_advice = "자녀의 감정을 이해하고 공감하는 어머니가 되세요"
                parenting_style = "따뜻한 사랑으로 감싸주되 독립심도 길러주세요"
            
            # 가족 모임
            if birth_month in [3, 4, 5, 9, 10, 11]:  # 봄가을생
                family_gathering = "봄과 가을에 가족 모임을 자주 가지세요"
                gathering_activities = ["등산", "나들이", "문화활동", "전통명절 중시"]
            else:  # 여름겨울생
                family_gathering = "여름과 겨울에 가족 모임을 자주 가지세요"
                gathering_activities = ["해수욕", "스키", "실내활동", "연말연시 모임"]
            
            # 세대 갈등 해결
            if dominant_element in ["토", "금"]:
                generation_gap = "전통과 현대의 조화를 이루는 역할을 하세요"
                conflict_resolution = [
                    "서로 다른 세대의 관점을 이해하려 노력하세요",
                    "중재자 역할을 통해 가족 화합을 이끌어주세요",
                    "전통을 존중하면서도 변화를 수용하세요"
                ]
            else:
                generation_gap = "소통의 다리 역할을 하는 것이 좋습니다"
                conflict_resolution = [
                    "열린 마음으로 대화의 장을 마련하세요",
                    "새로운 방식으로 가족간 소통을 시도하세요",
                    "서로의 차이를 인정하고 존중하세요"
                ]
            
            return {
                "parent_relationship": parent_relationship,
                "parent_advice": parent_advice,
                "sibling_relationship": sibling_relationship,
                "sibling_advice": sibling_advice,
                "children_timing": children_timing,
                "children_advice": children_advice,
                "parenting_style": parenting_style,
                "family_gathering": family_gathering,
                "gathering_activities": gathering_activities,
                "generation_gap": generation_gap,
                "conflict_resolution": conflict_resolution,
                "dominant_element": dominant_element
            }
            
        except Exception as e:
            logger.error(f"가족운 분석 오류: {e}")
            return self._get_default_family_fortune()

    def _get_default_career_fortune(self) -> Dict[str, Any]:
        """기본 직업운 데이터"""
        return {
            "job_change_months": ["3월", "6월", "9월"],
            "change_reason": "신중하게 계획하여 이직하는 것이 좋습니다",
            "promotion_advice": "꾸준한 노력과 성실함으로 인정받으세요",
            "promotion_timing": "내년이 승진의 기회입니다",
            "startup_suitability": "충분한 준비 후 창업을 고려하세요",
            "startup_fields": ["서비스업", "컨설팅"],
            "startup_timing": "경험을 쌓은 후 도전하세요",
            "side_jobs": ["온라인 강의", "블로그 운영"],
            "relationship_style": "신뢰할 수 있는 관계를 만들어가세요",
            "networking_advice": "진정성 있는 인맥을 구축하세요",
            "dominant_element": "토"
        }

    def _get_default_health_fortune(self) -> Dict[str, Any]:
        """기본 건강운 데이터"""
        return {
            "organ_care": {
                "전신": "균형잡힌 생활습관을 유지하세요",
                "면역": "면역력 강화에 신경 쓰세요"
            },
            "exercise_recommendations": ["걷기", "요가", "수영"],
            "diet_advice": [
                "규칙적인 식사를 하세요",
                "영양 균형을 맞추세요",
                "충분한 수분을 섭취하세요"
            ],
            "sleep_pattern": "7-8시간 규칙적인 수면을 취하세요",
            "sleep_reason": "충분한 휴식이 건강의 기본입니다",
            "checkup_timing": ["6월", "12월"],
            "checkup_focus": "정기적인 종합검진을 받으세요",
            "dominant_element": "토"
        }

    def _get_default_study_fortune(self) -> Dict[str, Any]:
        """기본 학업운 데이터"""
        return {
            "study_months": ["3월", "6월", "9월", "12월"],
            "study_reason": "꾸준한 학습이 가장 중요합니다",
            "exam_timing": "본인에게 맞는 시간대를 찾으세요",
            "exam_preparation": "충분한 준비와 계획이 필요합니다",
            "certifications": ["컴활", "토익", "기본 자격증"],
            "reading_genres": ["자기계발서", "실용서"],
            "language_aptitude": "꾸준한 노력으로 향상 가능합니다",
            "language_methods": ["체계적인 학습", "반복 연습"],
            "dominant_element": "토"
        }

    def _get_default_family_fortune(self) -> Dict[str, Any]:
        """기본 가족운 데이터"""
        return {
            "parent_relationship": "부모님과 좋은 관계를 유지하세요",
            "parent_advice": [
                "정기적으로 안부를 묻으세요",
                "효도하는 마음을 실천하세요"
            ],
            "sibling_relationship": "형제자매와 화목한 관계를 만드세요",
            "sibling_advice": "서로 도움을 주고받으세요",
            "children_timing": ["봄", "가을"],
            "children_advice": "자녀와의 소통을 중요하게 생각하세요",
            "parenting_style": "사랑과 규칙의 균형을 맞추세요",
            "family_gathering": "정기적인 가족 모임을 가지세요",
            "gathering_activities": ["식사", "여행", "문화활동"],
            "generation_gap": "서로를 이해하려 노력하세요",
            "conflict_resolution": [
                "열린 마음으로 대화하세요",
                "서로의 입장을 존중하세요"
            ],
            "dominant_element": "토"
        }

# 전역 인스턴스
extended_fortune_analyzer = ExtendedFortuneAnalyzer()