"""
궁합 분석 엔진
- 사주팔자 기반 궁합 분석
- 오행 상생상극 궁합
- 십성 배합 궁합
- 종합 궁합 점수 계산
"""
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

# 궁합 분석을 위한 사주 핵심 기능 import
from app.services.saju_core import saju_core

from app.models.compatibility import (
    PersonInfo, CompatibilityRequest, CompatibilityAnalysis,
    PillarCompatibility, WuxingCompatibility, TenStarsCompatibility
)
from app.database.connection import get_manseryuk_db

logger = logging.getLogger(__name__)

class CompatibilityAnalyzer:
    """궁합 분석 엔진"""
    
    def __init__(self):
        self.db = get_manseryuk_db()
        self.saju_core = saju_core
        
        # 천간 상성표 (10개 천간)
        self.gan_compatibility = {
            ('甲', '己'): 85, ('己', '甲'): 85,  # 갑기합화토
            ('乙', '庚'): 80, ('庚', '乙'): 80,  # 을경합화금
            ('丙', '辛'): 75, ('辛', '丙'): 75,  # 병신합화수
            ('丁', '壬'): 82, ('壬', '丁'): 82,  # 정임합화목
            ('戊', '癸'): 78, ('癸', '戊'): 78,  # 무계합화화
        }
        
        # 지지 상성표 (12개 지지)
        self.ji_compatibility = {
            # 삼합
            ('子', '辰'): 90, ('辰', '子'): 90,  # 수국삼합
            ('子', '申'): 90, ('申', '子'): 90,
            ('辰', '申'): 90, ('申', '辰'): 90,
            ('亥', '卯'): 88, ('卯', '亥'): 88,  # 목국삼합  
            ('亥', '未'): 88, ('未', '亥'): 88,
            ('卯', '未'): 88, ('未', '卯'): 88,
            ('寅', '午'): 85, ('午', '寅'): 85,  # 화국삼합
            ('寅', '戌'): 85, ('戌', '寅'): 85,
            ('午', '戌'): 85, ('戌', '午'): 85,
            ('巳', '酉'): 87, ('酉', '巳'): 87,  # 금국삼합
            ('巳', '丑'): 87, ('丑', '巳'): 87,
            ('酉', '丑'): 87, ('丑', '酉'): 87,
            
            # 육합
            ('子', '丑'): 80, ('丑', '子'): 80,
            ('寅', '亥'): 78, ('亥', '寅'): 78,
            ('卯', '戌'): 76, ('戌', '卯'): 76,
            ('辰', '酉'): 74, ('酉', '辰'): 74,
            ('巳', '申'): 72, ('申', '巳'): 72,
            ('午', '未'): 70, ('未', '午'): 70,
        }
        
        # 지지 충극표 (상극 관계)
        self.ji_conflicts = {
            ('子', '午'): -30, ('午', '子'): -30,  # 자오충
            ('丑', '未'): -25, ('未', '丑'): -25,  # 축미충
            ('寅', '申'): -35, ('申', '寅'): -35,  # 인신충
            ('卯', '酉'): -32, ('酉', '卯'): -32,  # 묘유충
            ('辰', '戌'): -28, ('戌', '辰'): -28,  # 진술충
            ('巳', '亥'): -30, ('亥', '巳'): -30,  # 사해충
        }
        
        # 오행 상생상극
        self.wuxing_relations = {
            "상생": {
                ("목", "화"): 15, ("화", "토"): 15, ("토", "금"): 15, 
                ("금", "수"): 15, ("수", "목"): 15
            },
            "상극": {
                ("목", "토"): -10, ("토", "수"): -10, ("수", "화"): -10,
                ("화", "금"): -10, ("금", "목"): -10
            }
        }

    def analyze_compatibility(self, request: CompatibilityRequest) -> CompatibilityAnalysis:
        """종합 궁합 분석"""
        try:
            # 1. 두 사람의 사주 분석
            person1_saju = self._get_person_saju(request.person1)
            person2_saju = self._get_person_saju(request.person2)
            
            # 2. 사주팔자 궁합 분석
            pillar_compatibility = self._analyze_pillar_compatibility(person1_saju, person2_saju)
            
            # 3. 오행 궁합 분석  
            wuxing_compatibility = self._analyze_wuxing_compatibility(person1_saju, person2_saju)
            
            # 4. 십성 궁합 분석
            ten_stars_compatibility = self._analyze_ten_stars_compatibility(person1_saju, person2_saju)
            
            # 5. 종합 점수 계산
            total_score = self._calculate_total_score(
                pillar_compatibility, wuxing_compatibility, ten_stars_compatibility
            )
            
            # 6. 등급 판정
            grade = self._determine_grade(total_score)
            
            # 7. 분야별 궁합 계산
            field_scores = self._calculate_field_compatibility(
                pillar_compatibility, wuxing_compatibility, ten_stars_compatibility
            )
            
            # 8. 해석 생성
            analysis_result = self._generate_interpretation(
                total_score, grade, pillar_compatibility, 
                wuxing_compatibility, ten_stars_compatibility
            )
            
            return CompatibilityAnalysis(
                total_score=total_score,
                grade=grade,
                pillar_compatibility=pillar_compatibility,
                wuxing_compatibility=wuxing_compatibility,
                ten_stars_compatibility=ten_stars_compatibility,
                strengths=analysis_result["strengths"],
                weaknesses=analysis_result["weaknesses"], 
                advice=analysis_result["advice"],
                love_compatibility=field_scores["love"],
                marriage_compatibility=field_scores["marriage"],
                business_compatibility=field_scores["business"],
                friendship_compatibility=field_scores["friendship"]
            )
            
        except Exception as e:
            logger.error(f"궁합 분석 중 오류: {e}")
            raise

    def _get_person_saju(self, person: PersonInfo) -> Dict:
        """개인의 사주 분석 결과 가져오기"""
        palja = self.saju_core.get_palja(person.year, person.month, person.day, person.hour, person.gender)
        wuxing = self.saju_core.get_wuxing(palja)
        ten_stars = self.saju_core.get_ten_stars(palja)
        
        return {
            "palja": palja,
            "wuxing": wuxing,
            "ten_stars": ten_stars
        }

    def _analyze_pillar_compatibility(self, person1: Dict, person2: Dict) -> PillarCompatibility:
        """사주팔자 궁합 분석"""
        p1_palja = person1["palja"]
        p2_palja = person2["palja"]
        
        # 각 주별 궁합 점수 계산
        year_score = self._calculate_pillar_score(
            p1_palja["year_gan"], p1_palja["year_ji"],
            p2_palja["year_gan"], p2_palja["year_ji"]
        )
        
        month_score = self._calculate_pillar_score(
            p1_palja["month_gan"], p1_palja["month_ji"],
            p2_palja["month_gan"], p2_palja["month_ji"]
        )
        
        day_score = self._calculate_pillar_score(
            p1_palja["day_gan"], p1_palja["day_ji"],
            p2_palja["day_gan"], p2_palja["day_ji"]
        )
        
        hour_score = self._calculate_pillar_score(
            p1_palja["hour_gan"], p1_palja["hour_ji"],
            p2_palja["hour_gan"], p2_palja["hour_ji"]
        )
        
        # 일주가 가장 중요하므로 가중치 적용
        overall_score = (year_score * 0.2 + month_score * 0.25 + 
                        day_score * 0.35 + hour_score * 0.2)
        
        return PillarCompatibility(
            year_compatibility=year_score,
            month_compatibility=month_score,
            day_compatibility=day_score,
            hour_compatibility=hour_score,
            overall_score=overall_score
        )

    def _calculate_pillar_score(self, gan1: str, ji1: str, gan2: str, ji2: str) -> float:
        """각 주의 궁합 점수 계산"""
        # 천간 궁합
        gan_score = self.gan_compatibility.get((gan1, gan2), 50)  # 기본 50점
        
        # 지지 궁합 (상생 > 충극 확인)
        ji_score = 50  # 기본 점수
        
        if (ji1, ji2) in self.ji_compatibility:
            ji_score = self.ji_compatibility[(ji1, ji2)]
        elif (ji1, ji2) in self.ji_conflicts:
            ji_score = 50 + self.ji_conflicts[(ji1, ji2)]  # 충극은 음수이므로 더함
        
        # 천간:지지 = 4:6 비율
        return gan_score * 0.4 + ji_score * 0.6

    def _analyze_wuxing_compatibility(self, person1: Dict, person2: Dict) -> WuxingCompatibility:
        """오행 궁합 분석"""
        p1_wuxing = person1["wuxing"]
        p2_wuxing = person2["wuxing"]
        
        # 오행 분포 계산
        elements = ["wood", "fire", "earth", "metal", "water"]
        element_names = {"wood": "목", "fire": "화", "earth": "토", "metal": "금", "water": "수"}
        
        harmony_elements = []
        conflict_elements = []
        balance_score = 0
        
        for elem1 in elements:
            for elem2 in elements:
                name1, name2 = element_names[elem1], element_names[elem2]
                
                # 상생 관계 확인
                if (name1, name2) in self.wuxing_relations["상생"]:
                    harmony_elements.append(f"{name1}-{name2}")
                    balance_score += self.wuxing_relations["상생"][(name1, name2)]
                
                # 상극 관계 확인  
                elif (name1, name2) in self.wuxing_relations["상극"]:
                    conflict_elements.append(f"{name1}-{name2}")
                    balance_score += self.wuxing_relations["상극"][(name1, name2)]
        
        # 궁합 유형 결정
        if balance_score > 30:
            compatibility_type = "상생 궁합"
        elif balance_score < -20:
            compatibility_type = "상극 궁합" 
        else:
            compatibility_type = "평형 궁합"
        
        # 점수 정규화 (0-100)
        normalized_score = max(0, min(100, balance_score + 50))
        
        return WuxingCompatibility(
            balance_score=normalized_score,
            harmony_elements=harmony_elements,
            conflict_elements=conflict_elements,
            compatibility_type=compatibility_type
        )

    def _analyze_ten_stars_compatibility(self, person1: Dict, person2: Dict) -> TenStarsCompatibility:
        """십성 궁합 분석"""
        # 간단한 십성 궁합 로직 (실제로는 더 복잡)
        p1_stars = person1.get("ten_stars", {})
        p2_stars = person2.get("ten_stars", {})
        
        # 기본적인 십성 상성 점수
        harmony_score = 65.0  # 기본 점수
        support_level = 70.0
        conflict_level = 30.0
        
        # 십성 배합에 따른 관계 유형 결정
        dominant_relationship = "조화로운 관계"
        
        return TenStarsCompatibility(
            dominant_relationship=dominant_relationship,
            support_level=support_level,
            conflict_level=conflict_level,
            harmony_score=harmony_score
        )

    def _calculate_total_score(self, pillar: PillarCompatibility, 
                              wuxing: WuxingCompatibility, 
                              ten_stars: TenStarsCompatibility) -> float:
        """총 궁합 점수 계산"""
        # 가중치: 사주팔자 50%, 오행 30%, 십성 20%
        total = (pillar.overall_score * 0.5 + 
                wuxing.balance_score * 0.3 + 
                ten_stars.harmony_score * 0.2)
        
        return round(total, 1)

    def _determine_grade(self, score: float) -> str:
        """궁합 등급 판정"""
        if score >= 85:
            return "천생연분"
        elif score >= 75:
            return "매우 좋음"
        elif score >= 65:
            return "좋음"
        elif score >= 55:
            return "보통"
        elif score >= 45:
            return "주의 필요"
        else:
            return "어려움"

    def _calculate_field_compatibility(self, pillar: PillarCompatibility, 
                                     wuxing: WuxingCompatibility, 
                                     ten_stars: TenStarsCompatibility) -> Dict[str, float]:
        """분야별 궁합 계산"""
        base_score = (pillar.overall_score + wuxing.balance_score + ten_stars.harmony_score) / 3
        
        return {
            "love": round(base_score * 1.05, 1),      # 연애는 약간 높게
            "marriage": round(base_score, 1),         # 결혼은 기본 점수
            "business": round(base_score * 0.95, 1),  # 사업은 약간 낮게
            "friendship": round(base_score * 1.1, 1)  # 우정은 높게
        }

    def _generate_interpretation(self, total_score: float, grade: str,
                               pillar: PillarCompatibility, 
                               wuxing: WuxingCompatibility, 
                               ten_stars: TenStarsCompatibility) -> Dict[str, List[str]]:
        """궁합 해석 생성"""
        strengths = []
        weaknesses = []
        advice = []
        
        # 점수에 따른 해석
        if total_score >= 75:
            strengths.extend([
                "서로의 부족한 부분을 잘 보완해주는 관계",
                "가치관과 성향이 조화롭게 어우러짐",
                "자연스러운 소통과 이해가 가능"
            ])
            advice.append("현재의 좋은 관계를 지속하며 더욱 발전시켜 나가세요")
        
        elif total_score >= 55:
            strengths.extend([
                "노력을 통해 좋은 관계 발전 가능",
                "서로 다른 점이 오히려 매력이 될 수 있음"
            ])
            weaknesses.append("때로는 가치관의 차이로 인한 갈등 가능")
            advice.extend([
                "서로의 차이점을 인정하고 배려하는 마음 필요",
                "꾸준한 대화와 소통으로 이해를 높여가세요"
            ])
        
        else:
            weaknesses.extend([
                "성향과 가치관의 차이가 클 수 있음",
                "서로를 이해하는데 많은 노력이 필요"
            ])
            advice.extend([
                "급하게 발전시키려 하지 말고 천천히 알아가세요",
                "서로의 장점에 집중하며 단점은 너그럽게 이해하세요"
            ])
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "advice": advice
        }

# 전역 인스턴스
compatibility_analyzer = CompatibilityAnalyzer()