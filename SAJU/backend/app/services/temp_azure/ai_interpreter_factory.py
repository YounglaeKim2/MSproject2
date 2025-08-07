"""
AI 해석 서비스 팩토리
Azure OpenAI와 Gemini 중 선택 가능
"""
import os
from typing import Dict, Any, Optional
from .azure_ai_interpreter import get_azure_ai_interpreter
from .gemini_ai_interpreter import get_gemini_interpreter


class AIInterpreterFactory:
    """AI 해석 서비스 선택을 위한 팩토리 클래스"""
    
    @staticmethod
    def get_interpreter(provider: str = "azure"):
        """
        AI 해석기 인스턴스 반환
        
        Args:
            provider: "azure" 또는 "gemini" (기본값: "azure")
            
        Returns:
            AI 해석기 인스턴스
        """
        provider = provider.lower()
        
        if provider == "azure":
            return get_azure_ai_interpreter()
        elif provider == "gemini":
            return get_gemini_interpreter()
        else:
            # 기본값은 Azure OpenAI
            print(f"알 수 없는 AI provider: {provider}. Azure OpenAI를 사용합니다.")
            return get_azure_ai_interpreter()
    
    @staticmethod
    def get_default_provider() -> str:
        """
        기본 AI provider 반환
        환경변수로 설정 가능, 기본값은 azure
        """
        return os.getenv("DEFAULT_AI_PROVIDER", "azure").lower()
    
    @staticmethod
    def get_available_providers() -> Dict[str, Dict[str, Any]]:
        """사용 가능한 AI provider 목록 반환"""
        return {
            "azure": {
                "name": "Azure OpenAI",
                "model": "gpt-4.1", 
                "description": "Microsoft Azure OpenAI GPT-4.1",
                "default": True
            },
            "gemini": {
                "name": "Google Gemini",
                "model": "gemini-2.5-flash",
                "description": "Google Gemini 2.5 Flash",
                "default": False
            }
        }


class UnifiedAIInterpreter:
    """통합 AI 해석 서비스 (기존 코드 호환성 유지)"""
    
    def __init__(self, provider: str = None):
        if provider is None:
            provider = AIInterpreterFactory.get_default_provider()
        
        self.provider = provider
        self.interpreter = AIInterpreterFactory.get_interpreter(provider)
    
    async def interpret_saju(self, analysis_result: Dict[str, Any], question: str, context: Optional[str] = None, tone: str = "concise") -> Dict[str, Any]:
        """사주 분석 결과를 AI로 해석 (통합 인터페이스)"""
        result = await self.interpreter.interpret_saju(analysis_result, question, context, tone)
        # provider 정보 추가
        result["provider"] = self.provider
        return result
    
    async def generate_suggested_questions(self, saju_result: Dict[str, Any], birth_info: Dict[str, Any]) -> Dict[str, Any]:
        """사주 분석 결과 기반 개인화된 질문 생성 (통합 인터페이스)"""
        result = await self.interpreter.generate_suggested_questions(saju_result, birth_info)
        # provider 정보 추가
        result["provider"] = self.provider
        return result
    
    async def test_connection(self) -> Dict[str, Any]:
        """AI 연결 테스트 (통합 인터페이스)"""
        result = await self.interpreter.test_connection()
        result["provider"] = self.provider
        return result
    
    def get_provider_info(self) -> Dict[str, Any]:
        """현재 사용 중인 provider 정보 반환"""
        providers = AIInterpreterFactory.get_available_providers()
        return {
            "current_provider": self.provider,
            "provider_info": providers.get(self.provider, {}),
            "available_providers": providers
        }


# 전역 인스턴스 (기존 코드 호환성)
unified_ai_interpreter = None

def get_unified_ai_interpreter(provider: str = None) -> UnifiedAIInterpreter:
    """통합 AI 해석기 인스턴스 반환"""
    global unified_ai_interpreter
    # provider가 변경될 수 있으므로 매번 새 인스턴스 생성
    unified_ai_interpreter = UnifiedAIInterpreter(provider)
    return unified_ai_interpreter

# 기존 코드와의 호환성을 위한 별칭
def get_ai_interpreter(provider: str = None):
    """기존 코드 호환용 함수"""
    return get_unified_ai_interpreter(provider)