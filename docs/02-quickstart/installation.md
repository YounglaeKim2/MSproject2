# 🔧 상세 설치 가이드

> **각 운영체제별 상세 설치 방법 및 환경 구성**

## 🖥️ Windows 설치

### ✅ **필수 소프트웨어 설치**

#### 1️⃣ **Python 3.8+ 설치**

```powershell
# 1. Python 공식 사이트에서 다운로드
# https://www.python.org/downloads/windows/

# 2. 설치 시 중요 옵션
# ✅ "Add Python to PATH" 체크
# ✅ "Install for all users" 체크 (선택)

# 3. 설치 확인
python --version
pip --version
```

#### 2️⃣ **Node.js 18+ 설치**

```powershell
# 1. Node.js 공식 사이트에서 LTS 버전 다운로드
# https://nodejs.org/en/download/

# 2. 기본 설정으로 설치

# 3. 설치 확인
node --version
npm --version
```

#### 3️⃣ **Git 설치**

```powershell
# 1. Git 공식 사이트에서 다운로드
# https://git-scm.com/download/win

# 2. 권장 설정
# - Use Git from the Windows Command Prompt
# - Checkout Windows-style, commit Unix-style line endings
# - Use Windows' default console window

# 3. 설치 확인
git --version
```

#### 4️⃣ **Docker Desktop 설치 (선택사항)**

```powershell
# 1. Docker Desktop 다운로드
# https://www.docker.com/products/docker-desktop

# 2. 설치 후 재부팅

# 3. 설치 확인
docker --version
docker-compose --version
```

### 🚀 **Windows 환경 최적화**

#### PowerShell 실행 정책 설정

```powershell
# 관리자 권한으로 PowerShell 실행 후
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows Defender 예외 설정

```powershell
# 프로젝트 폴더를 실시간 보호 예외에 추가
# Windows Defender > 바이러스 및 위협 방지 > 설정 관리 > 예외 추가
# C:\workspace\MSproject2 폴더 추가
```

---

## 🍎 macOS 설치

### ✅ **필수 소프트웨어 설치**

#### 1️⃣ **Homebrew 설치**

```bash
# 1. Homebrew 설치 (패키지 매니저)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. PATH 추가 (M1/M2 Mac의 경우)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### 2️⃣ **Python 설치**

```bash
# 1. Python 설치
brew install python@3.11

# 2. 심볼릭 링크 생성
brew link python@3.11

# 3. 설치 확인
python3 --version
pip3 --version
```

#### 3️⃣ **Node.js 설치**

```bash
# 1. Node.js 설치
brew install node

# 2. 설치 확인
node --version
npm --version
```

#### 4️⃣ **Git 설치**

```bash
# 1. Git 설치 (대부분 이미 설치됨)
brew install git

# 2. 설치 확인
git --version
```

#### 5️⃣ **Docker Desktop 설치**

```bash
# 1. Docker Desktop 다운로드 및 설치
# https://www.docker.com/products/docker-desktop

# 2. 설치 확인
docker --version
docker-compose --version
```

### 🔧 **macOS 환경 최적화**

#### Xcode Command Line Tools 설치

```bash
# 개발 도구 설치 (일부 Python 패키지 컴파일 시 필요)
xcode-select --install
```

---

## 🐧 Linux (Ubuntu) 설치

### ✅ **필수 소프트웨어 설치**

#### 1️⃣ **시스템 업데이트**

```bash
# 1. 패키지 목록 업데이트
sudo apt update && sudo apt upgrade -y

# 2. 기본 개발 도구 설치
sudo apt install -y build-essential curl wget git
```

#### 2️⃣ **Python 설치**

```bash
# 1. Python 3.9+ 설치
sudo apt install -y python3 python3-pip python3-venv

# 2. 심볼릭 링크 생성
sudo ln -sf /usr/bin/python3 /usr/bin/python

# 3. 설치 확인
python --version
pip3 --version
```

#### 3️⃣ **Node.js 설치**

```bash
# 1. NodeSource 리포지토리 추가
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# 2. Node.js 설치
sudo apt install -y nodejs

# 3. 설치 확인
node --version
npm --version
```

#### 4️⃣ **Docker 설치**

```bash
# 1. Docker 공식 GPG 키 추가
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 2. Docker 리포지토리 추가
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 3. Docker 설치
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 4. 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 5. 재로그인 후 설치 확인
docker --version
docker compose version
```

---

## 🔐 개발 환경 보안 설정

### 🔑 **Git 설정**

```bash
# 전역 Git 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# SSH 키 생성 (GitHub 연동 시)
ssh-keygen -t ed25519 -C "your.email@example.com"
```

### 🛡️ **환경 변수 설정**

#### Windows (.env 파일)

