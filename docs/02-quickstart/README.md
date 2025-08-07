# 🚀 빠른 시작 가이드

> **MSProject2 SAJU를 5분 만에 실행하세요!**

## 📋 시작하기 전에

### ✅ 필수 요구사항

| 요구사항           | 버전   | 설치 확인          | 필수 여부 |
| ------------------ | ------ | ------------------ | --------- |
| **Python**         | 3.8+   | `python --version` | ✅ 필수   |
| **Node.js**        | 14+    | `node --version`   | ✅ 필수   |
| **npm**            | 6+     | `npm --version`    | ✅ 필수   |
| **Git**            | latest | `git --version`    | ✅ 필수   |
| **Docker Desktop** | latest | `docker --version` | 🔶 권장   |

### 💻 지원 운영체제

- ✅ **Windows 10/11** (주 개발 환경)
- ✅ **macOS** 10.15+
- ✅ **Linux** Ubuntu 18.04+

## ⚡ 원클릭 실행 (권장)

### 🎯 **1단계: 프로젝트 클론**

```bash
# 1. 리포지토리 클론
git clone https://github.com/YounglaeKim2/MSproject2.git
cd MSproject2

# 2. 프로젝트 구조 확인
dir  # Windows
ls   # macOS/Linux
```

### 🚀 **2단계: 모든 서비스 한번에 시작**

```bash
# Windows 사용자
./scripts/start_all.bat

# macOS/Linux 사용자 (향후 지원 예정)
# ./scripts/start_all.sh
```

### 🔍 **3단계: 서비스 상태 확인**

```bash
# 실시간 서비스 상태 모니터링
./scripts/check_services.bat
```

**🎉 성공!** 아래 링크들이 모두 열리면 설치 완료입니다:

