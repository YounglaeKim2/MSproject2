# 🤖 AI 기반 예상 질문 제안 시스템 상세 설계

> 2025-08-03 작성  
> 사주 분석 결과를 바탕으로 AI가 사용자 맞춤형 질문을 자동 생성하는 시스템

## 🎯 시스템 개요

### 목적
- **사용자 참여도 향상**: 능동적인 질문 유도로 서비스 체류 시간 증가
- **AI 활용도 극대화**: Gemini AI의 컨텍스트 기반 개인화된 질문 생성
- **서비스 차별화**: 시장 유일의 AI 기반 맞춤형 질문 추천 시스템

### 핵심 기능
1. **사주 분석 기반 질문 생성**: 개인의 사주 특성을 반영한 맞춤 질문
2. **5개 카테고리 분류**: 연애, 직업, 건강, 재물, 가족 영역별 질문
3. **우선순위 시스템**: High/Medium/Low 우선순위로 질문 정렬
4. **실시간 AI 답변**: 선택한 질문에 대한 즉시 AI 상담 제공

---

## 🏗 시스템 아키텍처

### 전체 플로우
```
1. 사주 분석 완료
   ↓
2. AI 질문 생성 API 호출 (/suggested-questions)
   ↓
3. 사주 특성 분석 + AI 프롬프트 생성
   ↓
4. Gemini AI 질문 생성 + 템플릿 질문 결합
   ↓
5. 5개 추천 질문 카드 표시
   ↓
6. 질문 선택 → AI 맞춤 답변 생성 (/question-answer)
   ↓
7. 개인화된 AI 상담 결과 표시
```

### 백엔드 구조
```
SAJU/backend/app/
├── api/saju.py                        # API 엔드포인트
│   ├── POST /suggested-questions      # 질문 생성 API
│   └── POST /question-answer          # 질문 답변 API
├── services/
│   └── ai_question_generator.py       # AI 질문 생성 서비스
└── models/
    └── suggested_question.py          # 질문 모델 정의
```

---

## 📊 데이터 모델 설계

### SuggestedQuestion 클래스
```python
class SuggestedQuestion:
    def __init__(self, id: str, question: str, category: str, priority: str, ai_response: str = None):
        self.id = id                    # 질문 고유 ID
        self.question = question        # 질문 내용
        self.category = category        # 카테고리 (연애/직업/건강/재물/가족)
        self.priority = priority        # 우선순위 (high/medium/low)
        self.ai_response = ai_response  # 미리 생성된 답변 (선택사항)
```

### API 응답 형식
```json
{
  "success": true,
  "data": {
    "basic_info": {
      "name": "홍길동",
      "gender": "남성",
      "birth_date": "1990년 5월 15일 14시"
    },
    "suggested_questions": [
      {
        "id": "ai_1",
        "question": "올해 하반기 연애운이 어떨까요?",
        "category": "연애",
        "priority": "high",
        "ai_response": "연애운 분석 기반 추천 이유"
      }
    ],
    "question_count": 5,
    "generation_time": "방금 전",
    "categories": ["연애", "직업", "건강", "재물", "가족"]
  }
}
```

---

## 🤖 AI 질문 생성 알고리즘

### 1단계: 사주 특성 추출
```python
def _extract_key_features(self, saju_result: Dict[str, Any]) -> Dict[str, Any]:
    features = {}
    
    # 사주팔자 정보
    if 'saju_palja' in saju_result:
        palja = saju_result['saju_palja']
        features['palja'] = f"{palja.get('day_pillar', {}).get('stem', '')}일간"
    
    # 오행 분석 (가장 강한/약한 오행)
    if 'wuxing_analysis' in saju_result:
        wuxing = saju_result['wuxing_analysis']
        wuxing_scores = {k: v for k, v in wuxing.items() if isinstance(v, (int, float))}
        if wuxing_scores:
            features['strongest_element'] = max(wuxing_scores, key=wuxing_scores.get)
            features['weakest_element'] = min(wuxing_scores, key=wuxing_scores.get)
    
    # 성격/직업/재물 분석
    if 'interpretations' in saju_result:
        interpretations = saju_result['interpretations']
        features['personality'] = interpretations.get('personality', '')
        features['career_tendency'] = interpretations.get('career', '')
        features['wealth_tendency'] = interpretations.get('wealth', '')
    
    return features
```

