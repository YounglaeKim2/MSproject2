# SAJU - 사주팔자 분석 서비스

> 전통 명리학 기반 완전한 사주 분석 시스템 ✅ **100% 완성**

## 🎯 서비스 개요

**37개 메서드**로 구성된 전문적인 사주 분석 엔진
- 기본 분석 + 확장 분석 + 대운 + 세운 완전 지원

## 🚀 실행 방법

```bash
# 백엔드 (:8000)
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 (:3000)  
cd frontend && npm install && npm start
```

## 📊 주요 기능

### ✅ 완성된 분석 시스템
- **사주팔자**: 정확한 년/월/일/시주 계산
- **오행 분석**: 0-100점 균형 점수 + 6가지 성격 유형
- **대운 분석**: 10년 주기 (2세-81세, 8개 대운)
- **세운 분석**: 연간/월별 상세 운세
- **맞춤 조언**: 8가지 카테고리 (색상/방향/직업/건강/관계)

### 🔗 API 엔드포인트
```
POST /api/v1/saju/analyze    # 완전한 사주 분석
POST /api/v1/saju/daeun      # 대운 분석
POST /api/v1/saju/saeun      # 세운 분석
GET  /api/v1/saju/test       # API 테스트
```

## 📁 구조

```
SAJU/
├── backend/           # FastAPI 서버
│   ├── app/
│   │   ├── api/saju.py           # 7개 엔드포인트
│   │   ├── services/saju_analyzer.py  # 37개 분석 메서드
│   │   └── models/saju.py        # Pydantic 모델
│   └── requirements.txt
├── frontend/          # React UI
│   ├── src/App.tsx    # 메인 분석 화면
│   └── package.json
├── manseryukDB/       # 만세력 DB (73,442 레코드)
└── 사주해석로직.txt     # 명리학 문서
```

## 🔧 기술 스택

- **백엔드**: FastAPI + Pydantic + SQLite
- **프론트엔드**: React 18 + TypeScript + styled-components
- **데이터**: 만세력 DB (1900-2100년)

## 🌐 접속

- **UI**: http://localhost:3000
- **API**: http://localhost:8000  
- **문서**: http://localhost:8000/docs

## 📚 사용 예시

```json
{
  "year": 1990, "month": 5, "day": 15, "hour": 14,
  "gender": "male", "name": "홍길동"
}
```

**결과**: 89.6점 균형점수, 성장형 성격, 7-9월 최고운세

---

**완전히 구현된 전문 사주 분석 서비스입니다!** 🎉