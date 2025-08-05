"""
Google Gemini AI 기반 사주 해석 서비스
"""
import os
import sys

# Windows에서 UTF-8 인코딩 강제 설정
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import json
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class GeminiUsageTracker:
    """Gemini API 사용량 추적 및 제한"""
    
    def __init__(self):
        self.usage_file = "gemini_usage.json"
        self.load_usage()
    
    def load_usage(self):
        """사용량 파일 로드"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    self.usage_data = json.load(f)
            else:
                self.usage_data = {
                    "daily": {"date": "", "count": 0},
                    "monthly": {"month": "", "count": 0}
                }
        except Exception as e:
            print(f"사용량 파일 로드 실패: {e}")
            self.usage_data = {
                "daily": {"date": "", "count": 0},
                "monthly": {"month": "", "count": 0}
            }
    
    def save_usage(self):
        """사용량 파일 저장"""
        try:
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"사용량 파일 저장 실패: {e}")
    
    def check_and_update_usage(self) -> bool:
        """사용량 체크 및 업데이트"""
        today = datetime.now().strftime("%Y-%m-%d")
        this_month = datetime.now().strftime("%Y-%m")
        
        daily_limit = int(os.getenv("GEMINI_DAILY_LIMIT", 1000))
        monthly_limit = int(os.getenv("GEMINI_MONTHLY_LIMIT", 30000))
        
        # 일일 사용량 체크
        if self.usage_data["daily"]["date"] != today:
            self.usage_data["daily"] = {"date": today, "count": 0}
        
        # 월간 사용량 체크
        if self.usage_data["monthly"]["month"] != this_month:
            self.usage_data["monthly"] = {"month": this_month, "count": 0}
        
        # 한도 체크
        if self.usage_data["daily"]["count"] >= daily_limit:
            return False
        if self.usage_data["monthly"]["count"] >= monthly_limit:
            return False
        
        # 사용량 증가
        self.usage_data["daily"]["count"] += 1
        self.usage_data["monthly"]["count"] += 1
        self.save_usage()
        
        return True
    
    def get_usage_status(self) -> Dict[str, Any]:
        """현재 사용량 상태 반환"""
        daily_limit = int(os.getenv("GEMINI_DAILY_LIMIT", 1000))
        monthly_limit = int(os.getenv("GEMINI_MONTHLY_LIMIT", 30000))
        
        return {
            "daily": {
                "used": self.usage_data["daily"]["count"],
                "limit": daily_limit,
                "remaining": daily_limit - self.usage_data["daily"]["count"]
            },
            "monthly": {
                "used": self.usage_data["monthly"]["count"],
                "limit": monthly_limit,
                "remaining": monthly_limit - self.usage_data["monthly"]["count"]
            }
        }


class GeminiAIInterpreter:
    """Google Gemini AI 사주 해석 서비스"""
    
    def __init__(self):
        # Gemini API 설정 (임시로 직접 설정)
        api_key = "AIzaSyD7OB3MnPASwL6oN7_Ni8hKyPWOEACYeIo"
        
        # REST API 방식
        self.api_key = api_key
        self.model_name = "gemini-2.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
        
        # 사용량 추적기
        self.usage_tracker = GeminiUsageTracker()
        
        # AI 설정
        self.temperature = float(os.getenv("AI_TEMPERATURE", 0.7))
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", 1000))
        self.top_p = float(os.getenv("AI_TOP_P", 0.9))
    
    async def interpret_saju(self, analysis_result: Dict[str, Any], question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """사주 분석 결과를 AI로 해석"""
        try:
            # 사용량 체크
            if not self.usage_tracker.check_and_update_usage():
                paid_enabled = os.getenv("ENABLE_PAID_GEMINI", "false").lower() == "true"
                if not paid_enabled:
                    return {
                        "success": False,
                        "error": "daily_limit_exceeded",
                        "message": "일일 무료 사용량을 초과했습니다. 내일 다시 이용해주세요.",
                        "usage_status": self.usage_tracker.get_usage_status()
                    }
            
            # 프롬프트 생성
            prompt = self._create_saju_prompt(analysis_result, question, context)
            
            # Gemini API 호출
            response = await self._call_gemini_async(prompt)
            
            return {
                "success": True,
                "ai_interpretation": response,
                "usage_status": self.usage_tracker.get_usage_status(),
                "model": "gemini-2.5-flash",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": "현재 AI 해석 서비스에 일시적인 문제가 있습니다. 기본 분석 결과를 참고해주세요.",
                "usage_status": self.usage_tracker.get_usage_status()
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
    
    def _create_saju_prompt(self, analysis_result: Dict[str, Any], question: str, context: Optional[str] = None) -> str:
        """사주 해석용 프롬프트 생성"""
        
        # 분석 결과 요약
        palja_info = analysis_result.get('palja', {})
        wuxing_info = analysis_result.get('wuxing', {})
        personality_info = analysis_result.get('personality', {})
        ten_stars_info = analysis_result.get('ten_stars', {})
        
        base_prompt = f"""당신은 30년 경력의 전문 명리학자입니다. 
전통 명리학 이론을 바탕으로 정확하고 이해하기 쉬운 해석을 제공합니다.

<사주 분석 결과>
■ 사주팔자:
- 년주: {palja_info.get('year_pillar', '')}
- 월주: {palja_info.get('month_pillar', '')}  
- 일주: {palja_info.get('day_pillar', '')}
- 시주: {palja_info.get('hour_pillar', '')}

■ 오행 분석:
- 오행 분포: {wuxing_info.get('distribution', {})}
- 균형 점수: {wuxing_info.get('balance_score', 0)}점
- 강약: {wuxing_info.get('strength', '')}