### 2단계: AI 프롬프트 생성
```python
def _create_question_prompt(self, features: Dict[str, Any], user_info: Dict[str, Any]) -> str:
    name = user_info.get('name', '고객')
    gender = "남성" if user_info.get('gender', '').lower() in ['male', 'm'] else "여성"
    
    prompt = f"""당신은 30년 경력의 전문 명리학자입니다. 
다음 사주 분석 결과를 바탕으로 {name}님({gender})이 궁금해할 만한 질문 5개를 생성해주세요.

<사주 분석 특징>
- 일간: {features.get('palja', '정보 없음')}
- 가장 강한 오행: {features.get('strongest_element', '정보 없음')}
- 가장 약한 오행: {features.get('weakest_element', '정보 없음')}
- 성격 특징: {features.get('personality', '정보 없음')}
- 직업 성향: {features.get('career_tendency', '정보 없음')}
- 재물 성향: {features.get('wealth_tendency', '정보 없음')}

<질문 생성 가이드라인>
1. 각 질문은 구체적이고 개인화된 내용이어야 합니다
2. 5개 카테고리(연애, 직업, 건강, 재물, 가족)에 각각 1개씩 배치
3. 실제 상황에서 많이 하는 현실적인 질문
4. 너무 일반적이지 않고 개인의 사주 특성을 반영
5. 질문은 20자 이내로 간결하게

<응답 형식>
JSON 배열로 응답하되, 각 질문은 다음 형식:
{{
  "question": "질문 내용",
  "category": "연애|직업|건강|재물|가족",
  "priority": "high|medium|low",
  "reason": "이 질문을 추천하는 이유"
}}

반드시 5개의 질문을 생성하고, 각 카테고리별로 1개씩 배치해주세요."""

    return prompt
```

### 3단계: AI 응답 파싱
```python
def _parse_ai_response(self, ai_response: str) -> List[Dict[str, Any]]:
    try:
        # JSON 응답 파싱 시도
        if '[' in ai_response and ']' in ai_response:
            json_start = ai_response.find('[')
            json_end = ai_response.rfind(']') + 1
            json_str = ai_response[json_start:json_end]
            questions_data = json.loads(json_str)
            return questions_data
        else:
            # JSON이 아닌 경우 텍스트 파싱
            return self._parse_text_response(ai_response)
    except Exception as e:
        logger.error(f"AI 응답 파싱 실패: {e}")
        return []
```

### 4단계: 질문 결합 및 우선순위 설정
```python
def _combine_questions(self, ai_questions: List[Dict[str, Any]], saju_result: Dict[str, Any]) -> List[SuggestedQuestion]:
    suggested_questions = []
    used_categories = set()
    
    # AI 생성 질문 우선 추가
    for i, q_data in enumerate(ai_questions[:5]):
        question = SuggestedQuestion(
            id=f"ai_{i+1}",
            question=q_data.get('question', ''),
            category=q_data.get('category', '연애'),
            priority=q_data.get('priority', 'medium'),
            ai_response=q_data.get('reason', '')
        )
        suggested_questions.append(question)
        used_categories.add(q_data.get('category'))
    
    # 부족한 카테고리는 템플릿에서 추가
    categories = ["연애", "직업", "건강", "재물", "가족"]
    for category in categories:
        if category not in used_categories and len(suggested_questions) < 5:
            template_question = self._get_template_question(category, saju_result)
            if template_question:
                suggested_questions.append(template_question)
    
    return suggested_questions[:5]  # 최대 5개
```

---

## 🎨 프론트엔드 UI/UX 설계

