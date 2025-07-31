#!/bin/bash

echo "========================================"
echo "  MSProject2 SAJU - 서비스 상태 확인"
echo "========================================"
echo

# 색상 코드 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 포트별 서비스 상태 확인
echo "[서비스 상태 확인]"

check_port() {
    local port=$1
    local service_name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "  $service_name ($port):     ${GREEN}✅ 실행 중${NC}"
        return 0
    else
        echo -e "  $service_name ($port):     ${RED}❌ 중지됨${NC}"
        return 1
    fi
}

check_port 4000 "메인 앱"
check_port 3000 "사주 UI"
check_port 3002 "궁합 UI"
check_port 3001 "관상 UI"
check_port 8000 "사주 API"
check_port 8002 "궁합 API"
check_port 8001 "관상 API"

echo
echo "[Docker 컨테이너 상태]"
if command -v docker >/dev/null 2>&1; then
    if docker ps --format "table {{.Names}}\t{{.Status}}" --filter "name=physiognomy" 2>/dev/null | grep -q physiognomy; then
        echo -e "  관상학 컨테이너:       ${GREEN}✅ 실행 중${NC}"
        docker ps --format "  {{.Names}}: {{.Status}}" --filter "name=physiognomy"
    else
        echo -e "  관상학 컨테이너:       ${RED}❌ 중지됨 또는 없음${NC}"
    fi
else
    echo -e "  Docker:               ${RED}❌ 설치되지 않음${NC}"
fi

echo
echo "[접속 URL 테스트]"
echo "  테스트를 시작합니다... (5초 정도 소요)"

# URL 접속 테스트
test_url() {
    local url=$1
    local service_name=$2
    
    if curl -s --max-time 3 "$url" >/dev/null 2>&1; then
        echo -e "  $service_name:         ${GREEN}✅ $url${NC}"
    else
        echo -e "  $service_name:         ${RED}❌ 연결 실패${NC}"
    fi
}

test_url "http://localhost:4000" "메인 허브"
test_url "http://localhost:3000" "사주 분석"
test_url "http://localhost:3002" "궁합 분석"
test_url "http://localhost:3001" "관상 분석"

echo
echo "[API 상태 확인]"
test_url "http://localhost:8000/health" "사주 API"
test_url "http://localhost:8002/health" "궁합 API"
test_url "http://localhost:8001/docs" "관상 API"

echo
echo "[시스템 리소스]"
echo "  CPU 사용률:"
if command -v top >/dev/null 2>&1; then
    top -l 1 -n 0 | grep "CPU usage" 2>/dev/null || echo "    확인 불가"
elif command -v htop >/dev/null 2>&1; then
    echo "    htop 명령어로 확인 가능"
else
    echo "    확인 도구 없음"
fi

echo "  메모리 사용률:"
if command -v free >/dev/null 2>&1; then
    free -h | grep Mem | awk '{print "    사용: " $3 "/" $2 " (" int($3/$2*100) "%)"}'
elif [[ "$OSTYPE" == "darwin"* ]]; then
    vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+[^\d])+(\d+)/ and printf("    %s: %.2f MB\n", $1, $2 * $size / 1048576);'
else
    echo "    확인 불가"
fi

echo "  디스크 사용률:"
df -h . | tail -1 | awk '{print "    " $5 " 사용 중 (여유: " $4 ")"}'

echo
echo "[로그 파일 상태]"
if [ -d "logs" ]; then
    echo "  최근 로그 파일:"
    ls -la logs/ 2>/dev/null | tail -n +2 | while read line; do
        echo "    $line"
    done
else
    echo "  로그 디렉토리 없음"
fi

echo
echo "========================================"
echo "  상태 확인 완료!"
echo "========================================"
echo
echo "[도움말]"
echo "  - 서비스 시작: ./start_all.sh"
echo "  - 서비스 중지: ./stop_all.sh"
echo "  - 로그 확인: tail -f logs/[service-name].log"
echo "  - 개별 재시작: kill [PID] 후 해당 서비스 재실행"
echo