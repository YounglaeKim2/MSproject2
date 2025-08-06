# 🤖 AI 기반 예상 질문 제안 시스템 구현 계획서

> **프로젝트**: MSProject2 SAJU 서비스 - AI 개인화 기능 확장  
> **날짜**: 2025-08-05  
> **목표**: 사주 분석 결과 기반 맞춤형 질문 자동 생성 시스템 구현

---

## 🎯 구현 가능성 분석

### ✅ **매우 높은 가능성 (95%)**

**기존 인프라 활용 가능:**
- ✅ Google Gemini 2.5-Flash API 이미 구축
- ✅ AI 해석 시스템 (`gemini_ai_interpreter.py`) 완성
- ✅ 사주 분석 데이터 구조 완벽 정의
- ✅ 프론트엔드 AI 채팅 인터페이스 존재
- ✅ 사용량 추적 시스템 구현됨

**필요한 작업은 단순 확장:**
1. 새로운 API 엔드포인트 1개 추가
2. 질문 생성 프롬프트 작성
3. 프론트엔드 UI 약간 수정

---

## 🏗️ 기술 아키텍처

### **현재 AI 시스템 구조**
```
사용자 → AIChatInterface → /ai-chat API → GeminiAIInterpreter → Gemini API
```

### **확장된 시스템 구조**
```
사주 분석 완료 → /suggested-questions API → GeminiAIInterpreter → 개인화된 질문 5개 생성
사용자 질문 선택 → 기존 /ai-chat API → 답변 생성
```

---

## 📋 단계별 구현 계획

### **Phase 1: 백엔드 API 구현 (30분)**

#### 1.1 새로운 API 엔드포인트 추가
**파일**: `SAJU/backend/app/api/saju.py`

```python
@router.post("/suggested-questions")
async def generate_suggested_questions(birth_info: BirthInfoRequest):
    """사주 분석 결과 기반 개인화된 예상 질문 생성"""
    try:
        # 1. 사주 분석 (기존 로직 재사용)
        raw_result = saju_analyzer.analyze_saju(birth_info)
        
        # 2. AI로 맞춤 질문 생성
        gemini = get_gemini_interpreter()
        questions_result = await gemini.generate_suggested_questions(raw_result, birth_info)
        
        return JSONResponse({
            "success": True,
            "data": {
                "suggested_questions": questions_result["questions"],
                "usage_status": questions_result.get("usage_status"),
                "timestamp": questions_result.get("timestamp")
            }
        })
        
    except Exception as e:
        logger.error(f"질문 생성 실패: {e}")
        # 폴백: 기본 질문들 반환
        return JSONResponse({
            "success": True,
            "data": {
                "suggested_questions": get_fallback_questions(),
                "fallback": True
            }
        })
```

#### 1.2 Gemini AI 인터프리터 확장
**파일**: `SAJU/backend/app/services/gemini_ai_interpreter.py`

