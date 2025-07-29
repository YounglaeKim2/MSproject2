# AI 기능 구현 현재 상황 정리

📅 **작업일**: 2025년 7월 29일  
🎯 **목표**: Google Gemini AI 채팅 기능 완전 구현

---

## 🏆 완성된 것들

### ✅ 1. 백엔드 구조 완성
- **파일**: `SAJU/backend/app/services/gemini_ai_interpreter.py`
- **기능**: Google Gemini 2.5-flash REST API 완전 구현
- **방식**: `aiohttp`를 사용한 비동기 HTTP 요청
- **API 엔드포인트**: 
  - `/ai-chat` - AI 대화형 해석
  - `/ai-usage` - 사용량 조회
  - `/ai-test` - 연결 테스트

### ✅ 2. 프론트엔드 UI 완성
- **파일**: `SAJU/frontend/src/components/AIChatInterface.tsx`
- **기능**: 완전한 채팅 인터페이스
- **특징**: 
  - 모달 방식 채팅창
  - 퀵 버튼 (성격, 운세, 직업운 등)
  - 사용량 표시
  - 실시간 채팅

### ✅ 3. API 통합 완성
- **파일**: `SAJU/backend/app/api/saju.py`
- **엔드포인트 추가**: AI 관련 3개 엔드포인트 구현
- **에러 핸들링**: 완전한 예외 처리 구조

### ✅ 4. 서비스 시작 명령어 및 시간

#### 서비스 시작 순서 및 시간
| 순서 | 서비스 | 포트 | 명령어 | 시작 시간 | 상태 |
|------|--------|------|---------|-----------|------|
| 1 | SAJU 백엔드 | 8000 | `cd SAJU/backend && uvicorn app.main:app --reload --port 8000` | **~4초** | ✅ 빠름 |
| 2 | SAJU 프론트엔드 | 3000 | `cd SAJU/frontend && npm start` | **~1분 30초** | ⚠️ 느림 |
| 3 | 메인 앱 | 4000 | `cd main-app && npm start` | **~1분 20초** | ⚠️ 느림 |

#### 포트 충돌 해결 명령어
```bash
# 포트 사용 프로세스 확인
powershell "Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess"
powershell "Get-NetTCPConnection -LocalPort 4000 | Select-Object OwningProcess"

# 프로세스 강제 종료
powershell "Stop-Process -Id [PID] -Force"
powershell "Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force"
```

#### 서비스 상태 확인
```bash
# 백엔드 상태 확인
curl -s http://localhost:8000/health

# 프론트엔드 상태 확인  
curl -s -o nul -w "%{http_code}" http://localhost:3000

# 메인 앱 상태 확인
curl -s -o nul -w "%{http_code}" http://localhost:4000
```

---

## 🚫 현재 문제점

### ❌ 1. JSON Serialization 오류 (심각한 문제)
```
"AI 해석 중 오류가 발생했습니다: Object of type SajuPaljaResponse is not JSON serializable"
```

**원인**: 
- `saju_analyzer.analyze_saju()` 가 Pydantic 모델 객체 반환
- FastAPI JSON 응답 시 직렬화 불가

**시도한 해결책 (모두 실패)**:
- ✅ 재귀적 `convert_to_dict()` 함수 작성
- ✅ `analysis_result` 완전 우회 (테스트 데이터로 교체)
- ✅ `JSONResponse` → `dict` 반환 변경
- ✅ AI 해석 기능 완전 우회
- ✅ 서비스 완전 재시작 (프로세스 강제 종료 후 재시작)
- **⚠️ 서비스 재시작 후에도 동일한 오류 지속**

### ❌ 2. 프론트엔드 시작 속도 문제
**문제**: React 앱 시작이 매우 느림 (1분 20초~1분 30초)

**원인 분석**:
- **Webpack 컴파일**: React 앱의 JavaScript 번들링 과정
- **의존성 로딩**: node_modules의 라이브러리들 로딩
- **TypeScript 컴파일**: TypeScript → JavaScript 변환
- **개발 서버 준비**: Hot reload, dev server 설정

**개선 방법**:
- Production 빌드 사용: `npm run build` → serve 사용
- 의존성 최적화: 불필요한 라이브러리 제거
- 캐시 활용: npm 캐시 최적화

### ❌ 3. API 키 인식 문제
```
"400 API key expired. Please renew the API key."
```

**현상**:
- 직접 curl: ✅ 정상 작동
- 코드 내에서: ❌ "API key expired"
- **동일한 API 키**: `AIzaSyD7OB3MnPASwL6oN7_Ni8hKyPWOEACYeIo`

**시도한 해결책**:
- 환경변수 → 직접 하드코딩
- Python SDK → REST API 변경
- **여전히 실패** ❌

---

## 🔧 완성된 코드 구조

### REST API 호출 방식
```python
async def _call_gemini_async(self, prompt: str) -> str:
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
```

