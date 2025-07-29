# Azure OpenAI 구현 계획 (백업/프로덕션용)

📅 **작성일**: 2025년 7월 29일  
🎯 **용도**: Google Gemini 이후 프로덕션/엔터프라이즈 환경 구축용

---

## 🏆 Azure OpenAI 장점

### **vs Google Gemini 비교**

| 항목 | **Azure OpenAI** | Google Gemini |
|------|------------------|---------------|
| **보안** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **안정성** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **기업용** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **비용** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **한국어** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔧 **Azure 리소스 설정 가이드**

### **Step 1: 리소스 그룹 생성**
```
이름: MSProject2-SAJU-RG
지역: Korea Central
태그: Project=SAJU, Environment=Production
```

### **Step 2: Azure OpenAI 서비스 생성**
```
서비스명: saju-openai-service
지역: Korea Central
가격 책정: Standard S0
```

### **Step 3: 모델 배포**
```
모델: gpt-4o (추천) 또는 gpt-35-turbo
배포 이름: saju-gpt4
버전: 최신
토큰 제한: 80K TPM (분당 토큰)
```

---

## 💻 **코드 구현**

### **환경 설정**
```bash
pip install openai azure-identity python-dotenv
```

### **환경 변수**
```bash
# .env
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://saju-openai-service.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=saju-gpt4
AZURE_OPENAI_API_VERSION=2024-02-01
```

### **Azure OpenAI 클라이언트**
```python
# app/services/azure_ai_interpreter.py
from openai import AzureOpenAI
import os

class AzureAIInterpreter:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    async def interpret_saju(self, analysis_result, question, context=None):
        """사주 분석 결과를 AI로 해석"""
        prompt = self._create_saju_prompt(analysis_result, question, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 30년 경력의 전문 명리학자입니다. 전통 명리학 이론을 바탕으로 정확하고 이해하기 쉬운 해석을 제공합니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9
            )
            
            return {
                "success": True,
                "ai_interpretation": response.choices[0].message.content,
                "usage": response.usage.dict(),
                "model": self.deployment_name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": "현재 AI 해석 서비스에 일시적인 문제가 있습니다."
            }
    
    def _create_saju_prompt(self, analysis, question, context):
        base_prompt = f"""
        사주 분석 결과:
        - 사주팔자: {analysis.get('palja', {})}
        - 오행 분석: {analysis.get('wuxing', {})}
        - 성격 분석: {analysis.get('personality', {})}
        - 십성 분석: {analysis.get('ten_stars', {})}
        
        사용자 질문: {question}
        분석 영역: {context or '전체'}
        
        위 사주 분석을 바탕으로 친근하면서도 전문적인 톤으로 해석해주세요.
        구체적이고 실용적인 조언을 포함해주세요.
        """
        return base_prompt
```

### **API 엔드포인트**
```python
# app/api/saju.py에 추가
from app.services.azure_ai_interpreter import AzureAIInterpreter

@router.post("/ai-chat")
async def ai_chat_interpretation(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="사용자 질문"),
    context: str = Query(None, description="분석 영역")
):
    """Azure OpenAI 기반 사주 해석"""
    try:
        # 기존 사주 분석
        analyzer = SajuAnalyzer()
        analysis_result = analyzer.analyze_saju(birth_info)
        
        # Azure AI 해석
        ai_interpreter = AzureAIInterpreter()
        ai_result = await ai_interpreter.interpret_saju(
            analysis_result, question, context
        )
        
        return {
            "success": True,
            "data": {
                "ai_interpretation": ai_result,
                "analysis_context": analysis_result,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 💰 **비용 계산**

### **예상 사용량 (월간)**
- 사용자 100명 × 분석 3회 = 300회
- 평균 토큰: 1,500 토큰/요청
- 총 토큰: 450,000 토큰/월

### **gpt-4o 기준**
- 입력: $0.0025/1K 토큰
- 출력: $0.01/1K 토큰
- **월 예상 비용**: 약 $5-7

### **gpt-35-turbo 기준**
- 입력: $0.0005/1K 토큰  
- 출력: $0.0015/1K 토큰
- **월 예상 비용**: 약 $1-2

---

## 🔐 **보안 및 거버넌스**

### **데이터 보호**
- Azure Private Link 설정
- VNET 통합
- 키 자격 증명 모음 사용

### **모니터링**
- Azure Monitor 설정
- Application Insights 연동
- 사용량 및 비용 알림

---

## 📈 **마이그레이션 계획**

### **Google Gemini → Azure OpenAI**

1. **환경 변수만 변경**
2. **클라이언트 클래스 교체**
3. **프롬프트 최적화**
4. **성능 테스트**

### **점진적 전환**
```python
# 하이브리드 AI 클라이언트
class HybridAIInterpreter:
    def __init__(self):
        self.gemini_client = GeminiAIInterpreter()
        self.azure_client = AzureAIInterpreter()
        self.use_azure = os.getenv("USE_AZURE_AI", "false").lower() == "true"
    
    async def interpret_saju(self, *args, **kwargs):
        if self.use_azure:
            return await self.azure_client.interpret_saju(*args, **kwargs)
        else:
            return await self.gemini_client.interpret_saju(*args, **kwargs)
```

---

## 🎯 **언제 Azure로 전환할까?**

### **전환 시점**
- 월 사용자 500명 초과
- 엔터프라이즈 고객 확보
- 높은 가용성 요구사항
- 규제 준수 필요

### **전환 장점**
- 99.9% SLA 보장
- 기업급 보안
- 전용 인스턴스
- 24/7 지원

---

**🎊 결론: Google Gemini로 시작 → 성장 시 Azure로 업그레이드**