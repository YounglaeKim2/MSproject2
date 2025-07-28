from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from app.database.connection import manseryuk_db
from app.models.saju import BirthInfoRequest, SajuPaljaResponse, WuXingAnalysis, TenStarsAnalysis

class SajuAnalyzer:
    """사주 분석 엔진"""
    
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
    
    # 십성 계산을 위한 관계 정의
    SHISHEN_MAP = {
        ('목', '목', True): '비견',   # 같은 오행, 같은 음양
        ('목', '목', False): '겁재',  # 같은 오행, 다른 음양
        ('목', '화', True): '식신',   # 일간이 생하는 오행, 같은 음양
        ('목', '화', False): '상관',  # 일간이 생하는 오행, 다른 음양
        ('목', '토', True): '편재',   # 일간이 극하는 오행, 같은 음양
        ('목', '토', False): '정재',  # 일간이 극하는 오행, 다른 음양
        ('목', '금', True): '편관',   # 일간을 극하는 오행, 같은 음양
        ('목', '금', False): '정관',  # 일간을 극하는 오행, 다른 음양
        ('목', '수', True): '편인',   # 일간을 생하는 오행, 같은 음양
        ('목', '수', False): '정인',  # 일간을 생하는 오행, 다른 음양
    }
    
    # 오행 상생상극 관계
    GENERATE_CYCLE = {'목': '화', '화': '토', '토': '금', '금': '수', '수': '목'}
    OVERCOME_CYCLE = {'목': '토', '화': '금', '토': '수', '금': '목', '수': '화'}
    
    # 천간/지지 순서 (대운 계산용)
    HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 음양 구분
    YANG_STEMS = ['甲', '丙', '戊', '庚', '壬']
    YIN_STEMS = ['乙', '丁', '己', '辛', '癸']
    
    def __init__(self):
        self.db = manseryuk_db
    
    def analyze_saju(self, birth_info: BirthInfoRequest) -> Dict[str, Any]:
        """완전한 사주 분석"""
        # 1. 사주팔자 추출
        palja = self.extract_palja(birth_info)
        
        # 2. 오행 분석
        wuxing = self.analyze_wuxing(palja)
        
        # 3. 십성 분석
        ten_stars = self.analyze_ten_stars(palja)
        
        # 4. 성격 분석
        personality = self.analyze_personality(palja, wuxing, ten_stars)
        
        # 5. 운세 분석
        career = self.analyze_career(palja, wuxing, ten_stars)
        health = self.analyze_health(palja, wuxing)
        relationship = self.analyze_relationship(palja, wuxing, ten_stars)
        fortune = self.analyze_fortune(palja, wuxing, ten_stars)
        
        # 6. 대운 분석 추가
        daeun = self.calculate_daeun(birth_info, palja)
        
        return {
            "palja": palja,
            "wuxing": wuxing,
            "ten_stars": ten_stars,
            "personality": personality,
            "career": career,
            "health": health,
            "relationship": relationship,
            "fortune": fortune,
            "daeun": daeun
        }
    
    def extract_palja(self, birth_info: BirthInfoRequest) -> SajuPaljaResponse:
        """출생 정보로부터 사주팔자 추출"""
        # 만세력 DB에서 해당 날짜 데이터 조회
        birth_data = self.db.get_birth_data(birth_info.year, birth_info.month, birth_info.day)
        
        if not birth_data:
            raise ValueError("해당 날짜의 만세력 데이터를 찾을 수 없습니다.")
        
        # 시주 계산
        hour_ji_han, hour_ji_kor = self.db.get_time_ganzhi(birth_info.hour)
        
        # 시간에 따른 천간 계산 (일간을 기준으로)
        day_gan = birth_data['cd_hdganjee'][0]  # 일간 (한문)
        hour_gan = self._calculate_hour_gan(day_gan, birth_info.hour)
        
        return SajuPaljaResponse(
            year_gan=birth_data['cd_hyganjee'][0],   # 년간
            year_ji=birth_data['cd_hyganjee'][1],    # 년지
            month_gan=birth_data['cd_hmganjee'][0],  # 월간
            month_ji=birth_data['cd_hmganjee'][1],   # 월지
            day_gan=birth_data['cd_hdganjee'][0],    # 일간
            day_ji=birth_data['cd_hdganjee'][1],     # 일지
            hour_gan=hour_gan,                       # 시간
            hour_ji=hour_ji_han                      # 시지
        )
    
    def _calculate_hour_gan(self, day_gan: str, hour: int) -> str:
        """일간을 기준으로 시간 계산"""
        # 간단한 시간 계산 로직 (실제로는 더 복잡한 계산 필요)
        gan_order = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        day_index = gan_order.index(day_gan)
        
        # 시간대별 시간 계산 (대략적)
        time_index = (hour + 1) // 2
        hour_gan_index = (day_index * 2 + time_index) % 10
        
        return gan_order[hour_gan_index]
    
    def analyze_wuxing(self, palja: SajuPaljaResponse) -> WuXingAnalysis:
        """오행 분석"""
        # 사주팔자에서 각 글자의 오행 추출
        chars = [
            palja.year_gan, palja.year_ji,
            palja.month_gan, palja.month_ji,
            palja.day_gan, palja.day_ji,
            palja.hour_gan, palja.hour_ji
        ]
        
        # 오행 카운트
        wuxing_count = {'목': 0, '화': 0, '토': 0, '금': 0, '수': 0}
        
        for char in chars:
            if char in self.WUXING_MAP:
                wuxing = self.WUXING_MAP[char]
                wuxing_count[wuxing] += 1
        
        # 일간 강약 판단 (간단한 로직)
        day_gan_wuxing = self.WUXING_MAP[palja.day_gan]
        supporting_count = wuxing_count[day_gan_wuxing]  # 같은 오행
        
        # 일간을 생조하는 오행 추가
        for wuxing, target in self.GENERATE_CYCLE.items():
            if target == day_gan_wuxing:
                supporting_count += wuxing_count[wuxing]
        
        strength = "strong" if supporting_count >= 3 else "weak"
        
        # 용신/기신 도출 (간단한 로직)
        use_god = day_gan_wuxing
        avoid_god = day_gan_wuxing
        
        if strength == "strong":
            # 신강이면 설기하거나 극하는 오행이 용신
            use_god = self.GENERATE_CYCLE[day_gan_wuxing]  # 설기
            avoid_god = day_gan_wuxing
        else:
            # 신약이면 생조하는 오행이 용신
            for wuxing, target in self.GENERATE_CYCLE.items():
                if target == day_gan_wuxing:
                    use_god = wuxing
                    break
            avoid_god = self.OVERCOME_CYCLE[day_gan_wuxing]
        
        # 확장된 오행 분석 수행
        extended_analysis = self._perform_extended_wuxing_analysis(
            wuxing_count, day_gan_wuxing, strength, use_god, avoid_god
        )
        
        return WuXingAnalysis(
            wood=wuxing_count['목'],
            fire=wuxing_count['화'],
            earth=wuxing_count['토'],
            metal=wuxing_count['금'],
            water=wuxing_count['수'],
            strength=strength,
            use_god=use_god,
            avoid_god=avoid_god,
            extended_analysis=extended_analysis
        )
    
    def _perform_extended_wuxing_analysis(self, wuxing_count: dict, day_gan_wuxing: str, 
                                        strength: str, use_god: str, avoid_god: str) -> dict:
        """확장된 오행 분석 수행"""
        total_count = sum(wuxing_count.values())
        
        # 오행별 강도 및 백분율 계산
        wuxing_details = {}
        for wuxing, count in wuxing_count.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            strength_level = self._calculate_wuxing_strength(count, percentage)
            
            wuxing_details[wuxing] = {
                'count': count,
                'percentage': round(percentage, 1),
                'strength': strength_level,
                'meaning': self._get_wuxing_meaning(wuxing),
                'characteristics': self._get_wuxing_characteristics(wuxing)
            }
        
        # 오행 균형 분석
        balance_analysis = self._analyze_wuxing_balance(wuxing_count, day_gan_wuxing)
        
        # 성격 분석
        personality_analysis = self._analyze_personality_by_wuxing(wuxing_count, day_gan_wuxing)
        
        # 보완 방법 제안
        recommendations = self._generate_balance_recommendations(
            wuxing_count, day_gan_wuxing, use_god, avoid_god
        )
        
        return {
            'wuxing_details': wuxing_details,
            'balance_analysis': balance_analysis,
            'personality_analysis': personality_analysis,
            'recommendations': recommendations
        }
    
    def _calculate_wuxing_strength(self, count: int, percentage: float) -> str:
        """오행 강도 계산"""
        if count == 0:
            return "없음"
        elif percentage < 10:
            return "매우 약함"
        elif percentage < 20:
            return "약함"
        elif percentage < 30:
            return "보통"
        elif percentage < 40:
            return "강함"
        else:
            return "매우 강함"
    
    def _get_wuxing_meaning(self, wuxing: str) -> str:
        """오행 의미 반환"""
        meanings = {
            '목': "성장, 창조, 유연성, 인자함",
            '화': "열정, 활력, 표현력, 밝음",
            '토': "안정, 신뢰, 포용력, 중후함",
            '금': "절제, 정의, 결단력, 냉철함",
            '수': "지혜, 적응력, 유동성, 깊이"
        }
        return meanings.get(wuxing, "")
    
    def _get_wuxing_characteristics(self, wuxing: str) -> list:
        """오행별 특성 반환"""
        characteristics = {
            '목': ["창의적", "성장지향적", "유연한", "협력적"],
            '화': ["열정적", "표현력이 풍부한", "사교적", "활동적"],
            '토': ["안정적", "신뢰할 수 있는", "포용력이 있는", "실용적"],
            '금': ["결단력이 있는", "정의로운", "체계적", "냉정한"],
            '수': ["지혜로운", "적응력이 있는", "깊이 있는", "유연한"]
        }
        return characteristics.get(wuxing, [])
    
    def _analyze_wuxing_balance(self, wuxing_count: dict, day_gan_wuxing: str) -> dict:
        """오행 균형 분석"""
        total = sum(wuxing_count.values())
        average = total / 5
        
        excessive = []  # 과다한 오행
        deficient = []  # 부족한 오행
        
        for wuxing, count in wuxing_count.items():
            if count > average * 1.5:
                excessive.append(wuxing)
            elif count < average * 0.5:
                deficient.append(wuxing)
        
        # 균형도 점수 계산 (0-100)
        variance = sum((count - average) ** 2 for count in wuxing_count.values()) / 5
        balance_score = max(0, 100 - variance * 10)
        
        return {
            'balance_score': round(balance_score, 1),
            'excessive_elements': excessive,
            'deficient_elements': deficient,
            'dominant_element': max(wuxing_count, key=wuxing_count.get),
            'weakest_element': min(wuxing_count, key=wuxing_count.get)
        }
    
    def _analyze_personality_by_wuxing(self, wuxing_count: dict, day_gan_wuxing: str) -> dict:
        """오행 분포에 따른 성격 분석"""
        total = sum(wuxing_count.values())
        
        # 주요 성격 특성 도출
        dominant_traits = []
        for wuxing, count in wuxing_count.items():
            percentage = (count / total * 100) if total > 0 else 0
            if percentage > 25:  # 25% 이상이면 주요 특성
                traits = self._get_wuxing_characteristics(wuxing)
                dominant_traits.extend(traits[:2])  # 상위 2개 특성
        
        # 성격 유형 판단
        personality_type = self._determine_personality_type(wuxing_count, day_gan_wuxing)
        
        # 강점과 약점 분석
        strengths, weaknesses = self._analyze_strengths_weaknesses(wuxing_count)
        
        return {
            'dominant_traits': dominant_traits[:5],  # 상위 5개 특성
            'personality_type': personality_type,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'advice': self._generate_personality_advice(dominant_traits[:3])
        }
    
    def _determine_personality_type(self, wuxing_count: dict, day_gan_wuxing: str) -> str:
        """성격 유형 판단"""
        dominant_element = max(wuxing_count, key=wuxing_count.get)
        
        personality_types = {
            '목': "성장형 - 끊임없이 발전을 추구하는 창의적 성격",
            '화': "열정형 - 활력이 넘치고 표현력이 풍부한 외향적 성격", 
            '토': "안정형 - 신뢰할 수 있고 포용력이 있는 온화한 성격",
            '금': "완벽형 - 원칙을 중시하고 결단력이 있는 냉정한 성격",
            '수': "지혜형 - 깊이 있게 사고하고 적응력이 뛰어난 유연한 성격"
        }
        
        return personality_types.get(dominant_element, "균형형 - 다양한 특성이 조화된 성격")
    
    def _analyze_strengths_weaknesses(self, wuxing_count: dict) -> tuple:
        """강점과 약점 분석"""
        total = sum(wuxing_count.values())
        
        strengths = []
        weaknesses = []
        
        for wuxing, count in wuxing_count.items():
            percentage = (count / total * 100) if total > 0 else 0
            
            if percentage > 25:  # 강한 오행의 장점
                if wuxing == '목':
                    strengths.append("창의력과 성장 잠재력이 뛰어남")
                elif wuxing == '화':
                    strengths.append("열정과 표현력이 풍부함")
                elif wuxing == '토':
                    strengths.append("안정감과 신뢰성이 높음")
                elif wuxing == '금':
                    strengths.append("결단력과 원칙성이 강함")
                elif wuxing == '수':
                    strengths.append("지혜와 적응력이 뛰어남")
            
            elif percentage < 10:  # 약한 오행의 단점
                if wuxing == '목':
                    weaknesses.append("창의력이나 성장 동력이 부족할 수 있음")
                elif wuxing == '화':
                    weaknesses.append("열정이나 표현력이 부족할 수 있음")
                elif wuxing == '토':
                    weaknesses.append("안정감이나 포용력이 부족할 수 있음")
                elif wuxing == '금':
                    weaknesses.append("결단력이나 원칙성이 부족할 수 있음")
                elif wuxing == '수':
                    weaknesses.append("지혜나 적응력이 부족할 수 있음")
        
        return strengths[:3], weaknesses[:3]
    
    def _generate_personality_advice(self, dominant_traits: list) -> str:
        """성격에 따른 조언 생성"""
        if "창의적" in dominant_traits:
            return "창의적 재능을 발휘할 수 있는 분야에서 활동하시면 좋겠습니다."
        elif "열정적" in dominant_traits:
            return "열정을 바탕으로 적극적인 도전을 통해 성과를 이루시길 바랍니다."
        elif "안정적" in dominant_traits:
            return "신뢰를 바탕으로 한 꾸준한 노력이 큰 성과로 이어질 것입니다."
        elif "결단력이 있는" in dominant_traits:
            return "명확한 목표 설정과 체계적인 접근으로 성공을 이루시길 바랍니다."
        elif "지혜로운" in dominant_traits:
            return "깊이 있는 사고와 유연한 대응으로 어려움을 극복하시길 바랍니다."
        else:
            return "다양한 재능을 균형 있게 발휘하여 조화로운 삶을 이루시길 바랍니다."
    
    def _generate_balance_recommendations(self, wuxing_count: dict, day_gan_wuxing: str, 
                                        use_god: str, avoid_god: str) -> dict:
        """오행 보완 방법 제안"""
        total = sum(wuxing_count.values())
        
        # 부족한 오행 찾기
        deficient_elements = []
        for wuxing, count in wuxing_count.items():
            percentage = (count / total * 100) if total > 0 else 0
            if percentage < 15:  # 15% 미만이면 부족
                deficient_elements.append(wuxing)
        
        recommendations = {
            'lifestyle': [],
            'colors': [],
            'directions': [],
            'foods': [],
            'activities': [],
            'career_advice': [],
            'health_advice': [],
            'relationship_advice': []
        }
        
        # 용신(有利한 오행) 보강 방법
        if use_god in deficient_elements or wuxing_count[use_god] < 2:
            recommendations.update(self._get_element_recommendations(use_god))
        
        # 부족한 오행별 보완 방법
        for element in deficient_elements:
            element_rec = self._get_element_recommendations(element)
            for key in recommendations:
                recommendations[key].extend(element_rec[key])
        
        # 중복 제거
        for key in recommendations:
            recommendations[key] = list(set(recommendations[key]))[:3]  # 상위 3개만
        
        return recommendations
    
    def _get_element_recommendations(self, element: str) -> dict:
        """특정 오행의 보완 방법"""
        recommendations = {
            '목': {
                'lifestyle': ['동쪽 방향 활동', '아침 시간 활용', '식물 기르기'],
                'colors': ['초록색', '연두색', '청색'],
                'directions': ['동쪽', '동남쪽'],
                'foods': ['녹색 채소', '신맛 음식', '간 기능에 좋은 음식'],
                'activities': ['독서', '학습', '창작 활동'],
                'career_advice': ['교육 분야', '상담 업무', '예술 창작', '환경 관련 직업'],
                'health_advice': ['간 기능 관리', '눈 건강 주의', '스트레스 해소'],
                'relationship_advice': ['따뜻한 배려심 발휘', '성장을 함께하는 관계', '인내심 기르기']
            },
            '화': {
                'lifestyle': ['남쪽 방향 활동', '정오 시간 활용', '밝은 조명'],
                'colors': ['빨간색', '주황색', '분홍색'],
                'directions': ['남쪽'],
                'foods': ['쓴맛 음식', '심장에 좋은 음식', '따뜻한 음식'],
                'activities': ['운동', '사회 활동', '예술 활동'],
                'career_advice': ['방송 관련', '마케팅 업무', '영업직', '엔터테인먼트 업계'],
                'health_advice': ['심장 건강 관리', '혈압 주의', '충분한 휴식'],
                'relationship_advice': ['밝은 에너지 전달', '적극적 소통', '감정 조절 연습']
            },
            '토': {
                'lifestyle': ['중앙 위치 선호', '오후 시간 활용', '안정적 환경'],
                'colors': ['노란색', '갈색', '베이지색'],
                'directions': ['중앙', '남서쪽', '북동쪽'],
                'foods': ['단맛 음식', '위장에 좋은 음식', '곡류'],
                'activities': ['명상', '요가', '안정적 취미'],
                'career_advice': ['부동산 업무', '건설 관련', '농업 분야', '요식업'],
                'health_advice': ['소화기 건강 관리', '규칙적 식사', '적당한 운동'],
                'relationship_advice': ['신뢰감 조성', '포용력 발휘', '안정적 관계 유지']
            },
            '금': {
                'lifestyle': ['서쪽 방향 활동', '저녁 시간 활용', '깔끔한 환경'],
                'colors': ['흰색', '회색', '금색'],
                'directions': ['서쪽', '북서쪽'],
                'foods': ['매운맛 음식', '폐에 좋은 음식', '견과류'],
                'activities': ['정리 정돈', '체계적 학습', '규칙적 운동'],
                'career_advice': ['금융 업무', '법무 관련', '기계 기술', 'IT 분야'],
                'health_advice': ['호흡기 건강 관리', '피부 관리', '정기 검진'],
                'relationship_advice': ['원칙 있는 관계', '명확한 소통', '상호 존중']
            },
            '수': {
                'lifestyle': ['북쪽 방향 활동', '밤 시간 활용', '조용한 환경'],
                'colors': ['검은색', '남색', '진청색'],
                'directions': ['북쪽'],
                'foods': ['짠맛 음식', '신장에 좋은 음식', '해산물'],
                'activities': ['수영', '독서', '깊이 있는 사고'],
                'career_advice': ['연구 업무', '학술 분야', '물류 관련', '컨설팅'],
                'health_advice': ['신장 기능 관리', '수분 섭취', '과로 주의'],
                'relationship_advice': ['깊이 있는 대화', '지혜로운 조언', '차분한 관계']
            }
        }
        
        return recommendations.get(element, {
            'lifestyle': [], 'colors': [], 'directions': [], 'foods': [], 'activities': [], 
            'career_advice': [], 'health_advice': [], 'relationship_advice': []
        })
    
    def analyze_ten_stars(self, palja: SajuPaljaResponse) -> TenStarsAnalysis:
        """십성 분석"""
        day_gan = palja.day_gan
        day_gan_wuxing = self.WUXING_MAP[day_gan]
        
        # 천간의 음양 판단 (간단한 로직)
        yang_gan = ['甲', '丙', '戊', '庚', '壬']
        day_gan_yang = day_gan in yang_gan
        
        chars = [palja.year_gan, palja.month_gan, palja.hour_gan]  # 일간 제외
        
        ten_stars_count = {
            'bijian': 0, '겁재': 0, '식신': 0, '상관': 0, '편재': 0,
            '정재': 0, '편관': 0, '정관': 0, '편인': 0, '정인': 0
        }
        
        for char in chars:
            if char in self.WUXING_MAP:
                char_wuxing = self.WUXING_MAP[char]
                char_yang = char in yang_gan
                
                # 십성 판단 로직 (간단한 버전)
                if char_wuxing == day_gan_wuxing:
                    if char_yang == day_gan_yang:
                        ten_stars_count['bijian'] += 1
                    else:
                        ten_stars_count['겁재'] += 1
        
        return TenStarsAnalysis(**ten_stars_count)
    
    def analyze_personality(self, palja: SajuPaljaResponse, wuxing: WuXingAnalysis, ten_stars: TenStarsAnalysis) -> Dict[str, Any]:
        """성격 분석"""
        day_gan = palja.day_gan
        day_gan_wuxing = self.WUXING_MAP[day_gan]
        
        personality = {
            "basic_nature": "",
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # 일간 오행에 따른 기본 성격
        if day_gan_wuxing == '목':
            personality["basic_nature"] = "성장과 발전을 추구하는 진취적인 성격"
            personality["strengths"] = ["창의적", "적응력", "성장 지향적"]
            personality["weaknesses"] = ["고집", "우유부단"]
        elif day_gan_wuxing == '화':
            personality["basic_nature"] = "열정적이고 밝은 에너지를 가진 성격"
            personality["strengths"] = ["열정적", "사교적", "리더십"]
            personality["weaknesses"] = ["급함", "감정기복"]
        elif day_gan_wuxing == '토':
            personality["basic_nature"] = "안정적이고 신뢰할 수 있는 성격"
            personality["strengths"] = ["신뢰성", "안정성", "포용력"]
            personality["weaknesses"] = ["보수적", "변화 기피"]
        elif day_gan_wuxing == '금':
            personality["basic_nature"] = "의지가 강하고 원칙적인 성격"
            personality["strengths"] = ["의지력", "원칙성", "결단력"]
            personality["weaknesses"] = ["완고함", "융통성 부족"]
        elif day_gan_wuxing == '수':
            personality["basic_nature"] = "지혜롭고 유연한 성격"
            personality["strengths"] = ["지혜", "유연성", "적응력"]
            personality["weaknesses"] = ["우유부단", "소극적"]
        
        # 오행 강약에 따른 보완
        if wuxing.strength == "strong":
            personality["recommendations"].append(f"{wuxing.use_god} 기운을 활용하여 에너지를 분산시키세요")
        else:
            personality["recommendations"].append(f"{wuxing.use_god} 기운을 보강하여 자신감을 키우세요")
        
        return personality
    
    def analyze_career(self, palja: SajuPaljaResponse, wuxing: WuXingAnalysis, ten_stars: TenStarsAnalysis) -> Dict[str, Any]:
        """직업운 분석"""
        day_gan_wuxing = self.WUXING_MAP[palja.day_gan]
        
        career = {
            "suitable_fields": [],
            "career_tendency": "",
            "success_factors": [],
            "cautions": []
        }
        
        # 일간 오행에 따른 적성 분야
        if day_gan_wuxing == '목':
            career["suitable_fields"] = ["교육", "상담", "예술", "환경", "성장 산업"]
            career["career_tendency"] = "창의적이고 발전적인 분야에서 능력 발휘"
        elif day_gan_wuxing == '화':
            career["suitable_fields"] = ["방송", "마케팅", "영업", "엔터테인먼트", "서비스업"]
            career["career_tendency"] = "사람들과의 소통이 중요한 분야에서 성공"
        elif day_gan_wuxing == '토':
            career["suitable_fields"] = ["부동산", "건설", "농업", "요식업", "안정적 직장"]
            career["career_tendency"] = "안정성과 신뢰성이 요구되는 분야에 적합"
        elif day_gan_wuxing == '금':
            career["suitable_fields"] = ["금융", "법무", "기계", "IT", "정밀 기술"]
            career["career_tendency"] = "정확성과 전문성이 중요한 분야에서 두각"
        elif day_gan_wuxing == '수':
            career["suitable_fields"] = ["연구", "학술", "물류", "유통", "컨설팅"]
            career["career_tendency"] = "지혜와 분석력을 활용하는 분야에 적성"
        
        career["success_factors"] = [f"{wuxing.use_god} 기운이 강한 시기나 환경에서 성공 가능성 높음"]
        career["cautions"] = [f"{wuxing.avoid_god} 기운이 강한 시기에는 신중한 결정 필요"]
        
        return career
    
    def analyze_health(self, palja: SajuPaljaResponse, wuxing: WuXingAnalysis) -> Dict[str, Any]:
        """건강운 분석"""
        health = {
            "strong_organs": [],
            "weak_organs": [],
            "health_advice": [],
            "caution_seasons": []
        }
        
        # 오행과 장기의 대응
        organ_map = {
            '목': "간, 담낭, 신경계",
            '화': "심장, 소장, 혈액순환",
            '토': "비장, 위장, 소화기",
            '금': "폐, 대장, 호흡기",
            '수': "신장, 방광, 생식기"
        }
        
        # 강한 오행과 약한 오행 파악
        wuxing_counts = {
            '목': wuxing.wood,
            '화': wuxing.fire,
            '토': wuxing.earth,
            '금': wuxing.metal,
            '수': wuxing.water
        }
        
        max_count = max(wuxing_counts.values())
        min_count = min(wuxing_counts.values())
        
        for wuxing_name, count in wuxing_counts.items():
            if count == max_count and count > 2:
                health["strong_organs"].append(organ_map[wuxing_name])
                health["health_advice"].append(f"{wuxing_name} 기운이 강하므로 {organ_map[wuxing_name]} 관련 과로 주의")
            elif count == min_count and count < 1:
                health["weak_organs"].append(organ_map[wuxing_name])
                health["health_advice"].append(f"{wuxing_name} 기운이 약하므로 {organ_map[wuxing_name]} 관리 필요")
        
        return health
    
    def analyze_relationship(self, palja: SajuPaljaResponse, wuxing: WuXingAnalysis, ten_stars: TenStarsAnalysis) -> Dict[str, Any]:
        """대인관계 분석"""
        relationship = {
            "relationship_style": "",
            "compatibility": [],
            "social_tendency": "",
            "advice": []
        }
        
        day_gan_wuxing = self.WUXING_MAP[palja.day_gan]
        
        if day_gan_wuxing == '목':
            relationship["relationship_style"] = "성장 지향적이고 발전적인 관계 추구"
            relationship["social_tendency"] = "새로운 인맥 개발에 적극적"
        elif day_gan_wuxing == '화':
            relationship["relationship_style"] = "밝고 활발한 관계 선호"
            relationship["social_tendency"] = "사교적이고 인기가 많음"
        elif day_gan_wuxing == '토':
            relationship["relationship_style"] = "안정적이고 신뢰할 수 있는 관계 중시"
            relationship["social_tendency"] = "깊고 오래가는 관계 선호"
        elif day_gan_wuxing == '금':
            relationship["relationship_style"] = "원칙적이고 명확한 관계 추구"
            relationship["social_tendency"] = "선택적이고 신중한 교제"
        elif day_gan_wuxing == '수':
            relationship["relationship_style"] = "지혜롭고 깊이 있는 관계 선호"
            relationship["social_tendency"] = "적은 수의 깊은 관계 중시"
        
        # 상생 관계의 오행과 좋은 궁합
        for wuxing_name, target in self.GENERATE_CYCLE.items():
            if target == day_gan_wuxing:
                relationship["compatibility"].append(f"{wuxing_name} 기운의 사람과 좋은 궁합")
        
        return relationship
    
    def analyze_fortune(self, palja: SajuPaljaResponse, wuxing: WuXingAnalysis, ten_stars: TenStarsAnalysis) -> Dict[str, Any]:
        """재물운 분석"""
        fortune = {
            "wealth_tendency": "",
            "income_style": "",
            "investment_advice": [],
            "cautions": []
        }
        
        day_gan_wuxing = self.WUXING_MAP[palja.day_gan]
        
        if day_gan_wuxing == '목':
            fortune["wealth_tendency"] = "성장성 있는 투자와 사업에서 재물 증식"
            fortune["income_style"] = "꾸준한 성장을 통한 재물 축적"
        elif day_gan_wuxing == '화':
            fortune["wealth_tendency"] = "인맥과 사업 확장을 통한 재물 획득"
            fortune["income_style"] = "활발한 활동을 통한 수익 창출"
        elif day_gan_wuxing == '토':
            fortune["wealth_tendency"] = "안정적이고 확실한 투자 선호"
            fortune["income_style"] = "착실한 저축과 부동산 투자"
        elif day_gan_wuxing == '금':
            fortune["wealth_tendency"] = "정확한 분석을 통한 투자 성공"
            fortune["income_style"] = "전문 기술과 능력을 통한 고수익"
        elif day_gan_wuxing == '수':
            fortune["wealth_tendency"] = "지혜로운 판단을 통한 재테크"
            fortune["income_style"] = "정보와 지식을 활용한 수익"
        
        # 용신 활용 조언
        fortune["investment_advice"].append(f"{wuxing.use_god} 관련 분야 투자 고려")
        fortune["cautions"].append(f"{wuxing.avoid_god} 관련 분야 투자 신중")
        
        return fortune
    
    # ==================== 대운 분석 메서드들 ====================
    
    def calculate_daeun(self, birth_info: BirthInfoRequest, palja: SajuPaljaResponse) -> Dict[str, Any]:
        """대운 계산 및 분석"""
        # 1. 대운수 계산
        daeun_start_age = self._calculate_daeun_start_age(birth_info, palja)
        
        # 2. 순행/역행 판단
        is_forward = self._determine_daeun_direction(birth_info.gender, palja.year_gan)
        
        # 3. 대운 시퀀스 생성
        daeun_sequence = self._generate_daeun_sequence(palja.month_gan, palja.month_ji, is_forward)
        
        # 4. 각 대운별 분석
        daeun_analysis = []
        current_year = datetime.now().year
        birth_year = birth_info.year
        current_age = current_year - birth_year + 1
        
        for i, (gan, ji) in enumerate(daeun_sequence[:8]):  # 80세까지
            start_age = daeun_start_age + (i * 10)
            end_age = start_age + 9
            
            # 현재 대운인지 확인
            is_current = start_age <= current_age <= end_age
            
            # 대운 분석
            daeun_info = self._analyze_single_daeun(
                gan, ji, start_age, end_age, palja, is_current
            )
            
            daeun_analysis.append(daeun_info)
        
        return {
            "daeun_start_age": daeun_start_age,
            "is_forward": is_forward,
            "current_age": current_age,
            "daeun_list": daeun_analysis
        }
    
    def _calculate_daeun_start_age(self, birth_info: BirthInfoRequest, palja: SajuPaljaResponse) -> int:
        """대운수 계산 (대운 시작 나이)"""
        # 생일과 해당 월의 절기 사이의 날짜 차이를 계산
        # 간단한 계산 방식 사용 (실제로는 더 정밀한 절기 계산 필요)
        
        # 월별 절기 대략적 날짜 (실제로는 만세력 DB에서 가져와야 함)
        month_jieqi = {
            1: 4,   # 입춘
            2: 19,  # 경칩  
            3: 21,  # 청명
            4: 20,  # 입하
            5: 21,  # 망종
            6: 21,  # 소서
            7: 23,  # 입추
            8: 23,  # 처서
            9: 23,  # 한로
            10: 23, # 입동
            11: 22, # 대설
            12: 22  # 소한
        }
        
        jieqi_day = month_jieqi.get(birth_info.month, 15)
        
        # 생일과 절기의 차이 계산
        if birth_info.day < jieqi_day:
            # 절기 전에 태어남 - 이전 달 기준
            days_diff = jieqi_day - birth_info.day
        else:
            # 절기 후에 태어남 - 다음 절기까지의 날짜
            next_month = birth_info.month + 1 if birth_info.month < 12 else 1
            next_jieqi = month_jieqi.get(next_month, 15)
            days_in_month = 30  # 간단화
            days_diff = (days_in_month - birth_info.day) + next_jieqi
        
        # 3일을 1년으로 계산
        daeun_start_age = days_diff // 3
        
        # 최소 1세, 최대 10세로 제한
        return max(1, min(10, daeun_start_age))
    
    def _determine_daeun_direction(self, gender: str, year_gan: str) -> bool:
        """대운 순행/역행 판단"""
        is_yang_year = year_gan in self.YANG_STEMS
        is_male = gender.lower() == 'male'
        
        # 연주가 양이고 남성이면 순행, 연주가 양이고 여성이면 역행
        # 연주가 음이고 남성이면 역행, 연주가 음이고 여성이면 순행
        if is_yang_year:
            return is_male  # 양간 + 남성 = 순행, 양간 + 여성 = 역행
        else:
            return not is_male  # 음간 + 남성 = 역행, 음간 + 여성 = 순행
    
    def _generate_daeun_sequence(self, month_gan: str, month_ji: str, is_forward: bool) -> List[Tuple[str, str]]:
        """대운 시퀀스 생성"""
        sequence = []
        
        # 월주를 기준으로 순행/역행
        gan_index = self.HEAVENLY_STEMS.index(month_gan)
        ji_index = self.EARTHLY_BRANCHES.index(month_ji)
        
        for i in range(1, 9):  # 80세까지 (8개 대운)
            if is_forward:
                new_gan_index = (gan_index + i) % 10
                new_ji_index = (ji_index + i) % 12
            else:
                new_gan_index = (gan_index - i) % 10
                new_ji_index = (ji_index - i) % 12
            
            sequence.append((
                self.HEAVENLY_STEMS[new_gan_index],
                self.EARTHLY_BRANCHES[new_ji_index]
            ))
        
        return sequence
    
    def _analyze_single_daeun(self, gan: str, ji: str, start_age: int, end_age: int, 
                             palja: SajuPaljaResponse, is_current: bool) -> Dict[str, Any]:
        """개별 대운 분석"""
        # 대운의 오행
        gan_wuxing = self.WUXING_MAP.get(gan, '토')
        ji_wuxing = self.WUXING_MAP.get(ji, '토')
        
        # 일간과의 관계
        day_gan_wuxing = self.WUXING_MAP[palja.day_gan]
        
        # 대운의 길흉 판단
        fortune_level = self._judge_daeun_fortune(gan_wuxing, ji_wuxing, day_gan_wuxing)
        
        # 대운 특성 분석
        characteristics = self._analyze_daeun_characteristics(gan, ji, day_gan_wuxing)
        
        # 주요 이벤트 예측
        major_events = self._predict_daeun_events(gan_wuxing, ji_wuxing, day_gan_wuxing)
        
        return {
            "period": f"{start_age}세 - {end_age}세",
            "start_age": start_age,
            "end_age": end_age,
            "gan": gan,
            "ji": ji,
            "gan_wuxing": gan_wuxing,
            "ji_wuxing": ji_wuxing,
            "is_current": is_current,
            "fortune_level": fortune_level,
            "characteristics": characteristics,
            "major_events": major_events,
            "advice": self._get_daeun_advice(fortune_level, characteristics)
        }
    
    def _judge_daeun_fortune(self, gan_wuxing: str, ji_wuxing: str, day_gan_wuxing: str) -> str:
        """대운의 길흉 판단"""
        score = 0
        
        # 천간(대운 전반기 5년)의 영향
        if gan_wuxing == day_gan_wuxing:
            score += 2  # 동일 오행 - 도움
        elif self.GENERATE_CYCLE.get(gan_wuxing) == day_gan_wuxing:
            score += 3  # 상생 관계 - 매우 도움
        elif self.OVERCOME_CYCLE.get(gan_wuxing) == day_gan_wuxing:
            score -= 2  # 상극 관계 - 방해
        
        # 지지(대운 후반기 5년)의 영향
        if ji_wuxing == day_gan_wuxing:
            score += 2
        elif self.GENERATE_CYCLE.get(ji_wuxing) == day_gan_wuxing:
            score += 3
        elif self.OVERCOME_CYCLE.get(ji_wuxing) == day_gan_wuxing:
            score -= 2
        
        # 점수에 따른 길흉 판단
        if score >= 4:
            return "대길"
        elif score >= 2:
            return "소길"
        elif score >= -1:
            return "평운"
        elif score >= -3:
            return "소흉"
        else:
            return "대흉"
    
    def _analyze_daeun_characteristics(self, gan: str, ji: str, day_gan_wuxing: str) -> List[str]:
        """대운 특성 분석"""
        characteristics = []
        
        gan_wuxing = self.WUXING_MAP.get(gan, '토')
        ji_wuxing = self.WUXING_MAP.get(ji, '토')
        
        # 천간 특성 (전반기 5년)
        gan_traits = {
            '목': ['성장과 발전의 시기', '새로운 시작', '학습과 창조력 증진'],
            '화': ['활발한 활동과 성과', '인기와 명예', '열정적인 도전'],
            '토': ['안정과 기반 구축', '신뢰 관계 형성', '꾸준한 발전'],
            '금': ['정리와 완성의 시기', '원칙과 규율', '전문성 강화'],
            '수': ['깊이 있는 사고', '지혜와 통찰', '내면의 성장']
        }
        
        # 지지 특성 (후반기 5년)  
        ji_traits = {
            '목': ['실질적 성장 실현', '구체적 성과', '안정적 발전'],
            '화': ['사회적 성공', '대외 활동 활발', '리더십 발휘'],
            '토': ['기반 완성과 수확', '재물 축적', '사회적 인정'],
            '금': ['완성과 결실', '전문 분야 성취', '권위 확립'],
            '수': ['지혜로운 판단', '깊은 인맥', '정신적 성숙']
        }
        
        characteristics.extend(gan_traits.get(gan_wuxing, ['변화의 시기']))
        characteristics.extend(ji_traits.get(ji_wuxing, ['안정의 시기']))
        
        return characteristics[:4]  # 상위 4개 특성만
    
    def _predict_daeun_events(self, gan_wuxing: str, ji_wuxing: str, day_gan_wuxing: str) -> List[str]:
        """대운 시기 주요 이벤트 예측"""
        events = []
        
        # 상생/상극 관계에 따른 이벤트 예측
        if self.GENERATE_CYCLE.get(gan_wuxing) == day_gan_wuxing:
            events.append("전반기: 도움되는 인물 만남")
            events.append("전반기: 새로운 기회 발생")
        
        if self.GENERATE_CYCLE.get(ji_wuxing) == day_gan_wuxing:
            events.append("후반기: 실질적 성과 달성")
            events.append("후반기: 안정적 기반 구축")
        
        if self.OVERCOME_CYCLE.get(gan_wuxing) == day_gan_wuxing:
            events.append("전반기: 어려움 극복 필요")
        
        if self.OVERCOME_CYCLE.get(ji_wuxing) == day_gan_wuxing:
            events.append("후반기: 신중한 판단 요구")
        
        # 기본 이벤트가 없으면 일반적인 예측 추가
        if not events:
            events = ["점진적 변화", "새로운 경험", "성장 기회"]
        
        return events[:3]  # 상위 3개 이벤트만
    
    def _get_daeun_advice(self, fortune_level: str, characteristics: List[str]) -> str:
        """대운별 조언"""
        advice_map = {
            "대길": "최고의 운세 시기입니다. 적극적으로 도전하고 큰 계획을 실행하기에 좋습니다.",
            "소길": "좋은 운세의 시기입니다. 차근차근 계획을 세워 실행하면 좋은 결과를 얻을 수 있습니다.",
            "평운": "안정된 운세입니다. 기존의 것을 유지하면서 점진적 발전을 도모하세요.",
            "소흉": "다소 어려운 시기입니다. 신중하게 행동하고 기존 기반을 다지는 데 집중하세요.",
            "대흉": "주의가 필요한 시기입니다. 큰 변화보다는 현상 유지에 집중하고 인내하세요."
        }
        
        return advice_map.get(fortune_level, "균형 잡힌 시각으로 삶을 바라보세요.")
    
    # ==================== 세운 분석 메서드들 ====================
    
    def calculate_saeun(self, birth_info: BirthInfoRequest, palja: SajuPaljaResponse, target_year: int = None) -> Dict[str, Any]:
        """세운 계산 및 분석"""
        if target_year is None:
            target_year = datetime.now().year
        
        # 1. 연간 세운 계산
        yearly_saeun = self._calculate_yearly_saeun(target_year)
        
        # 2. 월별 세운 계산
        monthly_saeun = self._calculate_monthly_saeun(target_year)
        
        # 3. 개인 사주와 세운의 상호작용 분석
        saeun_interaction = self._analyze_saeun_interaction(palja, yearly_saeun, monthly_saeun)
        
        # 4. 중요 시기 분석
        critical_periods = self._get_critical_periods(saeun_interaction)
        
        # 5. 연간 운세 종합 점수
        annual_score = self._calculate_annual_fortune_score(saeun_interaction)
        
        return {
            "target_year": target_year,
            "yearly_saeun": yearly_saeun,
            "monthly_saeun": monthly_saeun,
            "annual_score": annual_score,
            "saeun_interaction": saeun_interaction,
            "critical_periods": critical_periods,
            "summary": self._generate_annual_summary(annual_score, critical_periods)
        }
    
    def _calculate_yearly_saeun(self, target_year: int) -> Dict[str, Any]:
        """연간 세운 계산 (해당 연도의 천간지지)"""
        # 갑자 60간지 순서
        ganzhi_cycle = []
        for gan in self.HEAVENLY_STEMS:
            for ji in self.EARTHLY_BRANCHES:
                ganzhi_cycle.append((gan, ji))
        
        # 기준년도 (갑자년) - 1984년을 갑자년으로 설정
        base_year = 1984
        year_offset = (target_year - base_year) % 60
        
        yearly_gan, yearly_ji = ganzhi_cycle[year_offset]
        yearly_gan_wuxing = self.WUXING_MAP.get(yearly_gan, '토')
        yearly_ji_wuxing = self.WUXING_MAP.get(yearly_ji, '토')
        
        return {
            "year": target_year,
            "gan": yearly_gan,
            "ji": yearly_ji,
            "gan_wuxing": yearly_gan_wuxing,
            "ji_wuxing": yearly_ji_wuxing,
            "ganzhi": yearly_gan + yearly_ji
        }
    
    def _calculate_monthly_saeun(self, target_year: int) -> List[Dict[str, Any]]:
        """월별 세운 계산"""
        monthly_saeun = []
        
        # 월별 지지 (자축인묘진사오미신유술해)
        monthly_ji_map = {
            1: '寅',  # 정월 (입춘)
            2: '卯',  # 2월 (경칩)
            3: '辰',  # 3월 (청명)
            4: '巳',  # 4월 (입하)
            5: '午',  # 5월 (망종)
            6: '未',  # 6월 (소서)
            7: '申',  # 7월 (입추)
            8: '酉',  # 8월 (처서)
            9: '戌',  # 9월 (한로)
            10: '亥', # 10월 (입동)
            11: '子', # 11월 (대설)
            12: '丑'  # 12월 (소한)
        }
        
        # 연간 천간을 기준으로 월간 천간 계산
        yearly_saeun = self._calculate_yearly_saeun(target_year)
        year_gan_index = self.HEAVENLY_STEMS.index(yearly_saeun['gan'])
        
        for month in range(1, 13):
            # 월간 천간 계산 (오호덕법)
            # 갑기년 - 정월부터 병인, 을경년 - 정월부터 무인...
            if yearly_saeun['gan'] in ['甲', '己']:
                month_gan_start = 2  # 丙
            elif yearly_saeun['gan'] in ['乙', '庚']:
                month_gan_start = 4  # 戊
            elif yearly_saeun['gan'] in ['丙', '辛']:
                month_gan_start = 6  # 庚
            elif yearly_saeun['gan'] in ['丁', '壬']:
                month_gan_start = 8  # 壬
            else:  # 戊, 癸
                month_gan_start = 0  # 甲
            
            month_gan_index = (month_gan_start + month - 1) % 10
            month_gan = self.HEAVENLY_STEMS[month_gan_index]
            month_ji = monthly_ji_map[month]
            
            month_gan_wuxing = self.WUXING_MAP.get(month_gan, '토')
            month_ji_wuxing = self.WUXING_MAP.get(month_ji, '토')
            
            monthly_saeun.append({
                "month": month,
                "gan": month_gan,
                "ji": month_ji,
                "gan_wuxing": month_gan_wuxing,
                "ji_wuxing": month_ji_wuxing,
                "ganzhi": month_gan + month_ji
            })
        
        return monthly_saeun
    
    def _analyze_saeun_interaction(self, palja: SajuPaljaResponse, yearly_saeun: Dict, monthly_saeun: List[Dict]) -> Dict[str, Any]:
        """개인 사주와 세운의 상호작용 분석"""
        day_gan_wuxing = self.WUXING_MAP[palja.day_gan]
        
        # 연간 상호작용 분석
        yearly_interaction = self._analyze_single_period_interaction(
            day_gan_wuxing, yearly_saeun['gan_wuxing'], yearly_saeun['ji_wuxing']
        )
        
        # 월별 상호작용 분석
        monthly_interactions = []
        for month_data in monthly_saeun:
            interaction = self._analyze_single_period_interaction(
                day_gan_wuxing, month_data['gan_wuxing'], month_data['ji_wuxing']
            )
            interaction.update({
                "month": month_data['month'],
                "ganzhi": month_data['ganzhi']
            })
            monthly_interactions.append(interaction)
        
        return {
            "yearly": yearly_interaction,
            "monthly": monthly_interactions
        }
    
    def _analyze_single_period_interaction(self, day_gan_wuxing: str, period_gan_wuxing: str, period_ji_wuxing: str) -> Dict[str, Any]:
        """단일 기간(연/월)의 상호작용 분석"""
        score = 0
        characteristics = []
        warnings = []
        opportunities = []
        
        # 천간 상호작용 (정신적/심리적 영향)
        if period_gan_wuxing == day_gan_wuxing:
            score += 2
            characteristics.append("자아 강화")
            opportunities.append("자신감 있는 도전")
        elif self.GENERATE_CYCLE.get(period_gan_wuxing) == day_gan_wuxing:
            score += 3
            characteristics.append("도움되는 기운")
            opportunities.append("협력자 출현")
        elif self.OVERCOME_CYCLE.get(period_gan_wuxing) == day_gan_wuxing:
            score -= 2
            characteristics.append("압박과 시련")
            warnings.append("신중한 결정 필요")
        
        # 지지 상호작용 (현실적/물질적 영향)
        if period_ji_wuxing == day_gan_wuxing:
            score += 2
            characteristics.append("안정적 기반")
            opportunities.append("실질적 성과")
        elif self.GENERATE_CYCLE.get(period_ji_wuxing) == day_gan_wuxing:
            score += 3
            characteristics.append("성장 동력")
            opportunities.append("새로운 기회")
        elif self.OVERCOME_CYCLE.get(period_ji_wuxing) == day_gan_wuxing:
            score -= 2
            characteristics.append("장애물 존재")
            warnings.append("계획 재검토")
        
        # 길흉 판단
        if score >= 4:
            fortune_level = "대길"
        elif score >= 2:
            fortune_level = "소길"
        elif score >= -1:
            fortune_level = "평운"
        elif score >= -3:
            fortune_level = "소흉"
        else:
            fortune_level = "대흉"
        
        return {
            "score": score,
            "fortune_level": fortune_level,
            "characteristics": characteristics[:3],  # 최대 3개
            "opportunities": opportunities[:2],      # 최대 2개
            "warnings": warnings[:2],               # 최대 2개
        }
    
    def _get_critical_periods(self, saeun_interaction: Dict) -> Dict[str, Any]:
        """중요 시기 (주의/기회) 분석"""
        monthly_data = saeun_interaction['monthly']
        
        # 최고 운세 월
        best_months = []
        # 주의 필요 월
        caution_months = []
        # 기회의 월
        opportunity_months = []
        
        for month_data in monthly_data:
            month = month_data['month']
            score = month_data['score']
            fortune_level = month_data['fortune_level']
            
            if fortune_level in ['대길', '소길'] and score >= 3:
                best_months.append({
                    "month": month,
                    "score": score,
                    "level": fortune_level
                })
            
            if fortune_level in ['대흉', '소흉']:
                caution_months.append({
                    "month": month,
                    "score": score,
                    "level": fortune_level
                })
            
            if month_data['opportunities']:
                opportunity_months.append({
                    "month": month,
                    "opportunities": month_data['opportunities']
                })
        
        return {
            "best_months": sorted(best_months, key=lambda x: x['score'], reverse=True)[:3],
            "caution_months": sorted(caution_months, key=lambda x: x['score'])[:3],
            "opportunity_months": opportunity_months[:4]
        }
    
    def _calculate_annual_fortune_score(self, saeun_interaction: Dict) -> Dict[str, Any]:
        """연간 운세 종합 점수 계산"""
        yearly_score = saeun_interaction['yearly']['score']
        monthly_scores = [month['score'] for month in saeun_interaction['monthly']]
        
        # 가중 평균 (연간 70%, 월간 평균 30%)
        monthly_avg = sum(monthly_scores) / len(monthly_scores)
        total_score = (yearly_score * 0.7) + (monthly_avg * 0.3)
        
        # 정규화 (0-100점)
        normalized_score = max(0, min(100, (total_score + 5) * 10))  # -5~5 점수를 0~100으로 변환
        
        # 등급 판정
        if normalized_score >= 80:
            grade = "최상"
        elif normalized_score >= 65:
            grade = "상"
        elif normalized_score >= 50:
            grade = "중"
        elif normalized_score >= 35:
            grade = "하"
        else:
            grade = "최하"
        
        return {
            "total_score": round(total_score, 1),
            "normalized_score": round(normalized_score, 1),
            "grade": grade,
            "yearly_contribution": yearly_score,
            "monthly_average": round(monthly_avg, 1)
        }
    
    def _generate_annual_summary(self, annual_score: Dict, critical_periods: Dict) -> str:
        """연간 운세 종합 요약"""
        grade = annual_score['grade']
        score = annual_score['normalized_score']
        
        base_summary = {
            "최상": f"올해는 매우 좋은 운세의 해입니다 ({score}점). 적극적인 도전과 새로운 시작에 최적의 시기입니다.",
            "상": f"올해는 좋은 운세의 해입니다 ({score}점). 계획했던 일들을 차근차근 실행하기에 좋습니다.",
            "중": f"올해는 안정적인 운세의 해입니다 ({score}점). 기존 기반을 다지며 점진적 발전을 도모하세요.",
            "하": f"올해는 신중함이 필요한 해입니다 ({score}점). 급한 변화보다는 현상 유지에 집중하세요.",
            "최하": f"올해는 인내가 필요한 해입니다 ({score}점). 어려움을 극복하며 내실을 다지는 시기로 보세요."
        }
        
        summary = base_summary.get(grade, "균형 잡힌 한 해가 될 것입니다.")
        
        # 주의 월이 있으면 추가
        if critical_periods['caution_months']:
            caution_months_str = ', '.join([f"{m['month']}월" for m in critical_periods['caution_months']])
            summary += f" 특히 {caution_months_str}에는 신중한 판단이 필요합니다."
        
        # 좋은 월이 있으면 추가
        if critical_periods['best_months']:
            best_months_str = ', '.join([f"{m['month']}월" for m in critical_periods['best_months']])
            summary += f" {best_months_str}은 특히 좋은 시기가 될 것입니다."
        
        return summary

# 싱글톤 인스턴스
saju_analyzer = SajuAnalyzer()