```powershell
# 프로젝트 루트에 .env 파일 생성
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "DB_PATH=./manseryukDB/DB/manseryuk.db" >> .env
```

#### macOS/Linux

```bash
# 프로젝트 루트에 .env 파일 생성
cat > .env << EOF
GOOGLE_API_KEY=your_api_key_here
DB_PATH=./manseryukDB/DB/manseryuk.db
EOF
```

---

## 🧪 설치 검증

### ✅ **전체 환경 확인 스크립트**

#### Windows (PowerShell)

```powershell
# 환경 확인 스크립트 실행
Write-Host "=== MSProject2 환경 확인 ===" -ForegroundColor Green

# Python 확인
$pythonVersion = python --version 2>&1
Write-Host "Python: $pythonVersion" -ForegroundColor Yellow

# Node.js 확인
$nodeVersion = node --version
Write-Host "Node.js: $nodeVersion" -ForegroundColor Yellow

# Git 확인
$gitVersion = git --version
Write-Host "Git: $gitVersion" -ForegroundColor Yellow

# Docker 확인 (선택사항)
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "Docker: $dockerVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Docker: Not installed (optional)" -ForegroundColor Gray
}

Write-Host "=== 환경 확인 완료 ===" -ForegroundColor Green
```

#### macOS/Linux

```bash
#!/bin/bash
echo "=== MSProject2 환경 확인 ==="

# Python 확인
echo "Python: $(python3 --version 2>&1)"

# Node.js 확인
echo "Node.js: $(node --version)"

# Git 확인
echo "Git: $(git --version)"

# Docker 확인 (선택사항)
if command -v docker &> /dev/null; then
    echo "Docker: $(docker --version)"
else
    echo "Docker: Not installed (optional)"
fi

echo "=== 환경 확인 완료 ==="
```

### 🔍 **개별 서비스 확인**

```bash
# 1. 프로젝트 클론
git clone https://github.com/YounglaeKim2/MSproject2.git
cd MSproject2

# 2. SAJU 백엔드 의존성 확인
cd SAJU/backend
pip install -r requirements.txt
python -c "import fastapi, uvicorn; print('SAJU Backend: OK')"

# 3. SAJU 프론트엔드 의존성 확인
cd ../../SAJU/frontend
npm install
npm run build
echo "SAJU Frontend: OK"

# 4. NewCompatibility 확인
cd ../../NewCompatibility/backend
pip install -r requirements.txt
echo "NewCompatibility: OK"

# 5. 모바일 앱 확인
cd ../../AppService/FortuneApp
npm install
echo "Mobile App: OK"
```

---

## 🚨 일반적인 설치 문제 해결

### ❌ **Python 관련 문제**

<details>
<summary><strong>Python이 PATH에 없는 경우</strong></summary>

**Windows:**
```powershell
# 1. Python 설치 경로 확인
where python

# 2. 환경 변수 수동 추가
# 제어판 > 시스템 > 고급 시스템 설정 > 환경 변수
# Path에 Python 설치 경로 추가
```

**macOS/Linux:**
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export PATH="/usr/local/bin/python3:$PATH"
source ~/.bashrc  # 또는 ~/.zshrc
```

</details>

<details>
<summary><strong>pip 설치 실패</strong></summary>

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 관리자 권한으로 설치 (Windows)
python -m pip install --user package_name

# 캐시 삭제 후 재설치
pip cache purge
pip install -r requirements.txt
```

</details>

### ❌ **Node.js 관련 문제**

<details>
<summary><strong>npm 권한 문제 (macOS/Linux)</strong></summary>

```bash
# npm 전역 패키지 디렉토리 변경
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# ~/.bashrc에 추가
export PATH=~/.npm-global/bin:$PATH
source ~/.bashrc
```

</details>

<details>
<summary><strong>Node.js 버전 관리</strong></summary>

```bash
# nvm (Node Version Manager) 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 특정 버전 설치 및 사용
nvm install 18
nvm use 18
nvm alias default 18
```

</details>

### ❌ **Docker 관련 문제**

<details>
<summary><strong>Docker 권한 문제 (Linux)</strong></summary>

```bash
# Docker 그룹에 사용자 추가
sudo usermod -aG docker $USER

# Docker 서비스 시작
sudo systemctl start docker
sudo systemctl enable docker

# 재로그인 후 테스트
docker run hello-world
```

</details>

---

## 🎯 설치 완료 후 다음 단계

설치가 완료되었다면:

1. **[빠른 시작 가이드](README.md)**로 첫 실행
2. **[서비스 가이드](../03-services/)**에서 각 기능 탐색
3. **[API 문서](../04-api/)**에서 개발자 정보 확인

**🎉 완벽한 개발 환경이 구성되었습니다!**