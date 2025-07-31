# Physiognomy - 관상 분석 서비스 (v1.1 - 규칙 기반)

**[중요] 현재 버전은 MediaPipe를 이용한 기하학적 특징 추출과 사전 정의된 규칙에 기반하여 동작하는 초기 데모 버전입니다. 딥러닝 AI 모델은 적용되어 있지 않습니다.**

AI 기반 얼굴 인식을 통한 관상 분석 독립 서비스입니다.

## 🎯 서비스 개요

- **포트**: 백엔드 8001, 프론트엔드 3001
- **데이터베이스**: PostgreSQL (Docker Compose로 실행)
- **기술 스택**: FastAPI + React + MediaPipe

## 🚀 실행 방법

### Docker로 실행 (권장)
```bash
cd Physiognomy
docker-compose up --build
```

### 로컬에서 직접 실행

**백엔드 실행**
```bash
cd Physiognomy/backend
# .env 파일 생성 및 DATABASE_URL 설정 필요
# 예: DATABASE_URL=postgresql://user:password@localhost:5433/physiognomy
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**프론트엔드 실행**
```bash
cd Physiognomy/frontend
npm install
npm start
```

## 🔗 접속

- **웹 서비스**: [http://localhost:3001](http://localhost:3001)
- **API 문서**: [http://localhost:8001/docs](http://localhost:8001/docs)

## 📊 주요 기능 (v1.1)

- 얼굴 이미지 업로드 및 전처리
- **MediaPipe 기반 얼굴 랜드마크 추출**
- **사전 정의된 규칙에 따른 얼굴 특징 분석** (예: 얼굴 비율, 눈 사이 거리 등)
- 분석 결과 리포트 생성 및 이력 조회

## 📝 API 엔드포인트

- `POST /analyze/` - 관상 분석 요청 및 결과 저장
- `GET /analysis-history/` - 관상 분석 기록 조회

## 🔒 개인정보 보호

- 업로드된 이미지는 서버에 저장되며, 분석 기록 조회를 위해 사용됩니다.
- 개인 식별 정보는 최소한으로 수집하며, 주기적인 데이터 관리가 필요합니다.
