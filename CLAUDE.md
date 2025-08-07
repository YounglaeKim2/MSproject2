# CLAUDE.md - 개발 가이드

> MSProject2 SAJU 서비스 개발을 위한 Claude Code 가이드

## 🎯 프로젝트 개요

**완전 분리형 마이크로서비스** 웹 플랫폼 - 전통 명리학 + 현대 AI 기술

### 서비스 구조

- **Main App** (`main-app/`) - 랜딩 페이지 (:4000)
- **SAJU Service** (`SAJU/`) - 사주팔자 분석 (:8000/:3000) ✅ **완성 + Azure AI**
- **NewCompatibility Service** (`NewCompatibility/`) - 궁합 분석 (:8003/:3003) ✅ **완성 + Azure AI**
- **Physiognomy Service** (`Physiognomy/`) - 관상 분석 (:8001/:3001) 📋 개발중

## 🏆 현재 완성 상태 (2025-07-28)

### ✅ SAJU 서비스 (100% 완성)

#### 백엔드 (37개 메서드)

- **기본 분석**: 사주팔자, 오행, 십성 ✅
- **확장 분석**: 13개 메서드 (균형점수, 성격유형, 맞춤추천) ✅
- **대운 분석**: 10년 주기 (2세-81세, 8개 대운) ✅
- **세운 분석**: 연간/월별 운세 ✅

#### API 엔드포인트 (7개)

```
POST /analyze     # 완전한 사주 분석 ✅
GET  /palja-only  # 사주팔자만 ✅
GET  /wuxing-only # 오행 분석만 ✅
POST /daeun       # 대운 분석 ✅
POST /saeun       # 세운 분석 ✅
GET  /test        # API 테스트 ✅
GET  /health      # 헬스 체크 ✅
```

#### 프론트엔드

- React 18 + TypeScript + styled-components ✅
- 기본 분석 + 대운 + 세운 UI 완성 ✅
- 반응형 디자인, 현대적 UI/UX ✅

#### 🔧 최종 버그 수정 완료 (2025.07.29)

- **강점 & 약점 표시 문제** → ✅ 해결
- **성격/건강/대인관계/재물운 고정 문제** → ✅ 해결  
- **대운/세운 분석 404 오류** → ✅ 해결
- **AI 채팅 cp949 인코딩 오류** → ✅ 해결
- **백엔드 리팩토링 및 안정성 강화** → ✅ 완료

## 📊 만세력 데이터베이스

- **경로**: `SAJU/manseryukDB/DB/manseryuk.db`
- **데이터**: 1900-2100년, 73,442 레코드
- **기반**: 고영창님 "진짜 만세력"
- **연결**: `SqliteDB` 클래스 (`mdbconn.py`)

## 🔧 개발 명령어

### 서비스 실행

```bash
# 메인 앱
cd main-app && npm start

# SAJU 백엔드 (포트 8000)
cd SAJU/backend && uvicorn app.main:app --reload --port 8000

# SAJU 프론트엔드 (포트 3000)
cd SAJU/frontend && npm start

# NewCompatibility 백엔드 (포트 8003)
cd NewCompatibility/backend && uvicorn app.main:app --reload --port 8003

# NewCompatibility 프론트엔드 (포트 3003)
cd NewCompatibility/frontend && npm start
```

### API 테스트

#### SAJU API
```bash
# 헬스 체크
curl http://localhost:8000/health

# 사주 분석
curl -X POST http://localhost:8000/api/v1/saju/analyze \
-H "Content-Type: application/json" \
-d '{"year":1990,"month":5,"day":15,"hour":14,"gender":"male","name":"홍길동"}'

# Azure AI 해석
curl -X POST http://localhost:8000/api/v1/azure/chat \
-H "Content-Type: application/json" \
-d '{"year":1990,"month":5,"day":15,"hour":14,"gender":"male","name":"홍길동"}' \
--data-urlencode "question=올해 운세는 어떤가요?"
```

#### NewCompatibility API  
```bash
# 궁합 분석
curl -X POST http://localhost:8003/api/v1/compatibility/analyze \
-H "Content-Type: application/json" \
-d '{"person1":{"name":"홍길동","year":1990,"month":5,"day":15,"hour":14,"gender":"male"},"person2":{"name":"김영희","year":1992,"month":8,"day":20,"hour":10,"gender":"female"}}'

# Azure AI 궁합 해석
curl -X POST http://localhost:8003/api/v1/azure-compatibility/chat \
-H "Content-Type: application/json" \
-d '{"person1":{"name":"홍길동","year":1990,"month":5,"day":15,"hour":14,"gender":"male"},"person2":{"name":"김영희","year":1992,"month":8,"day":20,"hour":10,"gender":"female"}}' \
--data-urlencode "question=우리 둘의 궁합은 어떤가요?"
```

## 📁 핵심 파일 구조