| 서비스           | URL                                     | 설명                    |
| ---------------- | --------------------------------------- | ----------------------- |
| 🏠 **메인 허브** | [localhost:4000](http://localhost:4000) | 모든 서비스 통합 접근점 |
| 🔮 **사주 분석** | [localhost:3000](http://localhost:3000) | 핵심 사주 서비스        |
| 💕 **궁합 분석** | [localhost:3003](http://localhost:3003) | 궁합 및 AI 채팅         |
| 🎭 **관상 분석** | [localhost:3001](http://localhost:3001) | AI 관상 서비스          |

## 🛑 정지 및 재시작

```bash
# 모든 서비스 정지
./scripts/stop_all.bat

# 개별 서비스 재시작은 수동 실행 가이드 참고
```

---

## 🔧 수동 실행 (상세 제어)

> 개발자나 문제 해결이 필요한 경우 사용하세요.

<details>
<summary><strong>📖 클릭하여 상세 실행 방법 보기</strong></summary>

### 🏠 **1. 메인 랜딩 페이지 실행**

```bash
# 터미널 1
cd landing
python server.py

# ✅ 성공: http://localhost:4000 접속 가능
```

### 🔮 **2. SAJU 서비스 실행**

**백엔드 시작:**

```bash
# 터미널 2
cd SAJU/backend

# 의존성 설치 (최초 1회)
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

# ✅ 성공: http://localhost:8000/docs 에서 API 문서 확인
```

**프론트엔드 시작:**

```bash
# 터미널 3
cd SAJU/frontend

# 의존성 설치 (최초 1회)
npm install

# 개발 서버 시작
npm start

# ✅ 성공: http://localhost:3000 자동 열림
```

### 💕 **3. NewCompatibility 서비스 실행**

```bash
# 터미널 4: 백엔드
cd NewCompatibility
./start_new_compatibility.bat

# 터미널 5: 프론트엔드
./start_frontend.bat

# ✅ 성공: http://localhost:3003 접속 가능
```

### 🎭 **4. Physiognomy 서비스 실행 (Docker 권장)**

```bash
# 터미널 6
cd Physiognomy

# Docker Compose로 실행
docker-compose up --build

# ✅ 성공: http://localhost:3001 접속 가능
```

### 📱 **5. 모바일 앱 실행 (선택사항)**

```bash
# 터미널 7
cd AppService/FortuneApp

# 의존성 설치 (최초 1회)
npm install

# Expo 개발 서버 시작
npx expo start --port 8082 --tunnel
npx expo start --web


# ✅ 성공: Expo DevTools가 열리고 QR코드로 모바일 접속
```

</details>

---

## 🔥 첫 사용 가이드

### 🎯 **1단계: 메인 허브에서 시작**

1. **[localhost:4000](http://localhost:4000)** 접속
2. **"사주 분석 서비스"** 클릭
3. 테마 선택 (기본/다크/라이트/고대비)

### 📝 **2단계: 첫 사주 분석**

1. **[localhost:3000](http://localhost:3000)** 에서 정보 입력

   - 생년월일시 (양력)
   - 성별
   - 이름 (선택)

2. **"사주 분석하기"** 클릭

3. **3초 내 결과** 확인:
   - 사주팔자 기본 정보
   - 오행 균형 점수
   - 성격 유형 분석
   - 8개 확장운세

### 🤖 **3단계: AI 채팅 체험**

1. 분석 결과에서 **"AI와 대화하기"** 클릭
2. 궁금한 점 자유롭게 질문
3. **"예상 질문 받기"** 버튼으로 맞춤 질문 생성

### 💕 **4단계: 궁합 분석 체험**

1. **[localhost:3003](http://localhost:3003)** 접속
2. 두 사람의 정보 입력
3. 궁합 점수 및 AI 해석 확인

### 🎭 **5단계: 관상 분석 체험**

1. **[localhost:3001](http://localhost:3001)** 접속
2. 얼굴 사진 업로드
3. AI 관상 분석 및 행운의 부적 다운로드

---

## 🔧 문제 해결

### ❌ **자주 발생하는 문제들**

<details>
<summary><strong>🐍 Python/pip 관련 오류</strong></summary>

**문제:** `ModuleNotFoundError` 또는 `pip: command not found`

**해결방법:**

```bash
# Python 설치 확인
python --version
python3 --version

# pip 업그레이드
python -m pip install --upgrade pip

# 가상환경 사용 (권장)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 의존성 재설치
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>📦 Node.js/npm 관련 오류</strong></summary>

**문제:** `npm: command not found` 또는 패키지 설치 실패

**해결방법:**

```bash
# Node.js 설치 확인
node --version
npm --version

# npm 캐시 정리
npm cache clean --force

# node_modules 재설치
rm -rf node_modules package-lock.json  # macOS/Linux
rmdir /s node_modules && del package-lock.json  # Windows
npm install
```

</details>

<details>
<summary><strong>🔌 포트 충돌 문제</strong></summary>

**문제:** `Port already in use` 오류

**해결방법:**

```bash
# Windows에서 포트 사용 프로세스 확인 및 종료
netstat -ano | findstr :3000
taskkill /PID <PID번호> /F

# macOS/Linux에서 포트 사용 프로세스 확인 및 종료
lsof -ti:3000
kill -9 <PID번호>
```

</details>

<details>
<summary><strong>🐳 Docker 관련 문제</strong></summary>

**문제:** Docker 컨테이너 실행 실패

**해결방법:**

```bash
# Docker 상태 확인
docker --version
docker-compose --version

# Docker Desktop 재시작
# Windows: Docker Desktop 앱 재시작
# macOS/Linux: sudo systemctl restart docker

# 컨테이너 재빌드
docker-compose down
docker-compose up --build --force-recreate
```

</details>

### 🆘 **추가 도움이 필요한 경우**

1. **[Issues 페이지](https://github.com/YounglaeKim2/MSproject2/issues)**에서 기존 문제 검색
2. **새로운 이슈 생성** 시 다음 정보 포함:

   - 운영체제 및 버전
   - Python, Node.js 버전
   - 에러 메시지 전문
   - 실행한 명령어

3. **개발자 가이드** 참고: [05-development](../05-development/)

---

## 📱 모바일 앱 사용법

### 📲 **iOS/Android 설치**

1. **Expo Go** 앱 설치

   - iOS: [App Store에서 다운로드](https://apps.apple.com/app/expo-go/id982107779)
   - Android: [Google Play에서 다운로드](https://play.google.com/store/apps/details?id=host.exp.exponent)

2. **QR 코드 스캔**

   - 모바일 앱 서버 실행 후 나타나는 QR 코드 스캔
   - 또는 `exp://localhost:8082` 직접 입력

3. **기능 사용**
   - 웹 버전과 동일한 모든 사주 분석 기능
   - 8개 확장운세 카드 지원
   - 모바일 최적화된 UI

---

## 🎊 다음 단계

설치가 완료되었다면 다음 문서들을 참고하세요:

- **[03-services](../03-services/)**: 각 서비스 상세 기능 가이드
- **[04-api](../04-api/)**: API 연동 및 개발자 가이드
- **[05-development](../05-development/)**: 코드 수정 및 개발 가이드

**🎉 축하합니다! MSProject2 SAJU 플랫폼을 성공적으로 실행했습니다!**

---

**⚠️ 문제가 해결되지 않나요?** [📞 지원 요청하기](../05-development/troubleshooting.md)