```python
async def generate_suggested_questions(self, saju_result: Dict[str, Any], birth_info: Dict[str, Any]) -> Dict[str, Any]:
    """사주 분석 결과 기반 개인화된 질문 생성"""
    try:
        # 사용량 체크
        if not self.usage_tracker.check_and_update_usage():
            return {"questions": get_fallback_questions(), "fallback": True}
        
        # 질문 생성 프롬프트
        prompt = self._create_question_generation_prompt(saju_result, birth_info)
        
        # Gemini API 호출
        response = await self._call_gemini_async(prompt)
        
        # JSON 파싱 및 검증
        questions = self._parse_and_validate_questions(response)
        
        return {
            "questions": questions,
            "usage_status": self.usage_tracker.get_usage_status(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"질문 생성 실패: {e}")
        return {"questions": get_fallback_questions(), "fallback": True}

def _create_question_generation_prompt(self, saju_result: Dict[str, Any], birth_info: Dict[str, Any]) -> str:
    """질문 생성용 프롬프트 작성"""
    
    # 주요 분석 결과 추출
    palja = saju_result.get('palja', {})
    wuxing = saju_result.get('wuxing', {})
    personality = saju_result.get('personality', {})
    
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

<질문 생성 가이드라인>
1. 개인의 사주 특성을 반영한 구체적 질문
2. 실용적이고 현실적인 관심사
3. 5개 카테고리 균형: 연애/직업/건강/재물/인간관계
4. 친근하고 자연스러운 말투
5. 각 질문은 20-30자 내외

다음 JSON 형식으로만 응답:
{{
  "questions": [
    {{"question": "올해 하반기 연애운이 어떨까요?", "category": "연애", "priority": "high", "icon": "💕"}},
    {{"question": "현재 직장에서 승진 가능성은?", "category": "직업", "priority": "high", "icon": "💼"}},
    {{"question": "건강 관리에서 주의할 점은?", "category": "건강", "priority": "medium", "icon": "🏥"}},
    {{"question": "투자하기 좋은 시기는 언제?", "category": "재물", "priority": "medium", "icon": "💰"}},
    {{"question": "인간관계 개선 방법은?", "category": "인간관계", "priority": "low", "icon": "👥"}}
  ]
}}"""

def _parse_and_validate_questions(self, response: str) -> List[Dict[str, str]]:
    """AI 응답에서 질문 파싱 및 검증"""
    try:
        import json
        data = json.loads(response)
        questions = data.get("questions", [])
        
        # 검증: 5개 질문, 필수 필드 존재
        if len(questions) != 5:
            raise ValueError("질문 개수가 5개가 아님")
            
        for q in questions:
            if not all(k in q for k in ["question", "category", "priority", "icon"]):
                raise ValueError("필수 필드 누락")
                
        return questions
        
    except Exception as e:
        logger.error(f"질문 파싱 실패: {e}")
        return get_fallback_questions()

def get_fallback_questions() -> List[Dict[str, str]]:
    """AI 실패 시 기본 질문들"""
    return [
        {"question": "내 성격의 장단점은 무엇인가요?", "category": "성격", "priority": "high", "icon": "🤔"},
        {"question": "올해 전체 운세는 어떤가요?", "category": "운세", "priority": "high", "icon": "🔮"},
        {"question": "직업운에 대해 알려주세요", "category": "직업", "priority": "medium", "icon": "💼"},
        {"question": "연애운은 어떤가요?", "category": "연애", "priority": "medium", "icon": "💕"},
        {"question": "건강 관리 포인트는?", "category": "건강", "priority": "low", "icon": "🏥"}
    ]
```

---

### **Phase 2: 프론트엔드 UI 수정 (45분)**

#### 2.1 AIChatInterface 컴포넌트 수정
**파일**: `SAJU/frontend/src/components/AIChatInterface.tsx`

```typescript
// 새로운 타입 정의
interface SuggestedQuestion {
  question: string;
  category: string;
  priority: 'high' | 'medium' | 'low';
  icon: string;
}

// 컴포넌트 props에 추가
interface AIChatProps {
  birthInfo: BirthInfo;
  isVisible: boolean;
  onClose: () => void;
  sajuAnalysisResult?: any; // 새로 추가
}

// 상태 추가
const [suggestedQuestions, setSuggestedQuestions] = useState<SuggestedQuestion[]>([]);
const [isLoadingQuestions, setIsLoadingQuestions] = useState(false);

// 개인화된 질문 생성 함수
const generateSuggestedQuestions = async () => {
  if (!sajuAnalysisResult) return;
  
  setIsLoadingQuestions(true);
  try {
    const response = await fetch('http://localhost:8000/api/v1/saju/suggested-questions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(birthInfo)
    });
    
    const data = await response.json();
    if (data.success) {
      setSuggestedQuestions(data.data.suggested_questions);
    }
  } catch (error) {
    console.error('개인화된 질문 생성 실패:', error);
    // 폴백: 기본 질문 사용
    setSuggestedQuestions(getDefaultQuestions());
  } finally {
    setIsLoadingQuestions(false);
  }
};

// 채팅 창 열릴 때 질문 생성
useEffect(() => {
  if (isVisible && sajuAnalysisResult) {
    generateSuggestedQuestions();
  }
}, [isVisible, sajuAnalysisResult]);
```

