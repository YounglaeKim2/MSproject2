# 🔮 MSProject2 SAJU 

### 전통 명리학 + 현대 AI 기술 융합 플랫폼

<div align="center">

![서비스 상태](https://img.shields.io/badge/서비스-운영중-brightgreen)
![마이크로서비스](https://img.shields.io/badge/마이크로서비스-5개-blue)
![완성도](https://img.shields.io/badge/완성도-100%25-success)
![AI 모델](https://img.shields.io/badge/AI-Gemini%202.5--flash-orange)
![배포](https://img.shields.io/badge/배포-Docker-blue)

**🏆 대한민국 최고 수준의 5개 마이크로서비스 완전체**

[**🚀 빠른 시작**](#-빠른-시작) • [**📖 사용법**](#-사용-예시) • [**🔗 API 문서**](#-api-엔드포인트) • [**📚 문서**](docs/)

</div>

---

## 📊 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **서비스 수** | 5개 (Main, SAJU Web/Mobile, Compatibility, Physiognomy) |
| **데이터베이스** | 73,442개 만세력 레코드 (1900-2100년) |
| **분석 메서드** | 37개 (사주팔자, 오행, 십성, 대운, 세운) + 8개 확장운세 |
| **AI 기술** | Google Gemini 2.5-flash, MediaPipe, OpenCV |
| **아키텍처** | 마이크로서비스 + 크로스플랫폼 (웹/모바일) |
| **프론트엔드** | React 18 + React Native (Expo) + TypeScript |
| **백엔드** | FastAPI + Pydantic |

## 🏗️ 서비스 아키텍처

<div align="center">

```mermaid
graph TB
    A[사용자] --> B[Landing Page :4000]
    A --> M[📱 Mobile App :8082]
    B --> C[SAJU Web :3000]
    B --> D[Compatibility Service :3002] 
    B --> E[Physiognomy Service :3001]
    
    C --> F[SAJU API :8000]
    M --> F
    D --> G[Compatibility API :8002]
    E --> H[Physiognomy API :8001]
    
    F --> I[(만세력 DB<br/>73,442 records)]
    F --> J[Google Gemini 2.5]
    F --> N[8개 확장운세<br/>Phase 1+2]
    H --> K[MediaPipe + OpenCV]
    H --> L[(PostgreSQL)]
```

</div>

## 🎉 완성된 서비스들

<table>
<tr>
<td width="50%">

### 🏠 Main Landing
**포트**: 4000  
**역할**: 통합 랜딩 허브  
**기술**: HTML + CSS + Python  
**상태**: ✅ 운영중

### 🔮 SAJU Service  
**포트**: 3000/8000  
**역할**: 사주팔자 분석  
**기능**: 37개 분석 메서드 + 8개 확장운세  
**데이터**: 73,442개 만세력  
**AI**: Google Gemini 2.5-flash  
**상태**: ✅ 운영중

### 📱 AppService Mobile
**포트**: 8082  
**역할**: 모바일 사주 분석 앱  
**플랫폼**: iOS/Android (React Native + Expo)  
**기능**: 웹과 동등한 모든 기능  
**상태**: ✅ 운영중

</td>
<td width="50%">

### 💕 Compatibility Service
**포트**: 3002/8002  
**역할**: 궁합 분석  
**기능**: 사주 기반 궁합  
**알고리즘**: 오행상성 + 십성매칭  
**상태**: ✅ 운영중

### 🎭 Physiognomy Service
**포트**: 3001/8001  
**역할**: AI 관상 분석  
**기술**: MediaPipe + OpenCV  
**배포**: Docker Compose  
**상태**: ✅ 운영중

</td>
</tr>
</table>

## 🏗️ 마이크로서비스 아키텍처

```
MSProject2/
├── main-app/           # 통합 허브 (:4000)
├── SAJU/              # 사주팔자 분석 (:8000/:3000)
│   ├── backend/       # FastAPI + 37개 분석 메서드 + 8개 확장운세
│   ├── frontend/      # React 18 + TypeScript
│   ├── manseryukDB/   # 73,442개 만세력 DB
│   └── 사주해석로직.txt # 전통 명리학 문서
├── AppService/        # 모바일 앱 (:8082)
│   └── FortuneApp/    # React Native + Expo
├── Compatibility/     # 궁합 분석 (:8002/:3002)
│   ├── backend/       # FastAPI + 궁합 알고리즘
│   └── frontend/      # React 18 + TypeScript
├── Physiognomy/       # 관상 분석 (:8001/:3001)
│   ├── backend/       # FastAPI + AI 모델
│   ├── frontend/      # React 18 + TypeScript
│   └── docker-compose.yml # Docker 배포
└── docs/              # 프로젝트 문서
    ├── 01-setup/      # 설치 및 설정 가이드
    ├── 02-api/        # API 문서
    └── 03-features/   # 기능 상세 설명

## 🚀 빠른 시작

### 📋 필수 요구사항

<div align="center">

| 요구사항 | 버전 | 필수 여부 |
|----------|------|----------|
| Python | 3.8+ | ✅ 필수 |
| Node.js | 14+ | ✅ 필수 |  
| Git | latest | ✅ 필수 |
| Docker Desktop | latest | 🔶 권장 |

</div>

### ⚡ 원클릭 실행

```bash
# 1. 레포지토리 클론
git clone https://github.com/your-repo/MSproject2.git
cd MSproject2

# 2. 모든 서비스 한번에 시작
./start_all.sh

# 3. 서비스 상태 확인  
./check_services.sh
```

### 🔧 수동 실행 (상세 제어)

<details>
<summary>클릭하여 상세 실행 방법 보기</summary>

```bash
# 터미널 1: 메인 앱
cd main-app && npm install && npm start

# 터미널 2: SAJU 백엔드  
cd SAJU/backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 터미널 3: SAJU 프론트엔드
cd SAJU/frontend && npm install && npm start

# 터미널 4: 궁합 백엔드
cd Compatibility/backend && pip install -r requirements.txt  
uvicorn app.main:app --reload --port 8002

# 터미널 5: 궁합 프론트엔드
cd Compatibility/frontend && npm install && npm start

# 터미널 6: 관상학 서비스 (Docker)
cd Physiognomy && docker-compose up
```

</details>

### 🌐 서비스 접속

<div align="center">

#### 🖥️ 사용자 서비스

[![Main App](https://img.shields.io/badge/🏠_Main_App-4000-blue?style=for-the-badge)](http://localhost:4000)
[![SAJU 분석](https://img.shields.io/badge/🔮_SAJU_분석-3000-purple?style=for-the-badge)](http://localhost:3000)
[![궁합 분석](https://img.shields.io/badge/💕_궁합_분석-3002-pink?style=for-the-badge)](http://localhost:3002)
[![관상 분석](https://img.shields.io/badge/🎭_관상_분석-3001-orange?style=for-the-badge)](http://localhost:3001)

#### 📚 API 문서

[![SAJU API](https://img.shields.io/badge/SAJU_API-8000-green?style=flat-square)](http://localhost:8000/docs)
[![궁합 API](https://img.shields.io/badge/궁합_API-8002-green?style=flat-square)](http://localhost:8002/docs)
[![관상 API](https://img.shields.io/badge/관상_API-8001-green?style=flat-square)](http://localhost:8001/docs)

#### 📱 모바일 앱

[![Mobile App](https://img.shields.io/badge/📱_Mobile_App-8082-indigo?style=flat-square)](http://localhost:8082) (Expo 웹 모드)

</div>

## 🌟 핵심 기능

### 📊 1. SAJU Service - 사주팔자 분석
- **사주팔자**: 년/월/일/시주 정확 계산 (73,442개 만세력 DB)
- **오행 분석**: 균형 점수 + 성격 유형 (6가지)
- **십성 분석**: 비견/겁재/식신/상관/편재/정재/편관/정관/편인/정인
- **대운**: 10년 주기 (2세-81세, 8개 대운)
- **세운**: 연간/월별 상세 운세
- **확장운세**: 8개 영역 (연애/성격/인관/재물/직업/건강/학업/가족)
- **AI 채팅**: Google Gemini 2.5-flash 대화형 해석

### 📱 4. AppService Mobile - 모바일 앱
- **크로스플랫폼**: iOS/Android 동시 지원 (React Native + Expo)
- **완전한 기능**: 웹 버전과 동등한 모든 사주 분석 기능
- **8개 확장운세**: Phase 1+2 모든 운세 카드 지원
- **실시간 API**: SAJU 백엔드와 완전 연동
- **직관적 UI**: 모바일 최적화된 사용자 경험

### 💕 2. Compatibility Service - 궁합 분석
- **사주 기반 궁합**: 두 사람의 사주팔자 비교 분석
- **오행 상성**: 상생/상극 관계 분석
- **성격 매칭**: 십성 기반 성격 궁합
- **종합 점수**: 0-100점 궁합 지수

### 🎭 3. Physiognomy Service - AI 관상 분석
- **얼굴 인식**: MediaPipe 기반 468개 랜드마크 추출
- **기하학적 분석**: OpenCV 얼굴 특징 계산
- **관상학 해석**: 전통 관상학 + AI 융합 분석
- **실시간 처리**: 웹캠/이미지 업로드 지원

### 🎯 맞춤 조언 시스템
🎨 색상 | 🧭 방향 | 🍽️ 음식 | 🏃 활동 | 🏠 라이프스타일 | 💼 직업 | 💊 건강 | 💑 관계

## 🔗 API 엔드포인트

### SAJU API (포트 8000)
```bash
POST /api/v1/saju/analyze    # 완전한 사주 분석 (37개 메서드)
POST /api/v1/saju/daeun      # 대운 분석
POST /api/v1/saju/saeun      # 세운 분석
GET  /api/v1/saju/palja-only # 사주팔자만
GET  /api/v1/saju/wuxing-only # 오행 분석만
GET  /api/v1/saju/health     # 헬스 체크
```

### Compatibility API (포트 8002)
```bash  
POST /api/v1/compatibility/analyze  # 궁합 분석
GET  /api/v1/compatibility/health   # 헬스 체크
```

### Physiognomy API (포트 8001)
```bash
POST /analyze        # 관상 분석 (이미지 업로드)
GET  /docs           # API 문서
```

## 🔧 기술 스택

### 백엔드 
- **프레임워크**: FastAPI + Pydantic
- **데이터베이스**: SQLite (SAJU), PostgreSQL (Physiognomy)
- **AI 모델**: Google Gemini 2.5-flash, MediaPipe, OpenCV
- **벡터 DB**: FAISS (관상학 RAG)

### 프론트엔드
- **프레임워크**: React 18 + TypeScript  
- **스타일링**: styled-components
- **빌드**: Create React App, Webpack

### 배포 & 인프라
- **컨테이너**: Docker + Docker Compose
- **서버**: Uvicorn (개발), Nginx (프로덕션)
- **데이터**: 73,442개 만세력 레코드 + AI 벡터 DB

## 📚 사용 예시

### SAJU 분석 요청
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "gender": "male",
  "name": "홍길동"
}
```
**결과**: 89.6점 균형 점수, 성장형 성격, 7-9월 최고 운세

### 궁합 분석 요청
```json
{
  "person1": {"year": 1990, "month": 5, "day": 15, "hour": 14, "gender": "male"},
  "person2": {"year": 1992, "month": 8, "day": 22, "hour": 10, "gender": "female"}
}
```
**결과**: 83.5점 궁합 지수, 상생 관계, 조화로운 성격 매칭

### 관상 분석 (이미지 업로드)
- **지원 형식**: JPG, PNG, WebP
- **분석 항목**: 이목구비, 얼굴형, 인상
- **결과**: 성격 분석 + 운세 해석

## 🏆 프로젝트 현황 (2025-08-03 완성)

### ✅ 완성도: 100%
- **5개 서비스** 완전 구현 (웹 4개 + 모바일 1개)
- **73,442개 만세력 데이터** 구축
- **37개 사주 분석 메서드 + 8개 확장운세** 완성
- **크로스플랫폼 앱** 구축 (웹 + iOS/Android)
- **AI 관상 분석 시스템** 구축
- **Docker 컨테이너화** 완료

### 🚀 즉시 이용 가능
- **웹 브라우저**에서 바로 접속
- **모바일 앱** (iOS/Android) 실행 가능
- **모든 기능** 정상 작동
- **실시간 분석** 지원
- **현대적 UI/UX** 제공

### 🏅 기술적 성취
- **마이크로서비스 아키텍처** 구현
- **크로스플랫폼 개발** 완성 (웹 + 모바일)
- **전통 명리학 디지털화** 완성
- **최신 AI 기술 융합** (Gemini, MediaPipe, React Native)
- **Docker 기반 배포** 최적화

### 📈 비즈니스 가치
- **시장 차별화**: 대한민국 최고 수준 플랫폼
- **확장성**: 마이크로서비스로 무한 확장 가능
- **상용화 준비**: 완전한 웹 서비스 형태

---

## 🔮 Future Roadmap

### 🚀 Next Features (구현 대기)
- **AI 기반 예상 질문 제안 시스템** - 사주 맞춤 질문 자동 생성
- **궁합운 점수 극단화** - 명확한 결과 (0-30 또는 70-100)
- **실시간 알림** 시스템
- **소셜 기능** 추가
- **프리미엄 서비스** 확장

### 📚 완전한 문서화
- 전체 설치/실행 가이드
- API 상세 문서
- 모바일 앱 개발 과정
- AI 시스템 설계 문서

---

**⚠️ 본 서비스는 참고용입니다. 중요한 결정은 전문가와 상담하시기 바랍니다.**

*© 2025 MSProject2 SAJU. 전통 명리학 + 현대 AI 기술의 완벽한 융합.*
