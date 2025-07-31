"""
간단하고 안정적인 궁합 분석 로직
"""
import random
from typing import Dict, Any
from app.models.compatibility import (
    PersonInfo, CompatibilityRequest, CompatibilityAnalysis,
    PillarCompatibility, WuxingCompatibility, TenStarsCompatibility
)
from app.database.connection import get_manseryuk_db
from app.services.saju_core import saju_core

class SimpleCompatibilityAnalyzer:
    """간단하고 다양한 점수를 생성하는 궁합 분석기"""
    
    def __init__(self):
        self.db = get_manseryuk_db()
        self.saju_core = saju_core
    
    def analyze_compatibility(self, request: CompatibilityRequest) -> CompatibilityAnalysis:
        """종합 궁합 분석"""
        try:
            # 1. 두 사람의 사주 분석
            person1_saju = self._get_person_saju(request.person1)
            person2_saju = self._get_person_saju(request.person2)
            
            # 2. 스펙타클한 점수 생성
            pillar_score = self._calculate_dramatic_pillar_score(person1_saju, person2_saju)
            wuxing_score = self._calculate_dramatic_wuxing_score(person1_saju, person2_saju)
            ten_stars_score = self._calculate_dramatic_ten_stars_score(person1_saju, person2_saju)
            
            # 3. 종합 점수 계산 (가중치 적용)
            total_score = round(
                pillar_score * 0.5 + wuxing_score * 0.3 + ten_stars_score * 0.2, 1
            )
            
            # 4. 등급 판정
            grade = self._determine_grade(total_score)
            
            # 5. 분야별 궁합 점수
            field_scores = self._calculate_field_scores(total_score)
            
            # 6. 해석 생성
            interpretation = self._generate_interpretation(total_score, grade)
            
            return CompatibilityAnalysis(
                total_score=total_score,
                grade=grade,
                pillar_compatibility=PillarCompatibility(
                    year_compatibility=round(random.uniform(15, 95), 1),
                    month_compatibility=round(random.uniform(20, 90), 1),
                    day_compatibility=round(random.uniform(10, 98), 1),
                    hour_compatibility=round(random.uniform(25, 85), 1),
                    overall_score=pillar_score
                ),
                wuxing_compatibility=WuxingCompatibility(
                    balance_score=wuxing_score,
                    harmony_elements=["목-화", "화-토", "토-금"] if wuxing_score > 60 else ["금-수"],
                    conflict_elements=["목-토", "수-화"] if wuxing_score < 40 else [],
                    compatibility_type="상생 궁합" if wuxing_score > 70 else "상극 궁합" if wuxing_score < 30 else "평형 궁합"
                ),
                ten_stars_compatibility=TenStarsCompatibility(
                    dominant_relationship=self._get_relationship_type(ten_stars_score),
                    support_level=round(random.uniform(20, 95), 1),
                    conflict_level=round(random.uniform(5, 60), 1),
                    harmony_score=ten_stars_score
                ),
                strengths=interpretation["strengths"],
                weaknesses=interpretation["weaknesses"],
                advice=interpretation["advice"],
                love_compatibility=field_scores["love"],
                marriage_compatibility=field_scores["marriage"],
                business_compatibility=field_scores["business"],
                friendship_compatibility=field_scores["friendship"]
            )
            
        except Exception as e:
            import logging
            logging.error(f"궁합 분석 중 오류: {e}")
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
    
    def _calculate_dramatic_pillar_score(self, person1: Dict, person2: Dict) -> float:
        """사주팔자 궁합 - 극적인 점수 범위"""
        # 80+ 점수가 나올 가능성을 크게 증가
        base_scores = [
            random.uniform(30, 98),   # 년주 (범위 상향)
            random.uniform(40, 95),   # 월주 (범위 상향)
            random.uniform(50, 99),   # 일주 (가장 중요, 높은 범위)
            random.uniform(45, 92)    # 시주 (범위 상향)
        ]
        
        # 높은 점수 보너스 확률 대폭 증가
        bonus = random.choice([10, 15, 20, 25, 30, 35])  # 항상 보너스
        
        # 일주 중요도 반영 가중평균
        weighted_score = (base_scores[0] * 0.2 + base_scores[1] * 0.25 + 
                         base_scores[2] * 0.35 + base_scores[3] * 0.2) + bonus
        
        return round(max(50, min(98, weighted_score)), 1)
    
    def _calculate_dramatic_wuxing_score(self, person1: Dict, person2: Dict) -> float:
        """오행 궁합 - 극적인 점수 범위"""
        base_score = random.uniform(20, 90)
        # 높은 점수 보너스 가능성
        bonus = random.choice([0, 0, 5, 10])
        return round(min(94, base_score + bonus), 1)
    
    def _calculate_dramatic_ten_stars_score(self, person1: Dict, person2: Dict) -> float:
        """십성 궁합 - 극적인 점수 범위"""
        base_score = random.uniform(25, 88)
        # 높은 점수 보너스 가능성
        bonus = random.choice([0, 0, 8, 15])
        return round(min(92, base_score + bonus), 1)
    
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
        elif score >= 30:
            return "어려움"
        else:
            return "매우 어려움"
    
    def _calculate_field_scores(self, total_score: float) -> Dict[str, float]:
        """분야별 궁합 점수"""
        base = total_score
        return {
            "love": round(base + random.uniform(-15, 20), 1),
            "marriage": round(base + random.uniform(-12, 18), 1),
            "business": round(base + random.uniform(-20, 15), 1),
            "friendship": round(base + random.uniform(-8, 25), 1)
        }
    
    def _get_relationship_type(self, score: float) -> str:
        """관계 유형 결정"""
        if score >= 80:
            return "완벽한 상호보완"
        elif score >= 65:
            return "조화로운 관계"
        elif score >= 50:
            return "노력이 필요한 관계"
        elif score >= 35:
            return "도전적인 관계"
        else:
            return "매우 어려운 관계"
    
    def _generate_interpretation(self, total_score: float, grade: str) -> Dict:
        """해석 생성"""
        strengths = []
        weaknesses = []
        advice = []
        
        if total_score >= 80:
            strengths.extend([
                "서로의 부족한 부분을 완벽하게 보완",
                "자연스러운 호흡과 깊은 이해",
                "함께할 때 더욱 빛나는 관계"
            ])
            advice.append("현재의 완벽한 조화를 더욱 발전시켜 나가세요")
        elif total_score >= 65:
            strengths.extend([
                "서로의 장점을 잘 살려주는 관계",
                "가치관과 성향이 조화롭게 어우러짐",
                "자연스러운 소통과 이해가 가능"
            ])
            advice.append("현재의 좋은 관계를 지속하며 더욱 발전시켜 나가세요")
        elif total_score >= 50:
            strengths.extend([
                "노력을 통해 좋은 관계 발전 가능",
                "서로 다른 점이 오히려 매력이 될 수 있음"
            ])
            weaknesses.append("때로는 가치관의 차이로 인한 갈등 가능")
            advice.extend([
                "서로의 차이점을 인정하고 배려하는 마음 필요",
                "꾸준한 대화와 소통으로 이해를 높여가세요"
            ])
        elif total_score >= 35:
            strengths.append("인내와 노력으로 관계 개선 가능")
            weaknesses.extend([
                "성향과 가치관의 차이가 클 수 있음",
                "서로를 이해하는데 많은 시간과 노력 필요"
            ])
            advice.extend([
                "급하게 발전시키려 하지 말고 천천히 알아가세요",
                "서로의 장점에 집중하며 단점은 너그럽게 이해하세요"
            ])
        else:
            strengths.append("어려움을 통해 더 강한 유대감 형성 가능")
            weaknesses.extend([
                "근본적인 성향 차이로 인한 지속적 갈등",
                "서로의 입장을 이해하기 매우 어려움"
            ])
            advice.extend([
                "관계보다는 개인의 성장에 더 집중하는 것이 좋겠습니다",
                "무리한 관계 유지보다는 적절한 거리를 두세요"
            ])
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "advice": advice
        }

# 전역 인스턴스
simple_compatibility_analyzer = SimpleCompatibilityAnalyzer()