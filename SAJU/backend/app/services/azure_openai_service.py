"""
Azure OpenAI 서비스 - 완전 독립형
기존 코드와 충돌 없이 동작
"""
import os
import sys
import json
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Windows UTF-8 설정 (주석 처리하여 인코딩 문제 방지)
# if sys.platform.startswith('win'):
#     import io
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#     sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class AzureOpenAIService:
    """Azure OpenAI 완전 독립 서비스"""
    
    def __init__(self):
        # Azure OpenAI 설정 (환경변수 필수)
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://1team-openai.openai.azure.com")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "saju-gpt-4.1")
        self.api_version = os.getenv("AZURE_OPENAI_VERSION", "2025-01-01-preview")
        
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        
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
    
    async def interpret_saju(self, saju_data: Dict[str, Any], question: str) -> Dict[str, Any]:
        """사주 해석 서비스"""
        try:
            system_prompt = """당신은 30년 경력의 친근한 명리학 전문가입니다. 
사주 분석 결과를 바탕으로 간결하고 따뜻한 조언을 제공합니다."""
            
            user_prompt = f"""
사주 정보: {json.dumps(saju_data, ensure_ascii=False, indent=2)}

질문: {question}

위 사주 분석을 바탕으로 친근하고 따뜻하게 답변해주세요:
- 핵심 내용 1-2줄로 요약
- 주요 특징 2-3개 
- 실용적인 조언 2개
- 200자 내외, 이모지 적절히 사용
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
    
    async def generate_questions(self, saju_data: Dict[str, Any], birth_info: Dict[str, Any]) -> Dict[str, Any]:
        """개인화된 질문 생성"""
        try:
            system_prompt = "당신은 사주 전문가로, 개인 맞춤형 질문을 생성하는 전문가입니다."
            
            user_prompt = f"""
사주 분석: {json.dumps(saju_data, ensure_ascii=False)}
개인 정보: {json.dumps(birth_info, ensure_ascii=False)}

이 분이 가장 궁금해할 만한 질문 5개를 다음 JSON 형식으로 생성해주세요:

{{
  "questions": [
    {{"question": "올해 하반기 연애운은 어떨까요?", "category": "연애", "priority": "high", "icon": "💕"}},
    {{"question": "현재 직장 상황은?", "category": "직업", "priority": "high", "icon": "💼"}},
    {{"question": "건강 관리 포인트는?", "category": "건강", "priority": "medium", "icon": "🏥"}},
    {{"question": "재물운 전망은?", "category": "재물", "priority": "medium", "icon": "💰"}},
    {{"question": "인간관계 개선 방법은?", "category": "인간관계", "priority": "low", "icon": "👥"}}
  ]
}}

개인의 사주 특성에 맞게 구체적이고 실용적인 질문으로 작성해주세요.
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
                questions = self._get_default_questions()
            
            return {
                "suggested_questions": questions,
                "generation_method": "azure_ai",
                "provider": "azure_openai", 
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(questions)
            }
            
        except Exception as e:
            return {
                "suggested_questions": self._get_default_questions(),
                "generation_method": "fallback",
                "provider": "azure_openai",
                "error": str(e)
            }
    
    def _get_default_questions(self) -> list:
        """기본 질문들 (폴백용)"""
        return [
            {"question": "올해 전반적인 운세는 어떤가요?", "category": "전체운", "priority": "high", "icon": "🔮"},
            {"question": "연애운이 궁금해요", "category": "연애", "priority": "high", "icon": "💕"},
            {"question": "직장 생활은 어떨까요?", "category": "직업", "priority": "medium", "icon": "💼"},
            {"question": "건강 상태는?", "category": "건강", "priority": "medium", "icon": "🏥"},
            {"question": "금전운은 어떤지 궁금해요", "category": "재물", "priority": "low", "icon": "💰"}
        ]
    
    async def test_connection(self) -> Dict[str, Any]:
        """연결 테스트"""
        try:
            test_response = await self.chat_completion("안녕하세요! Azure OpenAI 테스트입니다.", 
                                                    "간단히 인사말로 응답해주세요.")
            
            return {
                "success": True,
                "message": "Azure OpenAI 연결 성공",
                "provider": "azure_openai",
                "model": "gpt-4.1",
                "response": test_response[:100] + "..."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Azure OpenAI 연결 실패",
                "provider": "azure_openai",
                "error": str(e)
            }


# 전역 인스턴스
_azure_service = None

def get_azure_service() -> AzureOpenAIService:
    """Azure OpenAI 서비스 인스턴스 반환"""
    global _azure_service
    if _azure_service is None:
        _azure_service = AzureOpenAIService()
    return _azure_service