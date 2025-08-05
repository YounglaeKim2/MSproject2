#!/bin/bash

echo "=========================================="
echo "   🛑 MSProject2 SAJU 플랫폼 종료 v2.0"
echo "=========================================="
echo "🚀 모든 서비스 정리 중..."
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

# PID 파일 확인
if [ -f ".pids" ]; then
    echo -e "${BLUE}[INFO] PID 파일을 찾았습니다. 저장된 프로세스들을 종료합니다.${NC}"
    source .pids
    
    # 각 프로세스 종료
    processes=(
        "LANDING_PID:랜딩 페이지"
        "SAJU_BACKEND_PID:SAJU 백엔드"
        "SAJU_FRONTEND_PID:SAJU 프론트엔드"
        "MOBILE_APP_PID:모바일 앱"
        "COMPATIBILITY_BACKEND_PID:궁합 백엔드"
        "COMPATIBILITY_FRONTEND_PID:궁합 프론트엔드"
        "PHYSIOGNOMY_BACKEND_PID:관상 백엔드"
        "PHYSIOGNOMY_FRONTEND_PID:관상 프론트엔드"
    )
    
    for process in "${processes[@]}"; do
        pid_var="${process%%:*}"
        service_name="${process##*:}"
        pid="${!pid_var}"
        
        if [ ! -z "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo -e "${YELLOW}[STOP] $service_name (PID: $pid) 종료 중...${NC}"
            kill -TERM "$pid" 2>/dev/null
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                echo -e "${RED}[FORCE] $service_name 강제 종료...${NC}"
                kill -9 "$pid" 2>/dev/null
            else
                echo -e "${GREEN}[SUCCESS] $service_name 정상 종료${NC}"
            fi
        else
            echo -e "${CYAN}[INFO] $service_name 이미 종료됨${NC}"
        fi
    done
    
    rm .pids
    echo -e "${GREEN}[INFO] PID 파일 삭제 완료${NC}"
else
    echo -e "${YELLOW}[WARNING] PID 파일을 찾을 수 없습니다. 포트별 프로세스 종료를 시도합니다.${NC}"
fi

echo
echo -e "${PURPLE}================================================${NC}"
echo -e "${PURPLE}          포트별 프로세스 정리 중...            ${NC}"
echo -e "${PURPLE}================================================${NC}"

# 포트별 프로세스 종료
PORTS=(4000 3000 8000 8082 3002 8002 3001 8001)
SERVICES=("랜딩 페이지" "SAJU Frontend" "SAJU Backend" "모바일 앱" "궁합 Frontend" "궁합 Backend" "관상 Frontend" "관상 Backend")

for i in "${!PORTS[@]}"; do
    port="${PORTS[i]}"
    service="${SERVICES[i]}"
    
    pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}[CLEANUP] 포트 $port ($service) 프로세스 정리 중...${NC}"
        for pid in $pids; do
            echo -e "${CYAN}[KILL] PID $pid 종료...${NC}"
            kill -9 "$pid" 2>/dev/null
        done
        echo -e "${GREEN}[SUCCESS] 포트 $port 정리 완료${NC}"
    else
        echo -e "${GREEN}[INFO] 포트 $port 사용 중인 프로세스 없음${NC}"
    fi
done

echo
echo -e "${PURPLE}================================================${NC}"
echo -e "${PURPLE}            잔여 프로세스 정리 중...            ${NC}"
echo -e "${PURPLE}================================================${NC}"

# Node.js 관련 프로세스 정리
echo -e "${BLUE}[CLEANUP] Node.js 관련 프로세스 정리...${NC}"
pkill -f "node.*start" 2>/dev/null && echo -e "${GREEN}[SUCCESS] Node.js 프로세스 정리 완료${NC}" || echo -e "${CYAN}[INFO] 정리할 Node.js 프로세스 없음${NC}"

# Python 관련 프로세스 정리 (uvicorn, fastapi)
echo -e "${BLUE}[CLEANUP] Python 웹서버 프로세스 정리...${NC}"
pkill -f "uvicorn\|fastapi\|server.py" 2>/dev/null && echo -e "${GREEN}[SUCCESS] Python 웹서버 프로세스 정리 완료${NC}" || echo -e "${CYAN}[INFO] 정리할 Python 웹서버 프로세스 없음${NC}"

# React 개발 서버 정리
echo -e "${BLUE}[CLEANUP] React 개발 서버 정리...${NC}"
pkill -f "react-scripts" 2>/dev/null && echo -e "${GREEN}[SUCCESS] React 개발 서버 정리 완료${NC}" || echo -e "${CYAN}[INFO] 정리할 React 개발 서버 없음${NC}"

echo
echo -e "${PURPLE}================================================${NC}"
echo -e "${PURPLE}            로그 파일 정리 옵션...             ${NC}"
echo -e "${PURPLE}================================================${NC}"

if [ -d "logs" ] && [ "$(ls -A logs)" ]; then
    echo -e "${YELLOW}[OPTION] 로그 파일들이 있습니다:${NC}"
    ls -la logs/
    echo
    echo -e "${CYAN}로그 파일을 삭제하시겠습니까? (y/N): ${NC}"
    read -t 10 -n 1 response
    echo
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf logs/*
        echo -e "${GREEN}[SUCCESS] 로그 파일 삭제 완료${NC}"
    else
        echo -e "${BLUE}[INFO] 로그 파일 유지됨 (./logs/)${NC}"
    fi
else
    echo -e "${CYAN}[INFO] 삭제할 로그 파일 없음${NC}"
fi

echo
echo -e "${GREEN}=========================================="
echo -e "   ✅ MSProject2 SAJU 플랫폼 종료 완료!"
echo -e "==========================================${NC}"
echo
echo -e "${BLUE}📊 정리 완료 내역:${NC}"
echo -e "${CYAN}  ✅ 모든 서비스 프로세스 종료${NC}"
echo -e "${CYAN}  ✅ 포트 8개 (4000,3000,8000,8082,3002,8002,3001,8001) 정리${NC}"
echo -e "${CYAN}  ✅ Node.js/Python 잔여 프로세스 정리${NC}"
echo -e "${CYAN}  ✅ PID 파일 정리${NC}"
echo
echo -e "${PURPLE}🚀 다음번 시작: ./start_all_enhanced.sh${NC}"
echo -e "${YELLOW}💡 빠른 재시작: ./stop_all_enhanced.sh && ./start_all_enhanced.sh${NC}"