■ 성격 분석:
- 기본 성격: {personality_info.get('basic_nature', '')}
- 강점: {personality_info.get('strengths', [])}
- 약점: {personality_info.get('weaknesses', [])}

■ 십성 분석:
- 주요 십성: {ten_stars_info.get('dominant_stars', [])}
- 특징: {ten_stars_info.get('characteristics', '')}

<사용자 질문>
{question}

<분석 영역>
{context or '전체 사주 분석'}

<응답 가이드라인>
1. 친근하면서도 전문적인 톤으로 작성
2. 전통 명리학 이론을 바탕으로 설명
3. 구체적이고 실용적인 조언 포함
4. 너무 단정적이지 않게 "~하는 경향이 있습니다" 식으로 표현
5. 긍정적이고 건설적인 방향으로 해석
6. 1000자 이내로 간결하게 작성

위의 사주 분석을 바탕으로 사용자의 질문에 대해 전문적이고 친근한 해석을 제공해주세요."""

        return base_prompt
    
    def get_usage_status(self) -> Dict[str, Any]:
        """현재 사용량 상태 조회"""
        return self.usage_tracker.get_usage_status()
    
    async def generate_suggested_questions(self, saju_result: Dict[str, Any], birth_info: Dict[str, Any]) -> Dict[str, Any]:
        """사주 분석 결과 기반 개인화된 질문 생성"""
        try:
            # 사용량 체크
            if not self.usage_tracker.check_and_update_usage():
                paid_enabled = os.getenv("ENABLE_PAID_GEMINI", "false").lower() == "true"
                if not paid_enabled:
                    raise Exception("AI 사용량 초과")
            
            # 질문 생성 프롬프트
            prompt = self._create_question_generation_prompt(saju_result, birth_info)
            
            # Gemini API 호출
            response = await self._call_gemini_async(prompt)
            
            # JSON 파싱 및 검증
            questions = self._parse_and_validate_questions(response)
            
            return {
                "suggested_questions": questions,
                "generation_method": "ai",
                "usage_status": self.usage_tracker.get_usage_status(),
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(questions)
            }
            
        except Exception as e:
            print(f"AI 질문 생성 실패: {e}")
            raise e
    
    def _create_question_generation_prompt(self, saju_result: Dict[str, Any], birth_info: Dict[str, Any]) -> str:
        """질문 생성용 프롬프트 작성"""
        
        # 주요 분석 결과 추출
        palja = saju_result.get('palja', {})
        wuxing = saju_result.get('wuxing', {})
        personality = saju_result.get('personality', {})
        ten_stars = saju_result.get('ten_stars', {})
        
        return f"""당신은 30년 경력의 전문 명리학자입니다.
다음 사주 분석 결과를 바탕으로 이 분이 가장 궁금해할 만한 개인화된 질문 5개를 생성해주세요.

<개인 정보>
- 이름: {birth_info.get('name', '')}
- 성별: {birth_info.get('gender', '')}
- 생년: {birth_info.get('year', '')}년

<사주 분석 결과>
■ 사주팔자:
- 년주: {palja.get('year_pillar', '')}
- 월주: {palja.get('month_pillar', '')}
- 일주: {palja.get('day_pillar', '')}
- 시주: {palja.get('hour_pillar', '')}

■ 오행 분석:
- 분포: {wuxing.get('distribution', {})}
- 균형: {wuxing.get('balance_score', 0)}점
- 강약: {wuxing.get('strength', '')}

■ 성격 특성:
- 기본 성격: {personality.get('basic_nature', '')}
- 주요 강점: {personality.get('strengths', [])}

■ 십성 분석:
- 주요 십성: {ten_stars.get('dominant_stars', [])}

<질문 생성 가이드라인>
1. 개인의 사주 특성을 반영한 구체적 질문
2. 실용적이고 현실적인 관심사
3. 5개 카테고리 균형: 연애/직업/건강/재물/인간관계
4. 친근하고 자연스러운 말투
5. 각 질문은 20-30자 내외

반드시 다음 JSON 형식으로만 응답하세요:
{{
  "questions": [
    {{"question": "올해 하반기 연애운이 어떨까요?", "category": "연애", "priority": "high", "icon": "💕"}},
    {{"question": "현재 직장에서 승진 가능성은?", "category": "직업", "priority": "high", "icon": "💼"}},
    {{"question": "건강 관리에서 주의할 점은?", "category": "건강", "priority": "medium", "icon": "🏥"}},
    {{"question": "투자하기 좋은 시기는 언제?", "category": "재물", "priority": "medium", "icon": "💰"}},
    {{"question": "인간관계 개선 방법은?", "category": "인간관계", "priority": "low", "icon": "👥"}}
  ]
}}"""

    def _parse_and_validate_questions(self, response: str) -> list:
        """AI 응답에서 질문 파싱 및 검증"""
        try:
            import json
            import re
            
            # JSON 부분만 추출 (가능한 경우)
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

    async def test_connection(self) -> Dict[str, Any]:
        """Gemini REST API 연결 테스트"""
        try:
            test_prompt = "안녕하세요! 연결 테스트입니다."
            response = await self._call_gemini_async(test_prompt)
            return {
                "success": True,
                "message": "Gemini AI 연결 성공",
                "response": response[:100] + "..."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Gemini AI 연결 실패"
            }


# 전역 인스턴스 (싱글톤 패턴)
gemini_interpreter = None

def get_gemini_interpreter() -> GeminiAIInterpreter:
    """Gemini AI 해석기 인스턴스 반환"""
    global gemini_interpreter
    # 항상 새 인스턴스 생성 (환경변수 변경 반영)
    gemini_interpreter = GeminiAIInterpreter()
    return gemini_interpreter