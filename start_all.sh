#!/bin/bash

echo "========================================"
echo "  MSProject2 SAJU - 전체 서비스 시작"
echo "========================================"
echo

# 현재 디렉토리 확인
if [ ! -d "main-app" ]; then
    echo "[ERROR] MSProject2_SAJU 루트 디렉토리에서 실행해주세요!"
    exit 1
fi

# 포트 사용 여부 확인
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "[WARNING] 포트 $1이 이미 사용 중입니다!"
        echo "[WARNING] 다음 명령으로 프로세스를 종료하세요: kill -9 \$(lsof -ti:$1)"
        return 1
    fi
    return 0
}

echo "[INFO] 포트 사용 여부 확인 중..."
check_port 4000 || exit 1
check_port 3000 || exit 1
check_port 8000 || exit 1

echo "[INFO] 모든 서비스를 백그라운드에서 시작합니다..."
echo "[INFO] 로그는 각각의 .log 파일에서 확인할 수 있습니다."
echo

# 로그 디렉토리 생성
mkdir -p logs

# 1. 메인 앱 (포트 4000) - Vite 버전
echo "[1/6] 메인 앱 시작 중... (포트 4000) [Vite - 초고속!]"
cd main-app
npm install > ../logs/main-app-install.log 2>&1
nohup npm start > ../logs/main-app.log 2>&1 &
MAIN_PID=$!
cd ..
sleep 3

# 2. SAJU 백엔드 (포트 8000)
echo "[2/6] SAJU 백엔드 시작 중... (포트 8000)"
cd SAJU/backend
pip install -r requirements.txt > ../../logs/saju-backend-install.log 2>&1
nohup uvicorn app.main:app --reload --port 8000 > ../../logs/saju-backend.log 2>&1 &
SAJU_BACKEND_PID=$!
cd ../..
sleep 5

# 3. SAJU 프론트엔드 (포트 3000)
echo "[3/6] SAJU 프론트엔드 시작 중... (포트 3000)"
cd SAJU/frontend
npm install > ../../logs/saju-frontend-install.log 2>&1
nohup npm start > ../../logs/saju-frontend.log 2>&1 &
SAJU_FRONTEND_PID=$!
cd ../..
sleep 3

# 4. 궁합 백엔드 (포트 8002)
echo "[4/6] 궁합 백엔드 시작 중... (포트 8002)"
cd Compatibility/backend
pip install -r requirements.txt > ../../logs/compatibility-backend-install.log 2>&1
nohup uvicorn app.main:app --reload --port 8002 > ../../logs/compatibility-backend.log 2>&1 &
COMPATIBILITY_BACKEND_PID=$!
cd ../..
sleep 5

# 5. 궁합 프론트엔드 (포트 3002)
echo "[5/6] 궁합 프론트엔드 시작 중... (포트 3002)"
cd Compatibility/frontend
npm install > ../../logs/compatibility-frontend-install.log 2>&1
nohup npm start > ../../logs/compatibility-frontend.log 2>&1 &
COMPATIBILITY_FRONTEND_PID=$!
cd ../..
sleep 3

# 6. 관상학 서비스 (Docker 필수!)
echo "[6/6] 관상학 서비스 시작 중... (포트 8001/3001)"
echo "[IMPORTANT] Docker가 실행 중인지 확인해주세요!"
cd Physiognomy
nohup docker-compose up --build > ../logs/physiognomy.log 2>&1 &
PHYSIOGNOMY_PID=$!
cd ..

# PID 저장
echo $MAIN_PID > logs/main-app.pid
echo $SAJU_BACKEND_PID > logs/saju-backend.pid
echo $SAJU_FRONTEND_PID > logs/saju-frontend.pid
echo $COMPATIBILITY_BACKEND_PID > logs/compatibility-backend.pid
echo $COMPATIBILITY_FRONTEND_PID > logs/compatibility-frontend.pid
echo $PHYSIOGNOMY_PID > logs/physiognomy.pid

echo
echo "========================================"
echo "  모든 서비스 시작 완료!"
echo "========================================"
echo
echo "서비스 접속 URL:"
echo "  메인 허브:   http://localhost:4000"
echo "  사주 분석:   http://localhost:3000"
echo "  궁합 분석:   http://localhost:3002"
echo "  관상 분석:   http://localhost:3001"
echo
echo "API 문서:"
echo "  SAJU API:    http://localhost:8000/docs"
echo "  궁합 API:    http://localhost:8002/docs"
echo "  관상 API:    http://localhost:8001/docs"
echo
echo "로그 파일:"
echo "  tail -f logs/[service-name].log"
echo
echo "서비스 중지:"
echo "  ./stop_all.sh"
echo
echo "[주의] 모든 서비스가 완전히 시작되려면 2-3분 정도 소요됩니다."
echo "[주의] 관상학 서비스는 Docker 빌드로 인해 추가 시간이 필요할 수 있습니다."
echo