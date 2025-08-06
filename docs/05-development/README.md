# 🛠️ 개발 가이드

> **MSProject2 SAJU 개발자를 위한 완전한 개발 가이드**

## 👨‍💻 개발자 시작하기

### 🎯 **개발 환경 구성**

```bash
# 1. 프로젝트 클론
git clone https://github.com/YounglaeKim2/MSproject2.git
cd MSproject2

# 2. 각 서비스별 개발 환경 설정
# SAJU Backend
cd SAJU/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# SAJU Frontend
cd ../frontend
npm install

# NewCompatibility
cd ../../NewCompatibility/backend
pip install -r requirements.txt
cd ../frontend
npm install

# Mobile App
cd ../../AppService/FortuneApp
npm install
```

### 🔧 **개발 서버 실행**

```bash
# 각각 별도 터미널에서 실행

# SAJU API (터미널 1)
cd SAJU/backend
uvicorn app.main:app --reload --port 8000

# SAJU Frontend (터미널 2)
cd SAJU/frontend
npm start

# NewCompatibility API (터미널 3)
cd NewCompatibility/backend
uvicorn app.main:app --reload --port 8003

# NewCompatibility Frontend (터미널 4)
cd NewCompatibility/frontend
npm start
```

---

## 🏗️ 프로젝트 구조 이해

### 📁 **전체 디렉토리 구조**

```
MSProject2/
├── 🏠 landing/                    # 랜딩 페이지 (포트 4000)
├── 🔮 SAJU/                       # 핵심 사주 서비스
│   ├── backend/                   # FastAPI (포트 8000)
│   ├── frontend/                  # React (포트 3000)
│   └── manseryukDB/              # 만세력 데이터베이스
├── 📱 AppService/                 # 모바일 앱 (포트 8082)
├── 💕 NewCompatibility/           # 궁합 서비스
│   ├── backend/                   # FastAPI (포트 8003)
│   └── frontend/                  # React (포트 3003)
├── 🎭 Physiognomy/                # 관상 서비스 (포트 8001/3001)
├── 📚 docs_new/                   # 새로운 문서 체계
└── 🔧 scripts/                    # 통합 실행 스크립트
```

### 🧩 **마이크로서비스 아키텍처**

- **독립성**: 각 서비스는 독립적으로 개발/배포/운영
- **확장성**: 필요에 따라 개별 서비스만 확장 가능
- **기술 다양성**: 서비스별 최적 기술 스택 선택

---

## 🔮 SAJU 서비스 개발

### ⚙️ **백엔드 개발**

#### 핵심 파일 구조
```
SAJU/backend/app/
├── main.py                    # FastAPI 애플리케이션
├── api/                       # API 라우터
│   └── saju.py               # 사주 관련 엔드포인트
├── services/                  # 비즈니스 로직
│   ├── saju_analyzer.py      # 37개 분석 메서드
│   └── gemini_ai_interpreter.py  # AI 해석
├── models/                    # 데이터 모델
│   └── saju.py               # Pydantic 모델
└── database/                  # 데이터베이스 연결
    └── connection.py         # DB 커넥션
```

#### 새로운 분석 메서드 추가
```python
# services/saju_analyzer.py
class SajuAnalyzer:
    def get_new_analysis_method(self, palja_info):
        """새로운 분석 메서드 추가"""
        
        # 1. 필요한 데이터 추출
        day_stem = palja_info['day_stem']
        day_branch = palja_info['day_branch']
        
        # 2. 분석 로직 구현
        result = self._calculate_new_analysis(day_stem, day_branch)
        
        # 3. 결과 반환
        return {
            "score": result['score'],
            "interpretation": result['interpretation'],
            "recommendations": result['recommendations']
        }
```

#### API 엔드포인트 추가
```python
# api/saju.py
@app.post("/api/v1/saju/new-endpoint")
async def new_analysis_endpoint(birth_info: BirthInfo):
    try:
        analyzer = SajuAnalyzer(db)
        result = analyzer.get_new_analysis_method(birth_info)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 🖥️ **프론트엔드 개발**

#### React 컴포넌트 구조
```
SAJU/frontend/src/
├── App.tsx                    # 메인 애플리케이션
├── components/                # 재사용 가능 컴포넌트
│   └── AIChatInterface.tsx   # AI 채팅 인터페이스
├── services/                  # API 호출 서비스
├── types/                     # TypeScript 타입 정의
└── utils/                     # 유틸리티 함수
```

#### 새로운 컴포넌트 추가
```typescript
// components/NewAnalysisComponent.tsx
interface NewAnalysisProps {
  analysisData: any;
  onUpdate: (data: any) => void;
}

