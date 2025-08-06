"""
궁합 계산 엔진
- SAJU API 결과를 바탕으로 궁합 분석
- 오행 상생상극 계산
- 십성 배합 분석
- 종합 점수 산출
"""
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class CompatibilityEngine:
    """궁합 계산 엔진"""
    
    def __init__(self):
        # 오행 상생상극 매트릭스 (점수 기반)
        self.wuxing_compatibility = {
            ("목", "목"): 70,  # 같은 오행
            ("목", "화"): 85,  # 목생화 (상생)
            ("목", "토"): 30,  # 목극토 (상극)
            ("목", "금"): 25,  # 금극목 (상극)
            ("목", "수"): 80,  # 수생목 (상생)
            
            ("화", "목"): 80,  # 목생화 (상생)
            ("화", "화"): 70,  # 같은 오행
            ("화", "토"): 85,  # 화생토 (상생)
            ("화", "금"): 30,  # 화극금 (상극)
            ("화", "수"): 25,  # 수극화 (상극)
            
            ("토", "목"): 25,  # 목극토 (상극)
            ("토", "화"): 80,  # 화생토 (상생)
            ("토", "토"): 70,  # 같은 오행
            ("토", "금"): 85,  # 토생금 (상생)
            ("토", "수"): 30,  # 토극수 (상극)
            
            ("금", "목"): 30,  # 금극목 (상극)
            ("금", "화"): 25,  # 화극금 (상극)
            ("금", "토"): 80,  # 토생금 (상생)
            ("금", "금"): 70,  # 같은 오행
            ("금", "수"): 85,  # 금생수 (상생)
            
            ("수", "목"): 85,  # 수생목 (상생)
            ("수", "화"): 30,  # 수극화 (상극)
            ("수", "토"): 25,  # 토극수 (상극)
            ("수", "금"): 80,  # 금생수 (상생)
            ("수", "수"): 70,  # 같은 오행
        }
        
        # 십성 궁합 점수
        self.sibseong_compatibility = {
            # 정관계열 (안정적)
            ("정관", "정인"): 90,
            ("정관", "편인"): 75,
            ("정관", "비견"): 60,
            ("정관", "겁재"): 45,
            ("정관", "식신"): 80,
            ("정관", "상관"): 30,
            ("정관", "정재"): 85,
            ("정관", "편재"): 70,
            ("정관", "편관"): 50,
            ("정관", "정관"): 65,
            
            # 편관계열 (역동적)
            ("편관", "정인"): 75,
            ("편관", "편인"): 85,
            ("편관", "비견"): 70,
            ("편관", "겁재"): 80,
            ("편관", "식신"): 40,
            ("편관", "상관"): 75,
            ("편관", "정재"): 60,
            ("편관", "편재"): 85,
            ("편관", "편관"): 70,
            ("편관", "정관"): 50,
            
            # 정재계열 (현실적)
            ("정재", "정인"): 35,
            ("정재", "편인"): 25,
            ("정재", "비견"): 85,
            ("정재", "겁재"): 30,
            ("정재", "식신"): 90,
            ("정재", "상관"): 75,
            ("정재", "정재"): 80,
            ("정재", "편재"): 70,
            ("정재", "편관"): 60,
            ("정재", "정관"): 85,
            
            # 편재계열 (적극적)
            ("편재", "정인"): 25,
            ("편재", "편인"): 35,
            ("편재", "비견"): 70,
            ("편재", "겁재"): 85,
            ("편재", "식신"): 75,
            ("편재", "상관"): 90,
            ("편재", "정재"): 70,
            ("편재", "편재"): 80,
            ("편재", "편관"): 85,
            ("편재", "정관"): 70,
        }
        
    def extract_saju_elements(self, saju_data: Dict[str, Any]) -> Dict[str, Any]:
        """SAJU API 응답에서 필요한 요소들 추출"""
        try:
            elements = {}
            
            # 기본 정보 추출
            if "basic_info" in saju_data:
                elements["name"] = saju_data["basic_info"].get("name", "Unknown")
                elements["gender"] = saju_data["basic_info"].get("gender", "unknown")
            
            # 사주팔자 추출
            if "sajupalja" in saju_data:
                elements["sajupalja"] = saju_data["sajupalja"]
                
                # 일간 추출 (가장 중요)
                if "day" in saju_data["sajupalja"]:
                    elements["ilgan"] = saju_data["sajupalja"]["day"].get("천간", "")
                    elements["ilji"] = saju_data["sajupalja"]["day"].get("지지", "")
            
            # 오행 분석 추출
            if "wuxing_analysis" in saju_data:
                elements["wuxing"] = saju_data["wuxing_analysis"]
                elements["wuxing_score"] = saju_data["wuxing_analysis"].get("오행점수", {})
            
            # 십성 분석 추출
            if "sibseong_analysis" in saju_data:
                elements["sibseong"] = saju_data["sibseong_analysis"]
                # 주도적인 십성 찾기
                sibseong_scores = saju_data["sibseong_analysis"].get("십성점수", {})
                if sibseong_scores:
                    elements["main_sibseong"] = max(sibseong_scores.items(), key=lambda x: x[1])[0]
            
            # 성격 분석 추출
            if "personality_analysis" in saju_data:
                elements["personality"] = saju_data["personality_analysis"]
            
            return elements
            
        except Exception as e:
            logger.error(f"사주 요소 추출 실패: {e}")
            return {}
    
    def calculate_wuxing_compatibility(self, person1_wuxing: Dict[str, int], person2_wuxing: Dict[str, int]) -> Dict[str, Any]:
        """오행 궁합 계산"""
        try:
            # 각 사람의 주도적인 오행 찾기
            person1_main = max(person1_wuxing.items(), key=lambda x: x[1])[0] if person1_wuxing else "목"
            person2_main = max(person2_wuxing.items(), key=lambda x: x[1])[0] if person2_wuxing else "목"
            
            # 주오행 궁합 점수
            main_score = self.wuxing_compatibility.get((person1_main, person2_main), 50)
            
            # 전체 오행 밸런스 점수 계산
            balance_scores = []
            wuxing_elements = ["목", "화", "토", "금", "수"]
            
            for element in wuxing_elements:
                p1_score = person1_wuxing.get(element, 0)
                p2_score = person2_wuxing.get(element, 0)
                
                # 상호 보완성 계산 (한쪽이 부족하면 다른 쪽이 보완)
                complement_score = 100 - abs(p1_score - p2_score)
                balance_scores.append(complement_score)
            
            balance_score = sum(balance_scores) / len(balance_scores)
            
            # 최종 오행 궁합 점수 (주오행 70%, 밸런스 30%)
            final_score = int(main_score * 0.7 + balance_score * 0.3)
            
            return {
                "score": final_score,
                "person1_main": person1_main,
                "person2_main": person2_main,
                "main_compatibility": main_score,
                "balance_score": int(balance_score),
                "analysis": self.get_wuxing_analysis(person1_main, person2_main, final_score)
            }
            
        except Exception as e:
            logger.error(f"오행 궁합 계산 실패: {e}")
            return {"score": 50, "analysis": "오행 분석 중 오류가 발생했습니다."}
    
    def calculate_sibseong_compatibility(self, person1_sibseong: str, person2_sibseong: str) -> Dict[str, Any]:
        """십성 궁합 계산"""
        try:
            # 십성 궁합 점수 조회
            score = self.sibseong_compatibility.get((person1_sibseong, person2_sibseong), 50)
            
            # 역방향도 확인 (대칭적이지 않은 경우)
            reverse_score = self.sibseong_compatibility.get((person2_sibseong, person1_sibseong), 50)
            
            # 평균 점수 사용
            final_score = int((score + reverse_score) / 2)
            
            return {
                "score": final_score,
                "person1_sibseong": person1_sibseong,
                "person2_sibseong": person2_sibseong,
                "analysis": self.get_sibseong_analysis(person1_sibseong, person2_sibseong, final_score)
            }
            
        except Exception as e:
            logger.error(f"십성 궁합 계산 실패: {e}")
            return {"score": 50, "analysis": "십성 분석 중 오류가 발생했습니다."}
    
    def get_wuxing_analysis(self, element1: str, element2: str, score: int) -> str:
        """오행 궁합 분석 텍스트 생성"""
        if score >= 80:
            return f"{element1}과 {element2}의 조합은 매우 조화로운 관계입니다. 서로를 발전시키는 상생의 기운이 강합니다."
        elif score >= 60:
            return f"{element1}과 {element2}는 안정적인 관계를 유지할 수 있습니다. 큰 충돌 없이 조화로운 생활이 가능합니다."
        elif score >= 40:
            return f"{element1}과 {element2}의 관계에서는 서로 이해하려는 노력이 필요합니다. 차이점을 인정하고 배려한다면 좋은 관계가 됩니다."
        else:
            return f"{element1}과 {element2}는 상극 관계로 갈등이 생길 수 있습니다. 하지만 서로의 다름을 이해하고 소통한다면 극복 가능합니다."
    
    def get_sibseong_analysis(self, sibseong1: str, sibseong2: str, score: int) -> str:
        """십성 궁합 분석 텍스트 생성"""
        if score >= 80:
            return f"{sibseong1}과 {sibseong2}의 조합은 서로를 완벽하게 보완하는 이상적인 관계입니다."
        elif score >= 60:
            return f"{sibseong1}과 {sibseong2}는 서로를 이해하고 지지하는 좋은 관계를 만들 수 있습니다."
        elif score >= 40:
            return f"{sibseong1}과 {sibseong2}의 관계에서는 서로의 차이를 인정하고 조율하는 것이 중요합니다."
        else:
            return f"{sibseong1}과 {sibseong2}는 성격적 차이가 클 수 있어 많은 이해와 노력이 필요합니다."
    
    def calculate_overall_compatibility(self, person1_data: Dict[str, Any], person2_data: Dict[str, Any]) -> Dict[str, Any]:
        """전체 궁합 계산"""
        try:
            logger.info("전체 궁합 계산 시작")
            
            # 각 사람의 사주 요소 추출
            person1_elements = self.extract_saju_elements(person1_data)
            person2_elements = self.extract_saju_elements(person2_data)
            
            # 오행 궁합 계산
            wuxing_result = self.calculate_wuxing_compatibility(
                person1_elements.get("wuxing_score", {}),
                person2_elements.get("wuxing_score", {})
            )
            
            # 십성 궁합 계산
            sibseong_result = self.calculate_sibseong_compatibility(
                person1_elements.get("main_sibseong", "비견"),
                person2_elements.get("main_sibseong", "비견")
            )
            
            # 전체 점수 계산 (오행 60%, 십성 40%)
            overall_score = int(wuxing_result["score"] * 0.6 + sibseong_result["score"] * 0.4)
            
            # 세부 점수 계산
            love_score = int(wuxing_result["score"] * 0.7 + sibseong_result["score"] * 0.3)
            marriage_score = int(wuxing_result["score"] * 0.5 + sibseong_result["score"] * 0.5)
            communication_score = int(sibseong_result["score"] * 0.8 + wuxing_result["score"] * 0.2)
            values_score = int(wuxing_result["score"] * 0.4 + sibseong_result["score"] * 0.6)
            
            # 분석 결과 종합
            strengths = []
            weaknesses = []
            advice = []
            
            if overall_score >= 70:
                strengths.extend([
                    "서로를 이해하고 지지하는 관계",
                    "자연스러운 소통이 가능",
                    "상호 보완적인 성격"
                ])
                advice.extend([
                    "현재의 좋은 관계를 유지하세요",
                    "서로의 장점을 더욱 발휘할 수 있도록 격려하세요"
                ])
            else:
                weaknesses.extend([
                    "성격적 차이로 인한 갈등 가능성",
                    "서로 다른 가치관"
                ])
                advice.extend([
                    "서로의 차이점을 인정하고 이해하려 노력하세요",
                    "열린 마음으로 소통하는 시간을 늘리세요"
                ])
            
            if wuxing_result["score"] >= 70:
                strengths.append("오행 기운이 조화롭게 어우러짐")
            else:
                weaknesses.append("오행 상극으로 인한 에너지 충돌")
                advice.append("서로 다른 에너지를 이해하고 배려하세요")
            
            if sibseong_result["score"] >= 70:
                strengths.append("성격적으로 잘 맞는 조합")
            else:
                weaknesses.append("성격적 차이로 인한 오해 가능성")
                advice.append("상대방의 성격을 깊이 이해하려 노력하세요")
            
            return {
                "success": True,
                "overall_score": overall_score,
                "detailed_scores": {
                    "love": love_score,
                    "marriage": marriage_score,
                    "communication": communication_score,
                    "values": values_score
                },
                "wuxing_analysis": wuxing_result,
                "sibseong_analysis": sibseong_result,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "advice": advice,
                "summary": self.generate_summary(overall_score, person1_elements.get("name", "첫 번째 분"), person2_elements.get("name", "두 번째 분")),
                "analysis_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"전체 궁합 계산 실패: {e}")
            return {
                "success": False,
                "error": "compatibility_calculation_failed",
                "message": f"궁합 계산 중 오류가 발생했습니다: {str(e)}"
            }
    
    def generate_summary(self, score: int, name1: str, name2: str) -> str:
        """궁합 분석 요약 생성"""
        if score >= 80:
            return f"{name1}님과 {name2}님은 천생연분의 궁합입니다! 서로를 완벽하게 보완하며 행복한 관계를 만들어 갈 수 있습니다."
        elif score >= 60:
            return f"{name1}님과 {name2}님은 좋은 궁합을 가지고 있습니다. 서로를 이해하고 배려한다면 안정적이고 행복한 관계가 가능합니다."
        elif score >= 40:
            return f"{name1}님과 {name2}님은 노력이 필요한 관계입니다. 서로의 차이를 인정하고 소통을 늘린다면 좋은 관계로 발전할 수 있습니다."
        else:
            return f"{name1}님과 {name2}님은 많은 이해와 인내가 필요한 관계입니다. 하지만 진정한 사랑과 노력이 있다면 어떤 어려움도 극복할 수 있습니다."

# 글로벌 인스턴스
compatibility_engine = CompatibilityEngine()