### 질문 카드 디자인
```typescript
interface SuggestedQuestionsProps {
  sajuResult: SajuAnalysisResult;
  onQuestionSelect: (question: SuggestedQuestion) => void;
}

const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({
  sajuResult,
  onQuestionSelect
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>💬 AI가 추천하는 질문들</Text>
      {questions.map((question, index) => (
        <QuestionCard
          key={question.id}
          question={question}
          onPress={() => onQuestionSelect(question)}
          style={[
            styles.questionCard,
            { backgroundColor: getCategoryColor(question.category) }
          ]}
        />
      ))}
    </View>
  );
};
```

### 카테고리별 색상 시스템
```typescript
const getCategoryColor = (category: string): string => {
  const colors = {
    '연애': '#E91E63',  // 핑크
    '직업': '#2196F3',  // 블루
    '건강': '#4CAF50',  // 그린
    '재물': '#FF9800',  // 오렌지
    '가족': '#9C27B0'   // 퍼플
  };
  return colors[category] || '#757575';
};
```

### 우선순위별 스타일링
```typescript
const getPriorityStyle = (priority: string) => {
  return {
    high: { borderWidth: 3, borderColor: '#F44336' },      // 빨간 테두리
    medium: { borderWidth: 2, borderColor: '#FF9800' },    // 주황 테두리
    low: { borderWidth: 1, borderColor: '#9E9E9E' }        // 회색 테두리
  }[priority];
};
```

### 질문 선택 플로우
```typescript
const handleQuestionSelect = async (question: SuggestedQuestion) => {
  try {
    setIsLoading(true);
    
    // AI 답변 생성 API 호출
    const response = await sajuApi.getQuestionAnswer(birthInfo, question.question);
    
    if (response.success) {
      // AI 상담 화면으로 이동
      navigation.navigate('AIChat', {
        initialQuestion: question.question,
        aiAnswer: response.data.ai_answer,
        sajuContext: sajuResult
      });
    }
  } catch (error) {
    Alert.alert('오류', 'AI 답변 생성에 실패했습니다.');
  } finally {
    setIsLoading(false);
  }
};
```

---

## 📱 통합 플로우 설계

### 웹 서비스 통합
```typescript
// SAJU 웹 앱에서의 통합
const ProfileScreen: React.FC = () => {
  const [suggestedQuestions, setSuggestedQuestions] = useState<SuggestedQuestion[]>([]);
  
  useEffect(() => {
    if (analysisResult) {
      // 사주 분석 완료 후 자동으로 질문 생성
      generateSuggestedQuestions();
    }
  }, [analysisResult]);
  
  const generateSuggestedQuestions = async () => {
    try {
      const response = await fetch('/api/v1/saju/suggested-questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(birthInfo)
      });
      
      const data = await response.json();
      if (data.success) {
        setSuggestedQuestions(data.data.suggested_questions);
      }
    } catch (error) {
      console.error('질문 생성 실패:', error);
    }
  };
  
  return (
    <div className="profile-screen">
      {/* 기존 사주 분석 결과 */}
      <SajuAnalysisResult result={analysisResult} />
      
      {/* AI 추천 질문 섹션 */}
      {suggestedQuestions.length > 0 && (
        <SuggestedQuestionsSection 
          questions={suggestedQuestions}
          onQuestionSelect={handleQuestionSelect}
        />
      )}
    </div>
  );
};
```

### 모바일 앱 통합
```typescript
// AppService 모바일 앱에서의 통합
const ProfileScreen: React.FC = () => {
  const [showSuggestedQuestions, setShowSuggestedQuestions] = useState(false);
  
  const handleAnalysisComplete = async (result: SajuAnalysisResult) => {
    setAnalysisResult(result);
    
    // 분석 완료 후 질문 생성 제안
    Alert.alert(
      '분석 완료!',
      'AI가 추천하는 질문을 확인하시겠습니까?',
      [
        { text: '나중에', style: 'cancel' },
        { 
          text: '확인', 
          onPress: () => {
            setShowSuggestedQuestions(true);
            generateQuestions(result);
          }
        }
      ]
    );
  };
  
  return (
    <ScrollView style={styles.container}>
      {/* 기존 사주 분석 결과 */}
      <SajuAnalysisCard result={analysisResult} />
      
      {/* AI 추천 질문 모달 */}
      <Modal 
        visible={showSuggestedQuestions}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <SuggestedQuestionsModal
          questions={suggestedQuestions}
          onQuestionSelect={handleQuestionSelect}
          onClose={() => setShowSuggestedQuestions(false)}
        />
      </Modal>
    </ScrollView>
  );
};
```

