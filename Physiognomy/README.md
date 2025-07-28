# Physiognomy - 관상 분석 서비스

AI 기반 얼굴 인식을 통한 관상 분석 독립 서비스입니다.

## 🎯 서비스 개요

- **포트**: 백엔드 8001, 프론트엔드 3001
- **데이터베이스**: PostgreSQL/SQLite (관상 데이터)
- **기술 스택**: FastAPI + React + TensorFlow/PyTorch

## 📁 디렉토리 구조

```
Physiognomy/
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── api/           # API 라우터
│   │   ├── core/          # 설정
│   │   ├── models/        # 데이터 모델
│   │   ├── services/      # 관상 분석 서비스
│   │   └── ml/            # 머신러닝 모델
│   ├── uploads/           # 업로드된 이미지
│   ├── datasets/          # 학습 데이터셋
│   └── requirements.txt
├── frontend/              # React 프론트엔드
│   ├── src/
│   │   ├── components/    # 컴포넌트
│   │   ├── services/      # API 통신
│   │   ├── types/         # 타입 정의
│   │   └── utils/         # 유틸리티
│   └── package.json
├── models/                # AI 모델 파일
├── docs/                  # 관상학 문서
├── docker-compose.yml     # 컨테이너 설정
├── .env.example          # 환경 설정 예시
└── README.md             # 이 파일
```

## 🚀 실행 방법

### 백엔드 실행
```bash
cd Physiognomy/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 프론트엔드 실행
```bash
cd Physiognomy/frontend
npm install
npm start
```

### Docker로 실행
```bash
cd Physiognomy
docker-compose up
```

## 🔗 접속

- **웹 서비스**: http://localhost:3001
- **API 문서**: http://localhost:8001/docs

## 📊 주요 기능

- 얼굴 이미지 업로드 및 전처리
- AI 기반 얼굴 특징 분석
- 전통 관상학 이론 적용
- 성격, 운세, 적성 해석
- 실시간 분석 결과 제공

## 🤖 AI 모델

- **얼굴 인식**: OpenCV + MediaPipe
- **특징 추출**: CNN 기반 딥러닝 모델
- **관상 분류**: 전통 관상학 + 머신러닝

## 🔧 개발 환경

- Python 3.8+
- Node.js 14+
- TensorFlow 2.x / PyTorch
- OpenCV, MediaPipe

## 📝 API 엔드포인트

- `POST /api/v1/physiognomy/analyze` - 관상 분석
- `POST /api/v1/physiognomy/upload` - 이미지 업로드
- `GET /api/v1/physiognomy/features` - 얼굴 특징 추출

## 🔒 개인정보 보호

- 업로드된 이미지는 분석 후 즉시 삭제
- 개인 식별 정보 저장 안함
- GDPR 준수