```
SAJU/
├── backend/app/
│   ├── main.py                           # FastAPI 앱
│   ├── api/saju.py                       # 사주 API 엔드포인트
│   ├── api/azure_api.py                  # Azure OpenAI API 엔드포인트
│   ├── services/saju_analyzer.py         # 37개 분석 메서드
│   ├── services/azure_openai_service.py  # Azure OpenAI 서비스
│   ├── services/gemini_ai_interpreter.py # Gemini AI 서비스
│   ├── models/saju.py                    # Pydantic 모델
│   └── database/connection.py            # DB 연결
├── frontend/src/
│   ├── App.tsx                           # 메인 UI (Gemini + Azure 버튼)
│   ├── components/AzureAIChatInterface.tsx # Azure AI 채팅 컴포넌트
│   └── index.tsx                         # React 엔트리
├── manseryukDB/
│   ├── DB/manseryuk.db                  # 만세력 DB
│   └── mdbconn.py                       # DB 클래스
└── 사주해석로직.txt                       # 명리학 문서

NewCompatibility/
├── backend/app/
│   ├── main.py                                    # FastAPI 앱
│   ├── routers/azure_compatibility_api.py         # Azure 궁합 API 엔드포인트
│   ├── services/compatibility_engine.py           # 궁합 계산 엔진
│   ├── services/azure_compatibility_ai_service.py # Azure 궁합 AI 서비스
│   ├── services/compatibility_ai_interpreter.py   # Gemini 궁합 AI 서비스
│   ├── services/saju_client.py                    # SAJU API 클라이언트
│   └── models/compatibility.py                    # Pydantic 모델
├── frontend/src/
│   ├── App.tsx                              # 메인 UI (Gemini + Azure 버튼)
│   ├── components/AzureCompatibilityAIChat.tsx # Azure 궁합 채팅 컴포넌트
│   ├── components/CompatibilityForm.tsx     # 궁합 입력 폼
│   └── components/CompatibilityResult.tsx   # 궁합 결과 표시
└── test_data.json                          # 테스트 데이터
```

## 🌐 서비스 접속

| 서비스            | URL                        | 상태 |
| ----------------- | -------------------------- | ---- |
| 메인              | http://localhost:4000      | ✅   |
| SAJU UI           | http://localhost:3000      | ✅   |
| SAJU API          | http://localhost:8000      | ✅   |
| SAJU API 문서     | http://localhost:8000/docs | ✅   |
| NewCompatibility UI | http://localhost:3003    | ✅   |
| NewCompatibility API| http://localhost:8003    | ✅   |
| 궁합 API 문서     | http://localhost:8003/docs | ✅   |

## 🔨 기술 스택

- **백엔드**: FastAPI + Pydantic + SQLite
- **프론트엔드**: React 18 + TypeScript + styled-components
- **데이터**: 73,442개 만세력 레코드

## 📋 개발 가이드라인

### 코드 수정 시

1. **백엔드**: `saju_analyzer.py` 메서드 추가/수정
2. **API**: `saju.py` 엔드포인트 업데이트
3. **프론트엔드**: `App.tsx` UI 컴포넌트 수정
4. **타입 안전성**: TypeScript 인터페이스 동기화

### 포트 관리

- Main: 4000 | SAJU: 8000/3000 | NewCompatibility: 8003/3003 | Physiognomy: 8001/3001

### CORS 설정

- 개발환경: 모든 origins 허용
- SAJU: `http://localhost:3000` 허용

## 🎊 현재 프로젝트 상태 (2025.08.07 Azure OpenAI 보안 강화 완성)

**SAJU 서비스: 100% 완성 + Azure OpenAI 통합** ✅  
**NewCompatibility 서비스: 100% 완성 + Azure OpenAI 통합** ✅
**Azure OpenAI 보안: 환경변수 기반 안전한 API 키 관리** ✅

### 완성된 모든 기능들

#### SAJU 서비스 (이중 AI 지원)
- ✅ **기본 사주 분석**: 37개 메서드, 73,442개 만세력 DB
- ✅ **대운 분석**: 2세~81세 10년 주기 완벽 계산  
- ✅ **세운 분석**: 연간/월별 운세 분석
- ✅ **듀얼 AI 해석**: Google Gemini 2.5-flash + Azure GPT-4.1 
- ✅ **개인화된 질문 생성**: AI가 사주 기반 맞춤 질문 생성
- ✅ **현대적 UI/UX**: Gemini/Azure 선택 버튼, 직관적 인터페이스

#### NewCompatibility 서비스 (이중 AI 지원)
- ✅ **SAJU API 기반 궁합 분석**: 완전 독립 마이크로서비스
- ✅ **오행 상생상극 분석**: 정밀한 궁합 계산
- ✅ **십성 배합 분석**: 성격 궁합 점수화
- ✅ **듀얼 AI 해석**: Google Gemini + Azure GPT-4.1 (궁합 특화)
- ✅ **궁합 전용 질문 생성**: 결혼/갈등/소통/미래 등 맞춤 질문
- ✅ **실시간 AI 상담**: 관계 개선 조언 제공

### 🤖 AI 통합 현황

#### Azure OpenAI GPT-4.1 통합 (보안 강화)
- **SAJU**: `/api/v1/azure/` - 개인 사주 분석 특화
- **NewCompatibility**: `/api/v1/azure-compatibility/` - 궁합 분석 특화
- **공통 기능**: 대화형 해석, 개인화된 질문 생성, 연결 테스트
- **보안 강화**: 환경변수(.env) 기반 API 키 관리, GitHub 안전 푸시
- **안전한 통합**: try-catch로 Gemini와 독립 운영

#### Google Gemini 2.5-flash (기존)
- **SAJU**: `/api/v1/saju/` - 기존 서비스 유지
- **NewCompatibility**: `/api/v1/compatibility/` - 기존 서비스 유지

### 🔐 보안 강화 완료 (2025.08.07)

#### Azure OpenAI API 키 보안
- **환경변수 적용**: `.env` 파일로 API 키 분리
- **GitHub 보안**: `.gitignore`에 `.env` 제외 설정
- **개발자 설정**: 각 개발자는 개별 `.env` 파일 생성 필요
- **필수 환경변수**:
  ```
  AZURE_OPENAI_API_KEY=your-api-key
  AZURE_OPENAI_ENDPOINT=https://1team-openai.openai.azure.com
  AZURE_OPENAI_DEPLOYMENT=saju-gpt-4.1
  AZURE_OPENAI_VERSION=2025-01-01-preview
  ```

**🏆 이중 AI 지원 + 보안 강화로 세계 최고 수준의 온라인 사주/궁합 분석 플랫폼 완성!** 🚀
