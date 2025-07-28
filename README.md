# MSproject2 - 전문 사주팔자 분석 웹 서비스

> 한국 전통 명리학과 현대 웹 기술의 완벽한 결합 🎯

## 🎉 주요 특징

- ✅ **정확한 만세력**: 1900-2100년 73,442개 레코드 기반
- 🆕 **확장 분석**: 13개 신규 메서드, 0-100점 균형 측정
- ⏳ **대운/세운**: 10년 주기 대운 + 연간/월별 세운 분석
- 🎯 **맞춤 조언**: 색상/방향/직업/건강/관계 등 8가지 카테고리
- 🎨 **현대적 UI**: styled-components 기반 반응형 디자인

## 📁 프로젝트 구조

```
MSproject2/
├── main-app/           # 메인 랜딩 페이지 (:4000)
├── SAJU/              # 사주 분석 서비스 (:8000/:3000)
│   ├── backend/       # FastAPI + 37개 분석 메서드
│   ├── frontend/      # React + TypeScript UI
│   ├── manseryukDB/   # 만세력 데이터베이스
│   └── 사주해석로직.txt # 명리학 해석 문서
└── Physiognomy/       # 관상 분석 서비스 (:8001/:3001)
```

## 🚀 빠른 시작

### 필수 설치
- Python 3.8+ | Node.js 14+ | Git

### 실행 (3개 터미널)
```bash
# 터미널 1: 메인 앱
cd main-app && npm install && npm start

# 터미널 2: 사주 백엔드
cd SAJU/backend && pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 터미널 3: 사주 프론트엔드
cd SAJU/frontend && npm install && npm start
```

### 접속 URL
| 서비스 | URL | 상태 |
|--------|-----|------|
| 메인 페이지 | http://localhost:4000 | ✅ |
| 사주 분석 | http://localhost:3000 | ✅ |
| API 문서 | http://localhost:8000/docs | ✅ |

## 🌟 핵심 기능

### 📊 사주 분석 시스템
- **사주팔자**: 년/월/일/시주 정확 계산
- **오행 분석**: 균형 점수 + 성격 유형 (6가지)
- **십성 분석**: 비견/겁재/식신/상관/편재/정재/편관/정관/편인/정인

### ⏳ 운세 시스템
- **대운**: 10년 주기 (2세-81세, 8개 대운)
- **세운**: 연간/월별 상세 운세
- **현재 운세**: 나이별 맞춤 분석

### 🎯 맞춤 조언
🎨 색상 | 🧭 방향 | 🍽️ 음식 | 🏃 활동 | 🏠 라이프스타일 | 💼 직업 | 💊 건강 | 💑 관계

## 🔗 API 엔드포인트

```bash
POST /api/v1/saju/analyze    # 완전한 사주 분석
POST /api/v1/saju/daeun      # 대운 분석
POST /api/v1/saju/saeun      # 세운 분석
GET  /api/v1/saju/test       # API 테스트
```

## 🔧 기술 스택

**백엔드**: FastAPI + Pydantic + SQLite  
**프론트엔드**: React 18 + TypeScript + styled-components  
**데이터**: 만세력 DB (73,442 레코드) + 전통 명리학 로직

## 📚 사용 예시

```json
{
  "year": 1990, "month": 5, "day": 15, "hour": 14,
  "gender": "male", "name": "홍길동"
}
```

**결과**: 89.6점 균형 점수, 성장형 성격, 7-9월 최고 운세

## 🏆 프로젝트 현황

**구현도**: 100% ✅ | **서비스**: 즉시 이용 가능 🚀

- ✅ 모든 분석 기능 완성 (37개 메서드)
- ✅ 전문가급 해석 정확도
- ✅ 현대적 UI/UX 완성
- ✅ 안정적 서비스 운영

---

**⚠️ 참고용 서비스입니다. 중요한 결정은 전문가와 상담하세요.**