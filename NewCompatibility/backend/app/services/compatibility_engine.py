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
    
    def polarize_score(self, raw_score: int) -> int:
        """
        점수 극단화: 중간 점수를 피하고 명확한 결과 제공
        50점을 기준으로 좋은 궁합(70-100) 또는 나쁜 궁합(0-30)으로 극단화
        """
        try:
            # 기준점 설정
            neutral_point = 50
            good_threshold = 60  # 이 이상이면 좋은 궁합으로 판단
            bad_threshold = 40   # 이 이하면 나쁜 궁합으로 판단
            
            if raw_score >= good_threshold:
                # 좋은 궁합 구간 (70-100)으로 매핑
                # 60-90 점수를 70-100으로 스케일링
                normalized = min((raw_score - good_threshold) / (90 - good_threshold), 1.0)
                polarized = int(70 + normalized * 30)
                return max(70, min(100, polarized))
            
            elif raw_score <= bad_threshold:
                # 나쁜 궁합 구간 (0-30)으로 매핑  
                # 25-40 점수를 0-30으로 스케일링
                normalized = max((raw_score - 25) / (bad_threshold - 25), 0.0)
                polarized = int(normalized * 30)
                return max(0, min(30, polarized))
            
            else:
                # 애매한 중간 구간 (40-60)
                # 50을 기준으로 좋은 쪽 또는 나쁜 쪽으로 극단화
                if raw_score >= neutral_point:
                    # 50 이상이면 좋은 궁합 쪽으로
                    return 75  # 좋은 궁합의 시작점
                else:
                    # 50 미만이면 나쁜 궁합 쪽으로
                    return 25  # 나쁜 궁합의 끝점
                    
        except Exception as e:
            logger.error(f"점수 극단화 실패: {e}")
            # 실패 시 원래 점수 반환
            return raw_score
    
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
            raw_overall_score = int(wuxing_result["score"] * 0.6 + sibseong_result["score"] * 0.4)
            
            # 점수 극단화 적용 (0-30 또는 70-100)
            overall_score = self.polarize_score(raw_overall_score)
            
            # 세부 점수 계산 및 극단화
            raw_love_score = int(wuxing_result["score"] * 0.7 + sibseong_result["score"] * 0.3)
            raw_marriage_score = int(wuxing_result["score"] * 0.5 + sibseong_result["score"] * 0.5)
            raw_communication_score = int(sibseong_result["score"] * 0.8 + wuxing_result["score"] * 0.2)
            raw_values_score = int(wuxing_result["score"] * 0.4 + sibseong_result["score"] * 0.6)
            
            love_score = self.polarize_score(raw_love_score)
            marriage_score = self.polarize_score(raw_marriage_score)
            communication_score = self.polarize_score(raw_communication_score)
            values_score = self.polarize_score(raw_values_score)
            
            # 분석 결과 종합 (극단화된 점수 기준)
            strengths = []
            weaknesses = []
            advice = []
            
            if overall_score >= 70:
                # 좋은 궁합 (70-100점)
                strengths.extend([
                    "천생연분의 완벽한 조화",
                    "서로를 깊이 이해하고 지지하는 관계",
                    "자연스럽고 편안한 소통",
                    "상호 보완적인 완벽한 성격 매칭"
                ])
                advice.extend([
                    "이미 훌륭한 궁합을 가지고 있으니 현재 관계를 소중히 여기세요",
                    "서로의 장점을 더욱 발휘할 수 있도록 적극적으로 격려하세요",
                    "함께하는 시간을 늘리고 더 깊은 유대감을 형성하세요"
                ])
            else:
                # 나쁜 궁합 (0-30점)
                weaknesses.extend([
                    "근본적인 성격 차이로 인한 잦은 갈등",
                    "완전히 다른 가치관과 인생관",
                    "소통의 어려움과 오해 빈발",
                    "에너지와 기운의 상극 관계"
                ])
                advice.extend([
                    "관계 개선을 위해서는 상당한 노력과 시간이 필요합니다",
                    "서로의 근본적인 차이를 인정하고 존중하는 마음가짐이 중요합니다",
                    "전문가의 도움을 받아 소통 방법을 개선해보세요",
                    "무리하지 말고 서로에게 맞는 거리감을 찾아보세요"
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
        """궁합 분석 요약 생성 (극단화된 점수 기준)"""
        if score >= 70:
            # 좋은 궁합 (70-100점)
            if score >= 90:
                return f"✨ {name1}님과 {name2}님은 완벽한 천생연분입니다! 서로를 완전히 보완하는 이상적인 관계로, 함께하면 무한한 행복과 성장을 이루어 갈 수 있습니다."
            elif score >= 80:
                return f"💕 {name1}님과 {name2}님은 매우 훌륭한 궁합을 가지고 있습니다! 서로 깊이 이해하며 자연스럽게 어우러지는 조화로운 관계입니다."
            else:
                return f"💖 {name1}님과 {name2}님은 좋은 궁합입니다! 서로를 지지하고 배려하며 안정적이고 행복한 관계를 만들어 갈 수 있습니다."
        else:
            # 나쁜 궁합 (0-30점)
            if score <= 10:
                return f"⚠️ {name1}님과 {name2}님은 매우 어려운 궁합입니다. 근본적인 차이가 커서 관계 유지에 상당한 어려움이 예상됩니다. 신중한 결정이 필요합니다."
            elif score <= 20:
                return f"🤔 {name1}님과 {name2}님은 어려운 궁합입니다. 많은 갈등과 오해가 발생할 수 있으며, 관계 개선을 위해서는 전문적인 도움과 지속적인 노력이 필요합니다."
            else:
                return f"😔 {name1}님과 {name2}님은 힘든 궁합입니다. 성격과 가치관의 차이로 인한 갈등이 잦을 수 있지만, 서로를 깊이 이해하려는 노력이 있다면 극복할 수 있습니다."

# 글로벌 인스턴스
compatibility_engine = CompatibilityEngine()