---

## 🔧 백엔드 API 구현

### 질문 생성 API
```python
@router.post("/suggested-questions")
async def get_suggested_questions(birth_info: BirthInfoRequest):
    """
    AI 기반 예상 질문 생성 API
    
    Args:
        birth_info: 출생 정보 (년월일시, 성별, 이름)
    
    Returns:
        사주 분석 결과 기반 개인화된 추천 질문 리스트 (5개)
    """
    try:
        logger.info(f"AI 예상 질문 생성 요청: {birth_info.name}({birth_info.gender})")
        
        # 1. 입력 검증
        _validate_birth_info(birth_info)
        
        # 2. 사주 분석 실행 (질문 생성을 위한 컨텍스트)
        raw_result = saju_analyzer.analyze_saju(birth_info)
        analysis_result = safe_convert_to_dict(raw_result)
        saju_result = _format_for_frontend(analysis_result, birth_info)
        
        # 3. 사용자 정보 준비
        user_info = {
            "name": birth_info.name,
            "gender": birth_info.gender,
            "birth_date": f"{birth_info.year}-{birth_info.month:02d}-{birth_info.day:02d}",
            "birth_time": birth_info.hour
        }
        
        # 4. AI 질문 생성기로 추천 질문 생성
        question_generator = get_ai_question_generator()
        suggested_questions = await question_generator.generate_questions(saju_result, user_info)
        
        # 5. 응답 구성
        response_data = {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성",
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "suggested_questions": [q.to_dict() for q in suggested_questions],
                "question_count": len(suggested_questions),
                "generation_time": "방금 전",
                "categories": ["연애", "직업", "건강", "재물", "가족"]
            }
        }
        
        logger.info(f"AI 예상 질문 생성 완료: {len(suggested_questions)}개 질문")
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"AI 예상 질문 생성 오류: {e}")
        raise HTTPException(status_code=500, detail=f"AI 예상 질문 생성 실패: {str(e)}")
```

### 질문 답변 API
```python
@router.post("/question-answer")
async def get_question_answer(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="답변을 원하는 질문")
):
    """
    특정 질문에 대한 AI 맞춤 답변 생성 API
    
    Args:
        birth_info: 출생 정보 (사주 분석 컨텍스트용)
        question: 답변을 원하는 질문
    
    Returns:
        사주 분석 기반 개인화된 AI 답변
    """
    try:
        logger.info(f"AI 질문 답변 생성 요청: {question}")
        
        # 1. 사주 분석 실행 (답변 컨텍스트용)
        raw_result = saju_analyzer.analyze_saju(birth_info)
        analysis_result = safe_convert_to_dict(raw_result)
        saju_context = _format_for_frontend(analysis_result, birth_info)
        
        # 2. AI 답변 생성
        question_generator = get_ai_question_generator()
        ai_answer = await question_generator.get_question_answer(question, saju_context)
        
        # 3. 응답 구성
        response_data = {
            "success": True,
            "data": {
                "basic_info": {
                    "name": birth_info.name,
                    "gender": "남성" if birth_info.gender.lower() in ["male", "m"] else "여성",
                    "birth_date": f"{birth_info.year}년 {birth_info.month}월 {birth_info.day}일 {birth_info.hour}시"
                },
                "user_question": question,
                "ai_answer": ai_answer,
                "answer_time": "방금 전"
            }
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"AI 질문 답변 생성 오류: {e}")
        raise HTTPException(status_code=500, detail=f"AI 질문 답변 생성 실패: {str(e)}")
```

---

## 🧪 테스트 시나리오