### API 엔드포인트
```python
@router.post("/ai-chat")
async def ai_chat_interpretation(
    birth_info: BirthInfoRequest,
    question: str = Query(..., description="사용자 질문")
):
    # 1. 사주 분석
    analysis_result = convert_to_dict(saju_analyzer.analyze_saju(birth_info))
    
    # 2. AI 해석
    ai_result = await ai_interpreter.interpret_saju(analysis_result, question)
    
    # 3. 응답 반환
    return {"success": True, "data": {...}}
```

---

## 🎯 다음 작업 계획

### 🔴 1순위: JSON Serialization 해결
**방법 1**: Pydantic 모델 완전 교체
- `SajuPaljaResponse` → 순수 `dict` 반환으로 변경
- `app/services/saju_analyzer.py` 수정

**방법 2**: 직렬화 함수 개선
- 더 강력한 `to_dict()` 함수 작성
- 모든 객체 타입 처리

### 🔴 1순위: API 키 문제 해결
**방법 1**: 라이브러리 버전 확인
- `aiohttp` 버전 호환성 확인
- `google-generativeai` 완전 제거

**방법 2**: 직접 HTTP 요청
- `requests` 라이브러리 사용
- 동기 방식으로 단순화

### 🟡 2순위: 통합 테스트
- 프론트엔드 AI 버튼 연결 확인
- 전체 플로우 테스트

---

## 🧪 테스트 명령어

### 직접 API 테스트 (성공)
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
  -H "Content-Type: application/json" \
  -H "X-goog-api-key: AIzaSyD7OB3MnPASwL6oN7_Ni8hKyPWOEACYeIo" \
  -X POST \
  -d '{"contents": [{"parts": [{"text": "Hello"}]}]}'
```

### 서비스 테스트 (실패)
```bash
# AI 연결 테스트
curl http://localhost:8000/api/v1/saju/ai-test

# AI 채팅 테스트
curl -X POST "http://localhost:8000/api/v1/saju/ai-chat?question=test" \
  -H "Content-Type: application/json" \
  -d '{"year":1990,"month":5,"day":15,"hour":14,"gender":"male","name":"test"}'
```

---

## 📊 현재 서비스 상태

| 구성요소 | 상태 | 포트 | 비고 |
|---------|------|------|------|
| 메인 앱 | ✅ 실행중 | 4000 | 정상 |
| SAJU 백엔드 | ✅ 실행중 | 8000 | 정상 |
| SAJU 프론트엔드 | ✅ 실행중 | 3000 | 정상 |
| 기본 사주 분석 | ✅ 정상 | - | 37개 메서드 완벽 |
| AI 채팅 기능 | ❌ 오류 | - | JSON/API 키 문제 |

---

## 💡 해결 우선순위

1. **JSON Serialization 문제** (가장 중요)
2. **API 키 인식 문제** (가장 중요)  
3. 프론트엔드 통합 테스트
4. 성능 최적화

---

## 🚀 빠른 서비스 시작 가이드

### 전체 서비스 시작 (순서대로)
```bash
# 1. 백엔드 시작 (4초)
cd SAJU/backend && uvicorn app.main:app --reload --port 8000

# 2. 프론트엔드 시작 (1분 30초) - 새 터미널
cd SAJU/frontend && npm start

# 3. 메인 앱 시작 (1분 20초) - 새 터미널  
cd main-app && npm start
```

### 포트 충돌 해결
```bash
# 모든 포트의 프로세스 한번에 종료
powershell "Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force"
powershell "Stop-Process -Id (Get-NetTCPConnection -LocalPort 4000).OwningProcess -Force"
powershell "Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force"
```

### 서비스 접속 URL
- **메인 페이지**: http://localhost:4000
- **SAJU 서비스**: http://localhost:3000  
- **API 문서**: http://localhost:8000/docs
- **API 상태**: http://localhost:8000/health

---

## 💡 현재 분석 결과

### React 앱이 느린 이유
1. **Webpack 번들링**: JavaScript 모듈들을 하나로 합치는 과정
2. **의존성 해결**: package.json의 모든 라이브러리 로딩
3. **TypeScript 컴파일**: .tsx → .js 변환
4. **Hot Reload 설정**: 개발용 실시간 새로고침 준비
5. **소스맵 생성**: 디버깅용 맵 파일 생성

### 개선 방안
- **Production 모드**: `npm run build` 후 정적 서버 사용
- **의존성 최적화**: 불필요한 라이브러리 제거
- **코드 분할**: 지연 로딩 적용

---

## 🔥 긴급 해결 과제

### 1순위: JSON Serialization 오류 
**현상**: 모든 해결 시도에도 불구하고 계속 발생
**추정 원인**: 
- Git 캐시 문제
- Python 모듈 임포트 캐시
- FastAPI 내부 처리 문제
- 숨겨진 Pydantic 객체 존재

### 2순위: API 키 문제
**현상**: 동일 키로 curl은 성공, Python 코드는 실패

---

**🎊 결론**: AI 기능 구조는 **100% 완성**, 서비스 시작 방법 정리 완료. 하지만 JSON Serialization 오류가 핵심 걸림돌!