#!/bin/bash

echo "========================================"
echo "  MSProject2 SAJU - 전체 서비스 중지"
echo "========================================"
echo

echo "[INFO] 모든 관련 프로세스를 찾아서 종료합니다..."
echo

# PID 파일 기반 종료
stop_service_by_pid() {
    local service_name=$1
    local pid_file="logs/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "[INFO] $service_name (PID: $pid) 종료 중..."
            kill -TERM "$pid" 2>/dev/null
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                echo "[WARNING] $service_name 강제 종료 중..."
                kill -KILL "$pid" 2>/dev/null
            fi
        fi
        rm -f "$pid_file"
    fi
}

# 포트 기반 종료
stop_service_by_port() {
    local port=$1
    local service_name=$2
    
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "[INFO] $service_name (포트 $port, PID: $pid) 종료 중..."
        kill -TERM $pid 2>/dev/null
        sleep 2
        # 여전히 실행 중이면 강제 종료
        if kill -0 $pid 2>/dev/null; then
            echo "[WARNING] $service_name 강제 종료 중..."
            kill -KILL $pid 2>/dev/null
        fi
    fi
}

echo "[1/4] PID 파일 기반 서비스 종료 중..."
if [ -d "logs" ]; then
    stop_service_by_pid "main-app"
    stop_service_by_pid "saju-backend"
    stop_service_by_pid "saju-frontend"
    stop_service_by_pid "compatibility-backend"
    stop_service_by_pid "compatibility-frontend"
    stop_service_by_pid "physiognomy"
fi

echo "[2/4] 포트 기반 서비스 종료 중..."
stop_service_by_port 4000 "메인 앱"
stop_service_by_port 3000 "SAJU 프론트엔드"
stop_service_by_port 3002 "궁합 프론트엔드"
stop_service_by_port 8000 "SAJU 백엔드"
stop_service_by_port 8002 "궁합 백엔드"
stop_service_by_port 8001 "관상 백엔드"
stop_service_by_port 3001 "관상 프론트엔드"

echo "[3/4] Docker 컨테이너 정리 중..."
if [ -d "Physiognomy" ]; then
    cd Physiognomy
    docker-compose down >/dev/null 2>&1
    cd ..
fi

# Docker 컨테이너 강제 정리 (프로젝트 관련)
docker ps -q --filter "name=physiognomy" | xargs -r docker stop >/dev/null 2>&1
docker ps -q --filter "name=msproject2" | xargs -r docker stop >/dev/null 2>&1

echo "[4/4] 추가 프로세스 정리 중..."
# Node.js 프로세스 중 MSProject2 관련만 종료
pkill -f "MSProject2" 2>/dev/null
pkill -f "main-app" 2>/dev/null
pkill -f "SAJU" 2>/dev/null
pkill -f "Compatibility" 2>/dev/null
pkill -f "Physiognomy" 2>/dev/null

# 2초 대기
sleep 2

# 포트 사용 여부 최종 확인
echo
echo "[INFO] 포트 사용 여부 최종 확인:"
for port in 4000 3000 3002 8000 8002 8001 3001; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "  포트 $port: 아직 사용 중"
    else
        echo "  포트 $port: 정리 완료"
    fi
done

echo
echo "========================================"
echo "  모든 서비스 중지 완료!"
echo "========================================"
echo
echo "[INFO] 모든 포트가 정리되었습니다."
echo "[INFO] 로그 파일들은 logs/ 디렉토리에 보관됩니다."
echo "[INFO] 필요 시 다시 ./start_all.sh를 실행하세요."
echo