### 기본 기능 테스트
```bash
# 1. 질문 생성 API 테스트
curl -X POST http://localhost:8000/api/v1/saju/suggested-questions \
-H "Content-Type: application/json" \
-d '{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "gender": "male",
  "name": "홍길동"
}'

# 예상 응답:
{
  "success": true,
  "data": {
    "basic_info": {
      "name": "홍길동",
      "gender": "남성",
      "birth_date": "1990년 5월 15일 14시"
    },
    "suggested_questions": [
      {
        "id": "ai_1",
        "question": "올해 하반기 연애운이 어떨까요?",
        "category": "연애",
        "priority": "high"
      },
      {
        "id": "ai_2", 
        "question": "현재 직장에서 승진 가능성은?",
        "category": "직업",
        "priority": "high"
      }
    ],
    "question_count": 5
  }
}
```

### 질문 답변 테스트
```bash
# 2. 질문 답변 API 테스트
curl -X POST "http://localhost:8000/api/v1/saju/question-answer?question=올해%20하반기%20연애운이%20어떨까요?" \
-H "Content-Type: application/json" \
-d '{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "gender": "male",
  "name": "홍길동"
}'

# 예상 응답:
{
  "success": true,
  "data": {
    "user_question": "올해 하반기 연애운이 어떨까요?",
    "ai_answer": "1990년 5월 15일 오후 2시 출생의 홍길동님, 하반기 연애운을 살펴보겠습니다...",
    "answer_time": "방금 전"
  }
}
```

### 에러 상황 테스트
```python
# 3. AI 서비스 장애 시 fallback 질문 제공 테스트
def test_ai_fallback_questions():
    # AI 서비스가 응답하지 않을 때
    # 미리 정의된 템플릿 질문들이 반환되는지 확인
    
    fallback_questions = [
        "올해 하반기 연애운이 어떨까요?",
        "현재 직장에서 승진 가능성은?", 
        "건강 관리에서 주의할 점은?",
        "투자하기 좋은 시기는 언제인가요?",
        "가족과의 관계 개선 방법은?"
    ]
    
    assert len(response['data']['suggested_questions']) == 5
    assert all(q['category'] in ['연애', '직업', '건강', '재물', '가족'] 
               for q in response['data']['suggested_questions'])
```

---

## 📊 성능 및 비용 분석

### AI API 호출 최적화
```python
class AIQuestionGenerator:
    def __init__(self):
        # 캐싱 시스템 구현
        self.question_cache = {}
        self.cache_ttl = 3600  # 1시간 캐시
        
    async def generate_questions(self, saju_result: Dict[str, Any], user_info: Dict[str, Any]):
        # 사주 특성 기반 캐시 키 생성
        cache_key = self._generate_cache_key(saju_result, user_info)
        
        # 캐시 확인
        if cache_key in self.question_cache:
            cached_data = self.question_cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_ttl:
                return cached_data['questions']
        
        # AI 질문 생성 (캐시 미스 시에만)
        questions = await self._generate_ai_questions(saju_result, user_info)
        
        # 캐시 저장
        self.question_cache[cache_key] = {
            'questions': questions,
            'timestamp': time.time()
        }
        
        return questions
```

### 비용 예상 (Gemini AI)
```
월 예상 사용량:
- 사용자당 질문 생성: 1회
- 사용자당 질문 답변: 평균 3회
- 월 활성 사용자: 1,000명

총 AI 호출:
- 질문 생성: 1,000회 × 1회 = 1,000회
- 질문 답변: 1,000회 × 3회 = 3,000회
- 총 4,000회/월

Gemini AI 비용:
- 프롬프트 토큰: 평균 500토큰/호출
- 응답 토큰: 평균 300토큰/호출
- 총 800토큰/호출 × 4,000회 = 3,200,000토큰/월
- 예상 비용: $8-12/월 (Gemini 2.5-flash 기준)
```

---

## 🚀 배포 및 운영 계획

