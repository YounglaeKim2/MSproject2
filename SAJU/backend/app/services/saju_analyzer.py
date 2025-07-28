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
            else:
                use_god = day_gan_wuxing
            avoid_god = self.OVERCOME_CYCLE[day_gan_wuxing]  # 극하는 오행
        
        return WuXingAnalysis(
            wood=wuxing_count['목'],
            fire=wuxing_count['화'],
            earth=wuxing_count['토'],
            metal=wuxing_count['금'],
            water=wuxing_count['수'],
            strength=strength,
            use_god=use_god,
            avoid_god=avoid_god
        )
    
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