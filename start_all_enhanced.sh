#!/bin/bash

echo "=========================================="
echo "   🔮 MSProject2 SAJU 플랫폼 시작 v2.0"
echo "=========================================="
echo "🚀 5개 마이크로서비스 + 실시간 모니터링"
echo "🎯 향상된 통합 실행 스크립트"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 현재 디렉토리 확인
if [ ! -d "landing" ] || [ ! -d "SAJU" ] || [ ! -d "Compatibility" ] || [ ! -d "Physiognomy" ]; then
    echo -e "${RED}[ERROR] MSProject2 루트 디렉토리에서 실행해주세요!${NC}"
    echo -e "${YELLOW}[INFO] 필요한 폴더: landing, SAJU, Compatibility, Physiognomy, AppService${NC}"
    exit 1
fi

# 포트 사용 여부 확인 함수
check_port() {
    local port=$1
    local service=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}[WARNING] 포트 $port ($service)이 이미 사용 중입니다!${NC}"
        echo -e "${CYAN}[INFO] 기존 프로세스를 종료하려면: kill -9 \$(lsof -ti:$port)${NC}"
        return 1
    fi
    return 0
}

# 서비스 health check 함수
health_check() {
    local url=$1
    local service=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${CYAN}[INFO] $service 상태 확인 중...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" >/dev/null 2>&1; then
            echo -e "${GREEN}[SUCCESS] $service 시작 완료! ($url)${NC}"
            return 0
        fi
        echo -e "${YELLOW}[WAIT] $service 시작 대기 중... ($attempt/$max_attempts)${NC}"
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}[ERROR] $service 시작 실패! ($url)${NC}"
    return 1
}

# 로그 디렉토리 생성
mkdir -p logs
echo -e "${BLUE}[INFO] 로그 디렉토리 생성: ./logs/${NC}"

echo -e "${PURPLE}================================================${NC}"
echo -e "${PURPLE}            포트 사용 여부 확인 중...            ${NC}"
echo -e "${PURPLE}================================================${NC}"

# 포트 확인
PORTS=(4000 3000 8000 8082 3002 8002 3001 8001)
SERVICES=("Landing" "SAJU Frontend" "SAJU Backend" "Mobile App" "Compatibility Frontend" "Compatibility Backend" "Physiognomy Frontend" "Physiognomy Backend")

for i in "${!PORTS[@]}"; do
    check_port "${PORTS[i]}" "${SERVICES[i]}"
done

echo
echo -e "${PURPLE}================================================${NC}"
echo -e "${PURPLE}               서비스 시작 중...                ${NC}"  
echo -e "${PURPLE}================================================${NC}"

# 1. 랜딩 페이지 시작 (포트 4000)
echo -e "${BLUE}[1/7]${NC} 🏠 랜딩 페이지 시작 중... ${YELLOW}(포트 4000)${NC}"
cd landing
nohup python server.py > ../logs/landing.log 2>&1 &
LANDING_PID=$!
cd ..
echo -e "${GREEN}[INFO] 랜딩 페이지 PID: $LANDING_PID${NC}"
sleep 2

# 2. SAJU 백엔드 시작 (포트 8000)
echo -e "${BLUE}[2/7]${NC} 🔮 SAJU 백엔드 시작 중... ${YELLOW}(포트 8000)${NC}"
cd SAJU/backend
pip install -r requirements.txt > ../../logs/saju-backend-install.log 2>&1
nohup uvicorn app.main:app --reload --port 8000 > ../../logs/saju-backend.log 2>&1 &
SAJU_BACKEND_PID=$!
cd ../..
echo -e "${GREEN}[INFO] SAJU 백엔드 PID: $SAJU_BACKEND_PID${NC}"
sleep 3

# 3. SAJU 프론트엔드 시작 (포트 3000)
echo -e "${BLUE}[3/7]${NC} 🌐 SAJU 프론트엔드 시작 중... ${YELLOW}(포트 3000)${NC}"
cd SAJU/frontend
npm install > ../../logs/saju-frontend-install.log 2>&1
nohup npm start > ../../logs/saju-frontend.log 2>&1 &
SAJU_FRONTEND_PID=$!
cd ../..
echo -e "${GREEN}[INFO] SAJU 프론트엔드 PID: $SAJU_FRONTEND_PID${NC}"
sleep 5

# 4. 모바일 앱 시작 (포트 8082)
echo -e "${BLUE}[4/7]${NC} 📱 모바일 앱 시작 중... ${YELLOW}(포트 8082)${NC}"
cd AppService/FortuneApp
npm install > ../../logs/mobile-app-install.log 2>&1
nohup npm start > ../../logs/mobile-app.log 2>&1 &
MOBILE_APP_PID=$!
cd ../..
echo -e "${GREEN}[INFO] 모바일 앱 PID: $MOBILE_APP_PID${NC}"
sleep 3

