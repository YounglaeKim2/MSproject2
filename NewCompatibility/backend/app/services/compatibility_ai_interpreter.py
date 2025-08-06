"""
NewCompatibility용 Gemini AI 해석 서비스
SAJU의 AI 서비스를 궁합 분석에 특화
"""
import os
import sys
import json
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class CompatibilityAIInterpreter:
    """궁합 분석 전용 Gemini AI 해석 서비스"""
    
    def __init__(self):
        # Gemini API 설정 (SAJU와 동일한 키 사용)
        self.api_key = "AIzaSyD7OB3MnPASwL6oN7_Ni8hKyPWOEACYeIo"
        self.model_name = "gemini-2.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
        
        # AI 설정
        self.temperature = 0.7
        self.max_tokens = 1000
        self.top_p = 0.9
        
    async def interpret_compatibility(self, compatibility_result: Dict[str, Any], question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """궁합 분석 결과를 AI로 해석"""
        try:
            # 프롬프트 생성
            prompt = self._create_compatibility_prompt(compatibility_result, question, context)
            
            # Gemini API 호출
            response = await self._call_gemini_async(prompt)
            
            return {
                "success": True,
                "ai_interpretation": response,
                "model": "gemini-2.5-flash",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": "현재 AI 해석 서비스에 일시적인 문제가 있습니다. 기본 분석 결과를 참고해주세요."
            }

    async def generate_suggested_questions(self, compatibility_result: Dict[str, Any], persons_info: Dict[str, Any]) -> Dict[str, Any]:
        """궁합 분석 결과 기반 개인화된 질문 생성"""
        try:
            # 질문 생성 프롬프트
            prompt = self._create_question_generation_prompt(compatibility_result, persons_info)
            
            # Gemini API 호출
            response = await self._call_gemini_async(prompt)
            
            # JSON 파싱 및 검증
            questions = self._parse_and_validate_questions(response)
            
            return {
                "suggested_questions": questions,
                "generation_method": "ai",
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(questions)
            }
            
        except Exception as e:
            print(f"AI 질문 생성 실패: {e}")
            return {
                "suggested_questions": self._get_fallback_questions(),
                "generation_method": "fallback",
                "error": str(e)
            }

    async def _call_gemini_async(self, prompt: str) -> str:
        """비동기 Gemini REST API 호출"""
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    error_text = await response.text()
                    raise Exception(f"Gemini API 오류 ({response.status}): {error_text}")

    def _create_compatibility_prompt(self, compatibility_result: Dict[str, Any], question: str, context: Optional[str] = None) -> str:
        """궁합 해석용 프롬프트 생성"""
        
        score = compatibility_result.get('score', {})
        analysis = compatibility_result.get('analysis', {})
        persons = compatibility_result.get('persons', {})
        
        # 간결하면서 친근한 톤
        base_prompt = f"""당신은 간결하고 친근한 궁합 상담사입니다.

**궁합 정보:**
• 점수: {score.get('total', 0)}점 
• 등급: {score.get('grade', '')}

**질문:** {question}

**간결하면서 친근하게 답변해주세요:**
## 핵심 결과 💕
- (1줄로 친근하게 요약)

## 궁합 특징 ✨
- 특징 1 (간결하게)
- 특징 2 (간결하게)  
- 특징 3 (간결하게)

## 관계 조언 😊
- 조언 1 (친근하게)
- 조언 2 (친근하게)

**200자 내외로 간결하면서도 따뜻하게 작성하세요. "두 분은 ~하시네요", "~해보시면 좋겠어요" 같은 친근한 말투와 적절한 이모지 사용.**"""

        return base_prompt

    def _create_question_generation_prompt(self, compatibility_result: Dict[str, Any], persons_info: Dict[str, Any]) -> str:
        """질문 생성용 프롬프트 작성"""
        
        score = compatibility_result.get('score', {})
        analysis = compatibility_result.get('analysis', {})
        persons = compatibility_result.get('persons', {})
        
        return f"""당신은 30년 경력의 전문 명리학자입니다.
다음 궁합 분석 결과를 바탕으로 이 두 분이 가장 궁금해할 만한 개인화된 질문 5개를 생성해주세요.

<두 분의 정보>
- {persons.get('person1', {}).get('name', '')} & {persons.get('person2', {}).get('name', '')}
- 궁합 점수: {score.get('total', 0)}점 ({score.get('grade', '')})

<궁합 분석 결과>
■ 종합 평가: {analysis.get('overall_summary', '')}
■ 오행 상성: {analysis.get('wuxing_compatibility', '')}
■ 십성 배합: {analysis.get('ten_gods_compatibility', '')}

<질문 생성 가이드라인>
1. 궁합 결과에 특화된 구체적 질문
2. 실용적이고 현실적인 관심사 (연애, 결혼, 갈등 해결 등)
3. 5개 카테고리 균형: 연애발전/결혼궁합/갈등해결/소통방법/미래전망
4. 친근하고 자연스러운 말투
5. 각 질문은 20-30자 내외

반드시 다음 JSON 형식으로만 응답하세요:
{{
  "questions": [
    {{"question": "우리 둘이 결혼하면 어떨까요?", "category": "결혼궁합", "priority": "high", "icon": "💒"}},
    {{"question": "갈등이 생겼을 때 해결 방법은?", "category": "갈등해결", "priority": "high", "icon": "🤝"}},
    {{"question": "서로 소통할 때 주의할 점은?", "category": "소통방법", "priority": "medium", "icon": "💬"}},
    {{"question": "장기적으로 관계가 어떻게 발전할까요?", "category": "미래전망", "priority": "medium", "icon": "🔮"}},
    {{"question": "연애를 더 발전시키려면?", "category": "연애발전", "priority": "low", "icon": "💕"}}
  ]
}}"""

    def _parse_and_validate_questions(self, response: str) -> list:
        """AI 응답에서 질문 파싱 및 검증"""
        try:
            import re
            
            # JSON 부분만 추출
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
            else:
                data = json.loads(response)
                
            questions = data.get("questions", [])
            
            # 검증: 5개 질문, 필수 필드 존재
            if len(questions) != 5:
                raise ValueError(f"질문 개수가 {len(questions)}개임 (5개 필요)")
                
            for i, q in enumerate(questions):
                required_fields = ["question", "category", "priority", "icon"]
                missing_fields = [f for f in required_fields if f not in q]
                if missing_fields:
                    raise ValueError(f"질문 {i+1}에서 필드 누락: {missing_fields}")
                    
            return questions
            
        except Exception as e:
            print(f"질문 파싱 실패: {e}")
            print(f"AI 응답 원문: {response[:500]}...")
            raise ValueError(f"AI 응답 파싱 실패: {e}")

    def _get_fallback_questions(self) -> list:
        """폴백 질문들 (AI 실패 시 사용)"""
        return [
            {"question": "우리 둘의 궁합은 어떤가요?", "category": "전체궁합", "priority": "high", "icon": "💕"},
            {"question": "결혼하면 행복할까요?", "category": "결혼궁합", "priority": "high", "icon": "💒"},
            {"question": "서로 다른 점을 어떻게 맞춰갈까요?", "category": "갈등해결", "priority": "medium", "icon": "🤝"},
            {"question": "소통할 때 주의할 점은?", "category": "소통방법", "priority": "medium", "icon": "💬"},
            {"question": "미래에 어떤 관계가 될까요?", "category": "미래전망", "priority": "low", "icon": "🔮"}
        ]

    async def test_connection(self) -> Dict[str, Any]:
        """Gemini REST API 연결 테스트"""
        try:
            test_prompt = "안녕하세요! 궁합 분석 AI 연결 테스트입니다."
            response = await self._call_gemini_async(test_prompt)
            return {
                "success": True,
                "message": "궁합 AI 연결 성공",
                "response": response[:100] + "..."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "궁합 AI 연결 실패"
            }

# 전역 인스턴스 (싱글톤 패턴)
compatibility_ai_interpreter = None

def get_compatibility_ai_interpreter() -> CompatibilityAIInterpreter:
    """궁합 AI 해석기 인스턴스 반환"""
    global compatibility_ai_interpreter
    if compatibility_ai_interpreter is None:
        compatibility_ai_interpreter = CompatibilityAIInterpreter()
    return compatibility_ai_interpreter
