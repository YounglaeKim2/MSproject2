from typing import Dict, Any, List, Tuple
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
        
        return {
            "palja": palja,
            "wuxing": wuxing,
            "ten_stars": ten_stars,
            "personality": personality,
            "career": career,
            "health": health,
            "relationship": relationship,
            "fortune": fortune
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

# 싱글톤 인스턴스
saju_analyzer = SajuAnalyzer()