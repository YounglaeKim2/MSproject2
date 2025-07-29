# SAJU AI 하이브리드 모델 구현 계획

📅 **작업 시작일**: 2025년 7월 29일  
🎯 **목표**: 기존 SAJU 서비스에 AI 기능 통합하여 사용자 경험 향상

---

## 🧠 하이브리드 AI 전략

### **Phase 1: Google Gemini AI 통합** (즉시 구현) ⭐ **현재 계획**
- **목적**: 빠른 프로토타이핑 및 서비스 출시
- **기술**: Google Gemini API (무료 한도 존재)
- **기간**: 1-2주
- **장점**: 무료 시작, 한국어 우수, 빠른 구현

### **Phase 2: 특화 모델 개발** (3-6개월 후)
- **목적**: 사주 전용 정확도 향상
- **기술**: TensorFlow + 수집된 사용자 데이터
- **기간**: 3-6개월

---

## 🚀 Phase 1 구현 우선순위

### 1️⃣ **AI 대화형 해석 기능** (최우선)

#### **기능 설명**
- 기존 37개 분석 메서드 결과를 AI가 자연어로 해석
- 사용자 질문에 맞춤형 답변 제공
- 전문적이면서도 이해하기 쉬운 해석

#### **API 설계**
```http
POST /api/v1/saju/ai-chat
Content-Type: application/json

{
  "birth_info": {
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "gender": "male",
    "name": "홍길동"
  },
  "question": "내 성격의 장단점을 자세히 설명해주세요",
  "context": "personality" // optional: personality|career|health|relationship|fortune
}
```

#### **응답 형식**
```json
{
  "success": true,
  "data": {
    "ai_interpretation": "홍길동님의 사주를 분석한 결과...",
    "analysis_context": {
      "palja": {...},
      "personality": {...},
      "relevant_data": {...}
    },
    "confidence_score": 0.95,
    "timestamp": "2025-07-29T10:00:00Z"
  }
}
```

#### **구현 파일**
- `SAJU/backend/app/services/ai_interpreter.py` (신규)
- `SAJU/backend/app/api/saju.py` (수정)
- `SAJU/frontend/src/components/AIChatInterface.tsx` (신규)

### 2️⃣ **AI 운세 조언 기능**

#### **기능 설명**
- 일일/주간/월간 개인화된 운세 조언
- 세운 분석 결과와 AI 해석 결합
- 실용적인 행동 지침 제공

#### **API 설계**
```http
POST /api/v1/saju/ai-advice
Content-Type: application/json

{
  "birth_info": {...},
  "period": "daily", // daily|weekly|monthly
  "focus": "career", // career|love|health|finance|general
  "target_date": "2025-07-29"
}
```

### 3️⃣ **AI 궁합 분석 기능**

#### **기능 설명**
- 두 사람의 사주를 종합적으로 AI 분석
- 관계 유형별 맞춤 해석 (연인, 사업, 친구)
- 구체적인 상성 개선 방안 제시

#### **API 설계**
```http
POST /api/v1/saju/ai-compatibility
Content-Type: application/json

{
  "person1": {...},
  "person2": {...},
  "relationship_type": "romantic", // romantic|business|friendship
  "focus_areas": ["personality", "communication", "goals"]
}
```

---

## 🔧 기술 구현 세부사항

### **Google Gemini API 통합 구조**

```python
# app/services/gemini_ai_interpreter.py
import google.generativeai as genai

class GeminiAIInterpreter:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.saju_analyzer = SajuAnalyzer()
        
    async def interpret_saju(self, birth_info, question, context=None):
        # 1. 기존 사주 분석 실행
        analysis_result = self.saju_analyzer.analyze_saju(birth_info)
        
        # 2. AI 프롬프트 생성
        prompt = self._create_prompt(analysis_result, question, context)
        
        # 3. OpenAI API 호출
        response = await self._call_openai(prompt)
        
        # 4. 결과 포맷팅
        return self._format_response(response, analysis_result)
    
    def _create_prompt(self, analysis, question, context):
        base_prompt = f"""
        당신은 30년 경력의 전문 명리학자입니다.
        
        사주 분석 결과:
        - 사주팔자: {analysis['palja']}
        - 오행 분석: {analysis['wuxing']}
        - 성격 분석: {analysis['personality']}
        - 십성 분석: {analysis['ten_stars']}
        
        사용자 질문: {question}
        
        전통 명리학 이론을 바탕으로 개인화된 해석을 제공하세요.
        친근하면서도 전문적인 톤으로 답변해주세요.
        """
        return base_prompt
```

### **프론트엔드 AI 채팅 인터페이스**

```typescript
// src/components/AIChatInterface.tsx
interface AIChatProps {
  birthInfo: BirthInfo;
  analysisResult: SajuAnalysis;
}

const AIChatInterface: React.FC<AIChatProps> = ({ birthInfo, analysisResult }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSendMessage = async (question: string) => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/v1/saju/ai-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ birth_info: birthInfo, question })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, 
        { type: 'user', content: question },
        { type: 'ai', content: data.data.ai_interpretation }
      ]);
    } catch (error) {
      console.error('AI 해석 요청 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="ai-chat-container">
      <ChatHistory messages={messages} />
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
};
```

---

## 📊 구현 일정

### **Week 1: 기반 구조 설정**
- [x] 계획 수립 및 문서화
- [ ] OpenAI API 키 설정
- [ ] AI 해석 서비스 기본 구조 구현
- [ ] 프롬프트 엔지니어링

### **Week 2: AI 대화형 해석 구현**
- [ ] 백엔드 AI 해석 API 구현
- [ ] 프론트엔드 채팅 인터페이스 구현
- [ ] 테스트 및 품질 검증

### **Week 3-4: 추가 기능 구현**
- [ ] AI 운세 조언 기능
- [ ] AI 궁합 분석 기능
- [ ] 성능 최적화 및 에러 핸들링

---

## 🔐 보안 및 설정

### **환경 변수 설정**
```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-4
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.7
```

### **의존성 추가**
```bash
# 백엔드
pip install openai python-dotenv

# 프론트엔드
npm install @types/react
```

---

## 📈 성공 지표

### **Phase 1 목표**
- [ ] AI 해석 응답 시간 < 3초
- [ ] 사용자 만족도 > 85%
- [ ] API 에러율 < 1%
- [ ] 일일 AI 요청 처리 > 100건

### **품질 기준**
- [ ] 명리학적 정확성 검증
- [ ] 자연스러운 한국어 응답
- [ ] 개인화된 맞춤 해석 제공

---

## 🚀 다음 단계 (Phase 2)

### **데이터 수집 및 분석**
- 사용자 질문 패턴 분석
- AI 응답 품질 피드백 수집
- 사주 해석 정확도 데이터 축적

### **특화 모델 개발**
- TensorFlow 기반 사주 전용 모델 훈련
- 로컬 추론 서버 구축
- 하이브리드 라우팅 시스템 구현

---

**🎯 목표: 전통 명리학의 정확성 + 현대 AI의 편의성 = 최고의 사주 해석 서비스**