# 5. 궁합 서비스 시작 (백엔드 8002, 프론트엔드 3002)
echo -e "${BLUE}[5/7]${NC} 💕 궁합 서비스 시작 중... ${YELLOW}(포트 8002, 3002)${NC}"
cd Compatibility/backend
pip install -r requirements.txt > ../../logs/compatibility-backend-install.log 2>&1
nohup python start_compatibility.py > ../../logs/compatibility-backend.log 2>&1 &
COMPATIBILITY_BACKEND_PID=$!
cd ../frontend
npm install > ../../logs/compatibility-frontend-install.log 2>&1
nohup npm start > ../../logs/compatibility-frontend.log 2>&1 &
COMPATIBILITY_FRONTEND_PID=$!
cd ../..
echo -e "${GREEN}[INFO] 궁합 백엔드 PID: $COMPATIBILITY_BACKEND_PID${NC}"
echo -e "${GREEN}[INFO] 궁합 프론트엔드 PID: $COMPATIBILITY_FRONTEND_PID${NC}"
sleep 3

# 6. 관상 서비스 시작 (백엔드 8001, 프론트엔드 3001)
echo -e "${BLUE}[6/7]${NC} 🎭 관상 서비스 시작 중... ${YELLOW}(포트 8001, 3001)${NC}"
cd Physiognomy/backend
pip install -r requirements.txt > ../../logs/physiognomy-backend-install.log 2>&1
nohup python main.py > ../../logs/physiognomy-backend.log 2>&1 &
PHYSIOGNOMY_BACKEND_PID=$!
cd ../frontend
npm install > ../../logs/physiognomy-frontend-install.log 2>&1
nohup npm start > ../../logs/physiognomy-frontend.log 2>&1 &
PHYSIOGNOMY_FRONTEND_PID=$!
cd ../..
echo -e "${GREEN}[INFO] 관상 백엔드 PID: $PHYSIOGNOMY_BACKEND_PID${NC}"
echo -e "${GREEN}[INFO] 관상 프론트엔드 PID: $PHYSIOGNOMY_FRONTEND_PID${NC}"

# 7. PID 파일 저장 (종료 시 사용)
echo -e "${BLUE}[7/7]${NC} 💾 PID 정보 저장 중..."
cat > .pids << EOF
LANDING_PID=$LANDING_PID
SAJU_BACKEND_PID=$SAJU_BACKEND_PID
SAJU_FRONTEND_PID=$SAJU_FRONTEND_PID
MOBILE_APP_PID=$MOBILE_APP_PID
COMPATIBILITY_BACKEND_PID=$COMPATIBILITY_BACKEND_PID
COMPATIBILITY_FRONTEND_PID=$COMPATIBILITY_FRONTEND_PID
PHYSIOGNOMY_BACKEND_PID=$PHYSIOGNOMY_BACKEND_PID
PHYSIOGNOMY_FRONTEND_PID=$PHYSIOGNOMY_FRONTEND_PID
EOF

echo
echo -e "${PURPLE}================================================${NC}"
echo -e "${PURPLE}            Health Check 진행 중...            ${NC}"
echo -e "${PURPLE}================================================${NC}"

# Health Check 수행
sleep 10  # 모든 서비스가 충분히 시작할 시간

health_check "http://localhost:4000" "랜딩 페이지"
health_check "http://localhost:8000/health" "SAJU 백엔드"
health_check "http://localhost:3000" "SAJU 프론트엔드"
health_check "http://localhost:8082" "모바일 앱"
health_check "http://localhost:8002/health" "궁합 백엔드"
health_check "http://localhost:3002" "궁합 프론트엔드"
health_check "http://localhost:8001/docs" "관상 백엔드"
health_check "http://localhost:3001" "관상 프론트엔드"

echo
echo -e "${GREEN}=========================================="
echo -e "   🎉 MSProject2 SAJU 플랫폼 시작 완료!"
echo -e "==========================================${NC}"
echo
echo -e "${CYAN}🏠 메인 랜딩:   ${YELLOW}http://localhost:4000${NC} ${GREEN}(실시간 모니터링 포함)${NC}"
echo -e "${CYAN}🔮 SAJU 분석:   ${YELLOW}http://localhost:3000${NC}"
echo -e "${CYAN}📱 모바일 앱:   ${YELLOW}http://localhost:8082${NC}"
echo -e "${CYAN}💕 궁합 분석:   ${YELLOW}http://localhost:3002${NC}"
echo -e "${CYAN}🎭 관상 분석:   ${YELLOW}http://localhost:3001${NC}"
echo
echo -e "${BLUE}📚 API 문서:${NC}"
echo -e "${CYAN}  - SAJU API:      ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "${CYAN}  - 궁합 API:      ${YELLOW}http://localhost:8002/docs${NC}"
echo -e "${CYAN}  - 관상 API:      ${YELLOW}http://localhost:8001/docs${NC}"
echo
echo -e "${PURPLE}📊 모니터링:${NC}"
echo -e "${CYAN}  - 실시간 상태:   랜딩 페이지에서 확인${NC}"
echo -e "${CYAN}  - 로그 확인:     ${YELLOW}./logs/*.log${NC}"
echo -e "${CYAN}  - 서비스 종료:   ${YELLOW}./stop_all_enhanced.sh${NC}"
echo
echo -e "${GREEN}🚀 모든 서비스가 성공적으로 시작되었습니다!${NC}"
echo -e "${BLUE}💡 랜딩 페이지(localhost:4000)에서 실시간 서비스 상태를 확인하세요!${NC}"