#### 2.2 개선된 질문 버튼 UI
```typescript
// 카테고리별 색상 매핑
const getCategoryColor = (category: string) => {
  const colors = {
    '연애': '#ff6b9d',
    '직업': '#4dabf7', 
    '건강': '#51cf66',
    '재물': '#ffd43b',
    '인간관계': '#9775fa',
    '성격': '#ff8787',
    '운세': '#845ef7'
  };
  return colors[category] || '#6c757d';
};

// 개선된 퀵 버튼 렌더링
<QuickButtons>
  {isLoadingQuestions ? (
    <LoadingQuestions>🤖 맞춤 질문을 생성하는 중...</LoadingQuestions>
  ) : (
    suggestedQuestions.map((q, index) => (
      <PersonalizedQuickButton
        key={index}
        onClick={() => handleQuickQuestion(q.question)}
        disabled={isLoading}
        category={q.category}
        priority={q.priority}
      >
        <QuestionIcon>{q.icon}</QuestionIcon>
        <QuestionText>{q.question}</QuestionText>
        <CategoryBadge category={q.category}>
          {q.category}
        </CategoryBadge>
      </PersonalizedQuickButton>
    ))
  )}
</QuickButtons>
```

---

### **Phase 3: 통합 및 테스트 (15분)**

#### 3.1 메인 App 컴포넌트 수정
**파일**: `SAJU/frontend/src/App.tsx`

```typescript
// AI 채팅 호출 시 분석 결과 전달
<AIChatInterface
  birthInfo={birthInfo}
  isVisible={showAIChat}
  onClose={() => setShowAIChat(false)}
  sajuAnalysisResult={analysisResult} // 새로 추가
/>
```

#### 3.2 에러 처리 및 폴백 시스템
- AI API 실패 시 기본 질문으로 폴백
- 네트워크 오류 시 사용자 친화적 메시지
- 로딩 상태 표시

---

## 🧪 테스트 계획

### **1. 백엔드 API 테스트**
```bash
# 질문 생성 API 테스트
curl -X POST http://localhost:8000/api/v1/saju/suggested-questions \
-H "Content-Type: application/json" \
-d '{"year":1990, "month":5, "day":15, "hour":14, "gender":"male", "name":"홍길동"}'
```

### **2. 프론트엔드 통합 테스트**
- 사주 분석 후 자동 질문 생성 확인
- 개인화된 질문 클릭 시 AI 답변 확인
- 다양한 사주 케이스별 질문 품질 검증

### **3. 성능 테스트**
- 질문 생성 응답 시간 < 3초
- AI 사용량 추적 정확성
- 동시 사용자 처리 능력

---

## ⏰ 예상 개발 시간

| 단계 | 작업 내용 | 예상 시간 |
|------|-----------|-----------|
| Phase 1 | 백엔드 API 구현 | 30분 |
| Phase 2 | 프론트엔드 UI 수정 | 45분 |
| Phase 3 | 통합 및 테스트 | 15분 |
| **총계** | **전체 구현** | **90분** |

---

## 🎯 기대 효과

### **Before (현재)**
- 모든 사용자가 동일한 6개 고정 질문
- 개인화 없음, 단조로운 경험

### **After (개인화 시스템)**
- 각 사용자마다 다른 5개 맞춤 질문
- 사주 특성을 반영한 구체적 질문
- 카테고리별 색상 구분으로 시각적 개선

### **예시 개인화 질문**
```
갑목이 강한 사용자:
"올해 창업에 적합한 시기는 언제일까요? 🌱"

정관이 나타나는 사용자:
"승진이나 취업에 유리한 달은? 💼"

화가 부족한 사용자:
"인간관계 개선을 위한 조언은? 🤝"
```

---

## 🚨 위험 요소 및 대응책

### **1. AI API 실패**
- **대응**: 폴백 질문 시스템 구축
- **모니터링**: 에러율 추적

### **2. 질문 품질 문제**
- **대응**: 프롬프트 엔지니어링 최적화
- **검증**: 다양한 테스트 케이스 확인

### **3. 성능 이슈**
- **대응**: 캐싱 시스템 도입 고려
- **최적화**: API 호출 횟수 최소화

---

## 📊 성공 지표

### **정량적 지표**
- 사용자 체류 시간 20% 증가
- AI 채팅 사용률 30% 향상
- 질문 생성 성공률 95% 이상

### **정성적 지표**
- 사용자 만족도 조사
- 질문 품질 평가
- 개인화 정확도 검증

---

## 🎊 결론

**이 시스템은 매우 현실적이고 구현 가능한 프로젝트입니다.**

기존 인프라를 최대한 활용하여 **최소한의 개발로 최대 효과**를 낼 수 있으며, 사용자 경험을 크게 향상시킬 것으로 예상됩니다.

**개발 시작을 권장합니다!** 🚀