### 단계별 배포
```
Phase 1: 백엔드 API 개발 (3시간)
├── AI 질문 생성 서비스 구현
├── API 엔드포인트 추가
└── 기본 테스트 완료

Phase 2: 웹 프론트엔드 통합 (2시간)
├── 질문 카드 컴포넌트 개발
├── ProfileScreen 통합
└── AI 상담 연동

Phase 3: 모바일 앱 통합 (2시간)
├── 모바일 UI 컴포넌트 개발
├── AppService 통합
└── 전체 플로우 테스트

Phase 4: 최적화 및 배포 (1시간)
├── 성능 최적화
├── 캐싱 시스템 적용
└── 프로덕션 배포
```

### 모니터링 지표
```python
# 운영 모니터링 대시보드
class QuestionSystemMetrics:
    def track_question_generation(self, user_id: str, questions_count: int):
        # 질문 생성 횟수 추적
        pass
        
    def track_question_selection(self, user_id: str, question_category: str):
        # 질문 선택 패턴 분석
        pass
        
    def track_ai_response_time(self, response_time: float):
        # AI 응답 시간 모니터링
        pass
        
    def track_user_satisfaction(self, user_id: str, rating: int):
        # 사용자 만족도 추적
        pass

# 주요 KPI
- 질문 생성 성공률: 목표 95%+
- 평균 AI 응답 시간: 목표 3초 이내
- 질문 선택률: 목표 70%+ (생성된 질문 중 선택 비율)
- 사용자 만족도: 목표 4.5/5.0+
```

---

## 🎊 예상 비즈니스 효과

### 사용자 경험 개선
- **체류 시간 증가**: 평균 3-5분 → 8-12분 예상
- **재방문율 향상**: 기존 30% → 50%+ 목표
- **사용자 참여도**: 수동적 → 능동적 참여 전환

### 서비스 차별화
- **시장 유일성**: AI 기반 맞춤 질문 추천 시스템
- **전문성 강화**: 사주 특성 반영한 개인화된 상담
- **기술적 우위**: Gemini AI + 전통 명리학 융합

### 매출 기여도
- **프리미엄 전환**: AI 질문 기능으로 유료 전환 유도
- **추가 상담 수요**: 질문별 심화 상담 서비스 확장
- **데이터 수집**: 사용자 관심사 패턴 분석으로 서비스 개선

---

## 📝 구현 체크리스트

### 백엔드 개발
- [ ] AIQuestionGenerator 클래스 구현
- [ ] /suggested-questions API 엔드포인트 추가
- [ ] /question-answer API 엔드포인트 추가  
- [ ] Gemini AI 프롬프트 최적화
- [ ] 에러 처리 및 fallback 로직 구현
- [ ] API 문서 업데이트

### 프론트엔드 개발
- [ ] SuggestedQuestions 컴포넌트 (웹)
- [ ] QuestionCard 컴포넌트 (웹/모바일)
- [ ] ProfileScreen 질문 섹션 통합 (웹)
- [ ] SuggestedQuestionsModal (모바일)
- [ ] AI 상담 연동 플로우
- [ ] 카테고리별 색상 시스템 적용

### 테스트 및 검증
- [ ] API 단위 테스트 작성
- [ ] 질문 생성 품질 검증
- [ ] AI 응답 정확성 테스트
- [ ] 사용자 시나리오 테스트
- [ ] 성능 및 속도 최적화
- [ ] 크로스 플랫폼 호환성 확인

### 배포 및 운영
- [ ] 프로덕션 환경 설정
- [ ] 모니터링 대시보드 구축
- [ ] 사용량 추적 시스템
- [ ] 사용자 피드백 수집 체계
- [ ] A/B 테스트 시스템 구축

---

**🏆 AI 기반 예상 질문 제안 시스템으로 사주 분석 서비스의 차별화와 사용자 경험 혁신을 달성할 수 있습니다!**

**이 시스템이 구현되면 사용자는 단순히 결과를 보는 것이 아니라, AI와 능동적으로 소통하며 깊이 있는 사주 상담을 받을 수 있게 됩니다.** ✨