export const NewAnalysisComponent: React.FC<NewAnalysisProps> = ({
  analysisData,
  onUpdate
}) => {
  return (
    <div>
      {/* 새로운 분석 결과 표시 */}
      <h3>새로운 분석</h3>
      <div>{analysisData.interpretation}</div>
    </div>
  );
};
```

---

## 💕 NewCompatibility 서비스 개발

### 🔧 **궁합 알고리즘 커스터마이징**

```python
# services/compatibility_engine.py
class CompatibilityEngine:
    def calculate_wuxing_compatibility(self, person1_wuxing, person2_wuxing):
        """오행 상성 계산 커스터마이징"""
        
        # 25개 오행 조합별 점수
        compatibility_matrix = {
            ("금", "금"): 75,
            ("금", "수"): 90,  # 금생수
            ("수", "목"): 85,  # 수생목
            # ... 나머지 조합
        }
        
        return compatibility_matrix.get(
            (person1_wuxing, person2_wuxing), 50
        )
    
    def add_custom_compatibility_rule(self, rule_name, calculation_func):
        """새로운 궁합 규칙 추가"""
        self.custom_rules[rule_name] = calculation_func
```

### 🤖 **AI 해석 커스터마이징**

```python
# services/compatibility_ai_interpreter.py
CUSTOM_SYSTEM_PROMPT = """
당신은 전문적인 궁합 상담사입니다.
다음 요소들을 고려하여 궁합을 해석해주세요:
1. 오행 상생상극
2. 십성 매칭  
3. 성격 궁합
4. [새로운 요소 추가]
"""
```

---

## 🎭 Physiognomy 서비스 개발

### 🐳 **Docker 환경 개발**

```dockerfile
# backend/Dockerfile
FROM python:3.9

# MediaPipe 의존성 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 🔍 **관상 분석 로직 추가**

```python
# services/rule_engine.py
class PhysiognomyRules:
    def add_custom_rule(self, feature_name, analysis_func):
        """새로운 관상 분석 규칙 추가"""
        self.rules[feature_name] = analysis_func
    
    def analyze_custom_feature(self, landmarks):
        """사용자 정의 얼굴 특징 분석"""
        # 468개 랜드마크에서 특정 특징 추출
        feature_points = self.extract_feature_points(landmarks)
        
        # 분석 로직 실행
        analysis = self.calculate_feature_significance(feature_points)
        
        return {
            "feature_score": analysis.score,
            "interpretation": analysis.meaning,
            "recommendations": analysis.advice
        }
```

---

## 📱 Mobile App 개발

### 🔧 **React Native 개발 환경**

```bash
# 개발 서버 시작
cd AppService/FortuneApp
npx expo start

# iOS 시뮬레이터에서 실행
i

# Android 에뮬레이터에서 실행  
a

# 웹 브라우저에서 실행
w
```

### 📱 **새로운 화면 추가**

```typescript
// screens/NewFeatureScreen.tsx
import React from 'react';
import { View, Text, ScrollView } from 'react-native';

export const NewFeatureScreen: React.FC = () => {
  return (
    <ScrollView>
      <View style={styles.container}>
        <Text style={styles.title}>새로운 기능</Text>
        {/* 새로운 기능 구현 */}
      </View>
    </ScrollView>
  );
};
```

---

## 🔧 개발 도구 및 유틸리티

### 🐛 **디버깅 도구**

```python
# 백엔드 디버깅
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_saju_analysis(birth_info):
    logger.debug(f"분석 시작: {birth_info}")
    # 디버깅 로직
    logger.debug(f"만세력 조회 결과: {palja_data}")
```

```typescript
// 프론트엔드 디버깅
const DEBUG = process.env.NODE_ENV === 'development';

function debugLog(message: string, data?: any) {
  if (DEBUG) {
    console.log(`[DEBUG] ${message}`, data);
  }
}
```

### 🧪 **테스트 작성**

