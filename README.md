# MSproject2 - 사주 웹 서비스

한국 전통 명리학 기반의 사주팔자 분석 웹 서비스입니다.

## 🎯 프로젝트 개요

이 프로젝트는 전통 명리학을 현대 웹 기술과 결합하여 사용자에게 정확하고 체계적인 사주 분석 서비스를 제공합니다.

### 주요 특징
- ✅ **정확한 만세력 계산**: 1900-2100년 73,442개 레코드 기반
- ✅ **전문적인 해석 로직**: 오행, 십성, 신살 등 종합 분석
- ✅ **현대적인 UI/UX**: React + TypeScript 기반 반응형 디자인
- ✅ **RESTful API**: FastAPI 기반 고성능 백엔드

## 📁 프로젝트 구조

```
MSproject2/
├── main-app/                   # 메인 랜딩 페이지 (포트: 4000)
│   ├── frontend/              # 서비스 선택 화면
│   └── package.json
├── SAJU/                      # 사주팔자 서비스 (완전 독립)
│   ├── backend/               # FastAPI 백엔드 (포트: 8000)
│   ├── frontend/              # React 프론트엔드 (포트: 3000)
│   ├── manseryukDB/           # 만세력 데이터베이스
│   ├── 사주해석로직.txt        # 명리학 해석 로직 문서
│   ├── docker-compose.yml     # Docker 설정
│   └── README.md              # 사주 서비스 가이드
├── Physiognomy/               # 관상 분석 서비스 (완전 독립)
│   ├── backend/               # FastAPI 백엔드 (포트: 8001)
│   ├── frontend/              # React 프론트엔드 (포트: 3001)
│   ├── models/                # AI 모델
│   ├── datasets/              # 학습 데이터
│   ├── docker-compose.yml     # Docker 설정
│   └── README.md              # 관상 서비스 가이드
├── CLAUDE.md                  # Claude Code용 개발 가이드
└── README.md                  # 프로젝트 전체 가이드
```

## 🚀 설치 및 실행

### 사전 요구사항
- Python 3.8+
- Node.js 14+
- npm 또는 yarn

### 메인 랜딩 페이지 실행
```bash
cd main-app
npm install
npm start
```

### 사주 서비스 실행
```bash
# 백엔드
cd SAJU/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 (새 터미널)
cd SAJU/frontend
npm install
npm start
```

### 관상 서비스 실행 (동료 개발자용)
```bash
# 백엔드
cd Physiognomy/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 프론트엔드 (새 터미널)
cd Physiognomy/frontend
npm install
npm start
```

### 접속
- **메인 페이지**: http://localhost:4000
- **사주 서비스**: http://localhost:3000
- **관상 서비스**: http://localhost:3001
- **사주 API 문서**: http://localhost:8000/docs
- **관상 API 문서**: http://localhost:8001/docs

## 🔧 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Pydantic**: 데이터 검증 및 설정 관리
- **SQLite**: 만세력 데이터베이스
- **Uvicorn**: ASGI 서버

### 프론트엔드
- **React 18**: 사용자 인터페이스 라이브러리
- **TypeScript**: 타입 안전성
- **Styled Components**: CSS-in-JS 스타일링
- **Axios**: HTTP 클라이언트

## 📊 주요 기능

### 사주팔자 분석
- 정확한 년월일시 기반 사주팔자 추출
- 절기 기준 월주 계산
- 시주 정밀 계산

### 오행 분석
- 사주 내 오행 분포 계산
- 일간 강약 판단 (신강/신약)
- 용신/기신 도출

### 종합 해석
- **성격 분석**: 기본 성향, 장단점, 개선 방향
- **직업운**: 적성 분야, 성향, 성공 요인
- **건강운**: 강약 장기, 주의사항, 관리법
- **대인관계**: 관계 스타일, 궁합, 사회성
- **재물운**: 재물 성향, 수입 패턴, 투자 조언

## 📱 화면 구성

### 메인 화면
- 출생 정보 입력 폼
- 년/월/일/시/성별 선택
- 실시간 유효성 검사

### 결과 화면
- 사주팔자 시각적 표현
- 오행 분포 차트
- 카테고리별 상세 분석
- 반응형 레이아웃

## 🔗 API 엔드포인트

### 주요 API
- `POST /api/v1/saju/analyze` - 완전한 사주 분석
- `GET /api/v1/saju/palja-only` - 사주팔자만 추출
- `GET /api/v1/saju/wuxing-only` - 오행 분석만
- `GET /api/v1/saju/test` - API 테스트
- `GET /health` - 헬스 체크

### 예시 요청
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

## 📚 참고 자료

### 명리학 이론
- 고영창님의 "진짜 만세력" 기반 데이터
- 전통 명리학 해석 로직
- 음양오행 상생상극 이론

### 기술 문서
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [React 공식 문서](https://react.dev/)
- [TypeScript 핸드북](https://www.typescriptlang.org/docs/)

## 🔮 향후 계획

### Phase 2 - 관상 서비스
- 얼굴 인식 기반 관상 분석
- AI 모델 통합
- 사주와 관상 종합 해석

### Phase 3 - 고도화
- 대운/세운 분석
- 궁합 서비스
- 개인화 추천 시스템

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 개인 학습 및 연구 목적으로 개발되었습니다.

## 📞 문의

프로젝트 관련 문의사항이 있으시면 GitHub Issues를 통해 연락해 주세요.

---

**⚠️ 주의사항**: 이 서비스는 참고용이며, 중요한 결정은 전문가와 상담하시기 바랍니다.