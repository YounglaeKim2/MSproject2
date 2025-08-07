"""
Azure OpenAI 서비스 - NewCompatibility 전용
SAJU의 Azure 서비스를 궁합 분석에 특화
"""
import os
import sys
import json
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime

class AzureCompatibilityAIService:
    """Azure OpenAI 궁합 분석 전용 서비스"""
    
    def __init__(self):
        # Azure OpenAI 설정 (환경변수 사용)
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY", "your-azure-openai-api-key-here")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://1team-openai.openai.azure.com")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "saju-gpt-4.1")
        self.api_version = os.getenv("AZURE_OPENAI_VERSION", "2025-01-01-preview")
        
        # API URL 구성
        self.api_url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        # 설정값
        self.temperature = 0.7
        self.max_tokens = 1000
        self.top_p = 0.9
    
    async def chat_completion(self, messages: list, system_prompt: str = None) -> str:
        """Azure OpenAI Chat Completion API 호출"""
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        # 메시지 구성
        chat_messages = []
        if system_prompt:
            chat_messages.append({"role": "system", "content": system_prompt})
        
        if isinstance(messages, str):
            chat_messages.append({"role": "user", "content": messages})
        elif isinstance(messages, list):
            chat_messages.extend(messages)
        
        payload = {
            "messages": chat_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    raise Exception(f"Azure OpenAI API 오류 ({response.status}): {error_text}")
    
    async def interpret_compatibility(self, compatibility_data: Dict[str, Any], question: str) -> Dict[str, Any]:
        """궁합 분석 해석 서비스"""
        try:
            system_prompt = """당신은 30년 경력의 친근한 명리학 궁합 전문가입니다. 
궁합 분석 결과를 바탕으로 간결하고 따뜻한 조언을 제공합니다.
두 분의 관계에 실질적으로 도움이 되는 조언을 해주세요."""
            
            user_prompt = f"""
궁합 정보: {json.dumps(compatibility_data, ensure_ascii=False, indent=2)}

질문: {question}

위 궁합 분석을 바탕으로 친근하고 따뜻하게 답변해주세요:
- 핵심 내용 1-2줄로 요약 
- 두 분의 궁합 특징 2-3개
- 관계 개선을 위한 실용적 조언 2개
- 200자 내외, 이모지 적절히 사용 💕
            """
            
            response = await self.chat_completion(user_prompt, system_prompt)
            
            return {
                "success": True,
                "ai_interpretation": response,
                "provider": "azure_openai",
                "model": "gpt-4.1",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "azure_openai",
                "fallback": "Azure OpenAI 서비스에 일시적 문제가 발생했습니다."
            }
    
    async def generate_compatibility_questions(self, compatibility_data: Dict[str, Any], persons_info: Dict[str, Any]) -> Dict[str, Any]:
        """궁합 전용 개인화된 질문 생성"""
        try:
            system_prompt = "당신은 궁합 전문가로, 커플/부부의 관계에 특화된 질문을 생성하는 전문가입니다."
            
            score = compatibility_data.get('score', {})
            persons = compatibility_data.get('persons', {})
            
            user_prompt = f"""
궁합 분석: {json.dumps(compatibility_data, ensure_ascii=False)}
두 분 정보: {json.dumps(persons_info, ensure_ascii=False)}

{persons.get('person1', {}).get('name', '')}님과 {persons.get('person2', {}).get('name', '')}님의 궁합이 {score.get('total', 0)}점입니다.

이 두 분이 가장 궁금해할 만한 궁합 관련 질문 5개를 다음 JSON 형식으로 생성해주세요:

{{
  "questions": [
    {{"question": "우리 둘이 결혼하면 어떨까요?", "category": "결혼궁합", "priority": "high", "icon": "💒"}},
    {{"question": "갈등이 생겼을 때 해결 방법은?", "category": "갈등해결", "priority": "high", "icon": "🤝"}},
    {{"question": "서로 소통할 때 주의할 점은?", "category": "소통방법", "priority": "medium", "icon": "💬"}},
    {{"question": "장기적으로 관계가 어떻게 발전할까요?", "category": "미래전망", "priority": "medium", "icon": "🔮"}},
    {{"question": "연애를 더 발전시키려면?", "category": "연애발전", "priority": "low", "icon": "💕"}}
  ]
}}

궁합 점수와 특성을 반영해서 구체적이고 실용적인 질문으로 작성해주세요.
            """
            
            response = await self.chat_completion(user_prompt, system_prompt)
            
            # JSON 파싱
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    questions_data = json.loads(json_match.group())
                    questions = questions_data.get("questions", [])
                else:
                    questions = []
                    
            except:
                questions = self._get_default_compatibility_questions()
            
            return {
                "suggested_questions": questions,
                "generation_method": "azure_ai_compatibility",
                "provider": "azure_openai", 
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(questions)
            }
            
        except Exception as e:
            return {
                "suggested_questions": self._get_default_compatibility_questions(),
                "generation_method": "fallback_compatibility",
                "provider": "azure_openai",
                "error": str(e)
            }
    
    def _get_default_compatibility_questions(self) -> list:
        """궁합 전용 기본 질문들 (폴백용)"""
        return [
            {"question": "우리 둘의 궁합은 어떤가요?", "category": "전체궁합", "priority": "high", "icon": "💕"},
            {"question": "결혼하면 행복할까요?", "category": "결혼궁합", "priority": "high", "icon": "💒"},
            {"question": "서로 다른 점을 어떻게 맞춰갈까요?", "category": "갈등해결", "priority": "medium", "icon": "🤝"},
            {"question": "소통할 때 주의할 점은?", "category": "소통방법", "priority": "medium", "icon": "💬"},
            {"question": "미래에 어떤 관계가 될까요?", "category": "미래전망", "priority": "low", "icon": "🔮"}
        ]
    
    async def test_connection(self) -> Dict[str, Any]:
        """연결 테스트"""
        try:
            test_response = await self.chat_completion(
                "안녕하세요! Azure OpenAI 궁합 분석 테스트입니다.", 
                "간단히 궁합 전문가로서 인사말로 응답해주세요."
            )
            
            return {
                "success": True,
                "message": "Azure OpenAI 궁합 AI 연결 성공",
                "provider": "azure_openai",
                "model": "gpt-4.1",
                "service": "compatibility",
                "response": test_response[:100] + "..."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Azure OpenAI 궁합 AI 연결 실패",
                "provider": "azure_openai",
                "service": "compatibility",
                "error": str(e)
            }


# 전역 인스턴스
_azure_compatibility_service = None

def get_azure_compatibility_service() -> AzureCompatibilityAIService:
    """Azure OpenAI 궁합 서비스 인스턴스 반환"""
    global _azure_compatibility_service
    if _azure_compatibility_service is None:
        _azure_compatibility_service = AzureCompatibilityAIService()
    return _azure_compatibility_service