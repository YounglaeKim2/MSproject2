# 🎯 새로운 궁합 분석 서비스

> **SAJU API 기반 독립적인 궁합 분석 마이크로서비스**

## 🚀 서비스 개요

기존의 완벽하게 구축된 SAJU API를 활용하여 새로운 궁합 분석 서비스를 구현합니다.
기존 서비스들을 전혀 수정하지 않고 HTTP API 호출로 연동하는 안전한 방식입니다.

## 🏗️ 아키텍처

```
새 궁합 서비스 (포트 3003/8003)
           ↓ HTTP 호출
기존 SAJU API (포트 8000) ← 변경 없음!
```

## 📁 디렉토리 구조

```
NewCompatibility/
├── backend/                 # FastAPI 백엔드 (포트 8003)
│   ├── app/
│   │   ├── main.py         # FastAPI 앱
│   │   ├── models/         # 데이터 모델
│   │   ├── services/       # 비즈니스 로직
│   │   └── routers/        # API 라우터
│   └── requirements.txt
└── frontend/               # React 프론트엔드 (포트 3003)
    └── (추후 구현)
```

## 🔧 실행 방법

### 백엔드 실행

```bash
# 1. 디렉토리 이동
cd C:\workspace\MSproject2\NewCompatibility\backend

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행
python -m uvicorn app.main:app --reload --port 8003 --host 0.0.0.0
```

### 확인

- 백엔드: http://localhost:8003
- API 문서: http://localhost:8003/docs
- 헬스체크: http://localhost:8003/health
- 서비스 정보: http://localhost:8003/info

## 📋 개발 단계

- [x] **Phase 1**: 프로젝트 구조 생성 ✅
- [ ] **Phase 2**: SAJU API 클라이언트 구현
- [ ] **Phase 3**: 궁합 계산 엔진 구현
- [ ] **Phase 4**: API 라우터 구현
- [ ] **Phase 5**: 프론트엔드 구현
- [ ] **Phase 6**: 도커화 및 배포

## ⚠️ 주의사항

1. **기존 서비스 무손상**: SAJU API는 절대 수정하지 않음
2. **포트 분리**: 8003(백엔드), 3003(프론트엔드) 사용
3. **독립 실행**: 다른 서비스와 완전히 독립적
4. **API 호출**: HTTP 통신으로만 SAJU API 활용

## 🎯 목표

- ✅ 안정적인 개발 (기존 서비스 무손상)
- ✅ 코드 재사용 (SAJU API 활용)
- ✅ 마이크로서비스 패턴 완성
- ✅ 확장 가능한 아키텍처