```python
# tests/test_saju_analyzer.py
import pytest
from app.services.saju_analyzer import SajuAnalyzer

def test_basic_analysis():
    analyzer = SajuAnalyzer()
    birth_info = {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 14,
        "gender": "male"
    }
    
    result = analyzer.analyze(birth_info)
    
    assert result is not None
    assert "basic_info" in result
    assert result["basic_info"]["사주팔자"] is not None
```

```typescript
// frontend/src/__tests__/App.test.tsx
import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders saju analysis form', () => {
  render(<App />);
  const birthYearInput = screen.getByLabelText(/생년/i);
  expect(birthYearInput).toBeInTheDocument();
});
```

---

## 📊 성능 최적화

### ⚡ **백엔드 최적화**

```python
# 데이터베이스 연결 풀 설정
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)

# 결과 캐싱
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_saju_analysis(birth_info_hash):
    # 분석 결과 캐싱
    return analyzer.analyze(birth_info)
```

### 🚀 **프론트엔드 최적화**

```typescript
// React 성능 최적화
import { memo, useCallback, useMemo } from 'react';

export const OptimizedComponent = memo(({ data }) => {
  const memoizedValue = useMemo(() => {
    return expensiveCalculation(data);
  }, [data]);

  const handleClick = useCallback(() => {
    // 이벤트 핸들러 최적화
  }, []);

  return <div>{memoizedValue}</div>;
});

// Code Splitting
const LazyComponent = React.lazy(() => import('./LazyComponent'));
```

---

## 🔐 보안 고려사항

### 🛡️ **API 보안**

```python
# CORS 설정
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 입력 검증 강화
from pydantic import validator

class BirthInfo(BaseModel):
    year: int
    
    @validator('year')
    def validate_year(cls, v):
        if not (1900 <= v <= 2100):
            raise ValueError('Year must be between 1900 and 2100')
        return v
```

### 🔒 **환경 변수 관리**

```bash
# .env 파일 (버전 관리에서 제외)
GOOGLE_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./manseryuk.db
SECRET_KEY=your_secret_key
DEBUG=True
```

```python
# 환경 변수 로딩
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is required")
```

---

## 🚀 배포 및 CI/CD

### 🐳 **Docker 컨테이너화**

```yaml
# docker-compose.yml
version: '3.8'

services:
  saju-api:
    build: ./SAJU/backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./manseryuk.db
    volumes:
      - ./SAJU/manseryukDB:/app/manseryukDB

  saju-frontend:
    build: ./SAJU/frontend
    ports:
      - "3000:3000"
    depends_on:
      - saju-api
```

### 🔄 **GitHub Actions (예시)**

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        cd SAJU/backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd SAJU/backend
        pytest tests/
```

---

## 📚 개발자 리소스

### 🔗 **유용한 링크**
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **React 문서**: https://reactjs.org/docs/
- **React Native 문서**: https://reactnative.dev/docs/
- **MediaPipe 문서**: https://mediapipe.dev/

### 🛠️ **추천 개발 도구**
- **IDE**: VS Code, PyCharm
- **API 테스트**: Postman, Insomnia
- **데이터베이스**: DB Browser for SQLite
- **버전 관리**: Git, GitHub Desktop

### 📖 **코딩 컨벤션**
- **Python**: PEP 8
- **TypeScript**: ESLint + Prettier
- **커밋 메시지**: Conventional Commits

---

## 🤝 기여 가이드라인

### 🔄 **개발 프로세스**

1. **이슈 생성**: GitHub Issues에서 새로운 기능/버그 리포트
2. **브랜치 생성**: `feature/기능명` 또는 `fix/버그명`
3. **개발 및 테스트**: 로컬에서 충분한 테스트
4. **Pull Request**: 상세한 설명과 함께 PR 생성
5. **코드 리뷰**: 팀원들의 리뷰 후 머지

### 📋 **PR 체크리스트**

- [ ] 코드가 컨벤션을 따르는가?
- [ ] 테스트가 추가/수정되었는가?
- [ ] 문서가 업데이트되었는가?
- [ ] Breaking changes가 있는가?
- [ ] 모든 테스트가 통과하는가?

---

**🎉 MSProject2 SAJU 개발에 기여해주셔서 감사합니다!**

_완전한 개발 환경 구성부터 배포까지, 이 가이드가 개발 여정에 도움이 되길 바랍니다._