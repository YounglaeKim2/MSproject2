# 🔗 API 문서

> **MSProject2 SAJU의 모든 API 엔드포인트 완전 가이드**

## 🎯 API 개요

MSProject2는 **3개의 독립적인 API 서비스**로 구성되어 있으며, RESTful 설계를 따라 구현되었습니다.

### 🌐 **API 서비스 목록**

| API 서비스 | 포트 | 문서 URL | 상태 | 주요 기능 |
|------------|------|----------|------|-----------|
| **SAJU API** | :8000 | [localhost:8000/docs](http://localhost:8000/docs) | ✅ 운영중 | 사주팔자 분석, 대운, 세운, AI 채팅 |
| **NewCompatibility API** | :8003 | [localhost:8003/docs](http://localhost:8003/docs) | ✅ 운영중 | 궁합 분석, AI 궁합 채팅 |
| **Physiognomy API** | :8001 | [localhost:8001/docs](http://localhost:8001/docs) | ✅ 운영중 | AI 관상 분석, 부적 생성 |

---

## 📊 빠른 API 테스트

### ✅ **Health Check (모든 서비스)**

```bash
# 모든 API 서비스 상태 확인
curl http://localhost:8000/health  # SAJU API
curl http://localhost:8003/health  # NewCompatibility API  
curl http://localhost:8001/health  # Physiognomy API
```

### 🔮 **SAJU API 빠른 테스트**

```bash
# 기본 사주 분석
curl -X POST "http://localhost:8000/api/v1/saju/analyze" \
-H "Content-Type: application/json" \
-d '{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "gender": "male",
  "name": "홍길동"
}'
```

### 💕 **NewCompatibility API 빠른 테스트**

```bash
# 궁합 분석
curl -X POST "http://localhost:8003/api/v1/compatibility/analyze" \
-H "Content-Type: application/json" \
-d '{
  "person1": {"year": 1990, "month": 5, "day": 15, "hour": 14, "gender": "male"},
  "person2": {"year": 1992, "month": 8, "day": 22, "hour": 10, "gender": "female"}
}'
```

### 🎭 **Physiognomy API 빠른 테스트**

```bash
# 이미지 업로드를 통한 관상 분석
curl -X POST "http://localhost:8001/analyze" \
-F "file=@/path/to/your/image.jpg"
```

---

## 🔮 SAJU API 상세

### 📡 **엔드포인트 목록**

| 메서드 | 엔드포인트 | 기능 | 응답 시간 |
|--------|------------|------|-----------|
| `POST` | `/api/v1/saju/analyze` | 완전한 사주 분석 (37개 메서드) | ~3초 |
| `POST` | `/api/v1/saju/daeun` | 대운 분석 (10년 주기) | ~2초 |
| `POST` | `/api/v1/saju/saeun` | 세운 분석 (연간/월별) | ~2초 |
| `GET` | `/api/v1/saju/palja-only` | 사주팔자만 조회 | ~1초 |
| `GET` | `/api/v1/saju/wuxing-only` | 오행 분석만 조회 | ~1초 |
| `POST` | `/api/v1/saju/ai-chat` | AI 대화형 해석 | ~5초 |
| `POST` | `/api/v1/saju/suggested-questions` | AI 예상 질문 생성 | ~3초 |
| `GET` | `/health` | 헬스 체크 | ~100ms |

### 📝 **요청 데이터 모델**

```typescript
interface BirthInfo {
  year: number;          // 1900-2100
  month: number;         // 1-12
  day: number;          // 1-31
  hour: number;         // 0-23
  gender: "male" | "female";
  name?: string;        // 선택사항
}
```

### 📊 **응답 데이터 구조**

<details>
<summary><strong>📋 완전한 사주 분석 응답 구조</strong></summary>

```json
{
  "basic_info": {
    "사주팔자": "경오년 신사월 경신일 계미시",
    "일주": "경신",
    "나이": 33,
    "계절": "늦봄"
  },
  "wuxing_balance": {
    "오행_점수": {"금": 3, "목": 1, "수": 2, "화": 2, "토": 2},
    "균형_점수": 89.6,
    "성격_유형": "성장형",
    "설명": "오행 균형이 좋은 편입니다..."
  },
  "sipsung_analysis": {
    "십성_분포": {"비견": 2, "겁재": 1, "식신": 0, ...},
    "주요_십성": "정관",
    "특징": "리더십이 강하고 책임감이 뛰어남"
  },
  "personality_traits": {
    "핵심_성격": ["신중함", "책임감", "완벽주의"],
    "대인관계": "신뢰받는 타입",
    "의사결정": "신중하고 계획적"
  },
  "extended_fortune": {
    "연애운": {"점수": 85, "해석": "하반기 좋은 인연 기대"},
    "재물운": {"점수": 78, "해석": "투자보다는 저축 중심으로"},
    "건강운": {"점수": 82, "해석": "전반적으로 양호, 소화기 주의"},
    "직업운": {"점수": 88, "해석": "승진이나 이직 기회 있음"},
    // ... 8개 확장운세
  },
  "recommendations": {
    "행운의_색상": ["금색", "흰색", "은색"],
    "행운의_방향": ["서쪽", "서북쪽"], 
    "추천_직업": ["관리직", "금융업", "법무직"],
    "건강_관리법": ["규칙적인 운동", "소화기 관리"]
  }
}
```

</details>

---

## 💕 NewCompatibility API 상세

### 📡 **엔드포인트 목록**

| 메서드 | 엔드포인트 | 기능 | 응답 시간 |
|--------|------------|------|-----------|
| `POST` | `/api/v1/compatibility/analyze` | 궁합 분석 | ~5초 |
| `POST` | `/api/v1/compatibility/ai-chat` | AI 궁합 채팅 | ~5초 |
| `POST` | `/api/v1/compatibility/suggested-questions` | AI 질문 생성 | ~3초 |
| `POST` | `/api/v1/compatibility/test` | 연결 테스트 | ~1초 |
| `GET` | `/health` | 헬스 체크 | ~100ms |

### 📝 **요청 데이터 모델**

```typescript
interface CompatibilityRequest {
  person1: BirthInfo;
  person2: BirthInfo;
}
```

### 📊 **궁합 분석 응답**

```json
{
  "compatibility_score": {
    "overall": 83.5,
    "wuxing_harmony": 85,
    "sipsung_match": 82,
    "personality_fit": 84
  },
  "detailed_analysis": {
    "오행_상성": {
      "person1_dominant": "금",
      "person2_dominant": "수", 
      "relationship": "상생",
      "description": "금생수로 서로 도움이 되는 관계"
    },
    "십성_매칭": {
      "compatibility_type": "조화형",
      "strengths": ["서로 보완", "신뢰 관계"],
      "challenges": ["의견 차이", "속도 차이"]
    }
  },
  "relationship_advice": {
    "communication_tips": ["감정 표현 늘리기", "경청하기"],
    "growth_areas": ["인내심 기르기", "타협점 찾기"],
    "warning_periods": ["2024년 7-8월", "2025년 2-3월"]
  }
}
```

---

## 🎭 Physiognomy API 상세

### 📡 **엔드포인트 목록**

| 메서드 | 엔드포인트 | 기능 | 응답 시간 |
|--------|------------|------|-----------|
| `POST` | `/analyze` | 관상 분석 | ~10초 |
| `POST` | `/generate-charm/` | 행운의 부적 생성 | ~3초 |
| `GET` | `/static/amulets/{filename}` | 부적 이미지 다운로드 | ~100ms |
| `GET` | `/health` | 헬스 체크 | ~100ms |

### 📝 **이미지 업로드 요청**

```bash
# multipart/form-data 형식
curl -X POST "http://localhost:8001/analyze" \
-F "file=@image.jpg" \
-F "additional_info=관상 분석 요청"
```

### 📊 **관상 분석 응답**

```json
{
  "face_analysis": {
    "landmarks": {
      "total_points": 468,
      "key_features": {
        "eyes": {"size": "중간", "shape": "아몬드형"},
        "nose": {"height": "보통", "bridge": "직선형"},
        "mouth": {"size": "적당", "shape": "일자형"},
        "face_shape": "타원형"
      }
    },
    "physiognomy_reading": {
      "personality": ["신중함", "책임감", "리더십"],
      "fortune": {
        "career": "관리직이나 전문직에 적합",
        "wealth": "중년 이후 재물운 상승",
        "health": "전반적으로 건강, 스트레스 주의",
        "relationships": "신뢰받는 성격으로 좋은 인간관계"
      }
    }
  },
  "lucky_charm": {
    "image_url": "/static/amulets/charm_20250807123456.jpg",
    "description": "개인 맞춤형 행운의 부적",
    "instructions": "지갑이나 가방에 소지하세요"
  }
}
```

---

## 🔧 API 인증 및 보안

### 🔐 **현재 보안 정책**

- **인증**: 현재 인증 없이 사용 가능 (개발/데모 환경)
- **CORS**: 허용된 도메인에서만 접근 가능
- **Rate Limiting**: API 남용 방지 (분당 60회)
- **입력 검증**: Pydantic을 통한 데이터 검증

### 🚀 **프로덕션 보안 계획**

```python
# 향후 API 키 인증 예정
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
```

---

## 📊 에러 코드 및 처리

### ❌ **표준 에러 응답**

```json
{
  "error": true,
  "message": "에러 설명",
  "code": "ERROR_CODE",
  "details": {
    "field": "year",
    "issue": "1900-2100 범위를 벗어남"
  }
}
```

### 🔍 **일반적인 에러 코드**

| 코드 | 메시지 | 해결 방법 |
|------|--------|-----------|
| `INVALID_DATE` | 잘못된 날짜 | 유효한 날짜 확인 |
| `MISSING_FIELD` | 필수 필드 누락 | 모든 필수 필드 입력 |
| `DB_ERROR` | 데이터베이스 오류 | 잠시 후 재시도 |
| `AI_TIMEOUT` | AI 응답 시간 초과 | AI 없이 기본 분석 제공 |
| `FILE_TOO_LARGE` | 파일 크기 초과 | 10MB 이하 이미지 사용 |

---

## 🧪 개발자 테스트 도구

### 📋 **Postman Collection**

```json
{
  "info": {"name": "MSProject2 SAJU API"},
  "item": [
    {
      "name": "SAJU 기본 분석",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/saju/analyze",
        "body": {
          "raw": "{\"year\":1990,\"month\":5,\"day\":15,\"hour\":14,\"gender\":\"male\"}"
        }
      }
    }
  ]
}
```

### 🔧 **Python SDK 예시**

```python
import requests

class SajuAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def analyze(self, birth_info):
        response = requests.post(
            f"{self.base_url}/api/v1/saju/analyze",
            json=birth_info
        )
        return response.json()
    
    def ai_chat(self, question, context):
        response = requests.post(
            f"{self.base_url}/api/v1/saju/ai-chat",
            json={"question": question, "context": context}
        )
        return response.json()

# 사용 예시
api = SajuAPI()
result = api.analyze({
    "year": 1990,
    "month": 5, 
    "day": 15,
    "hour": 14,
    "gender": "male"
})
```

### 📱 **JavaScript/TypeScript SDK**

```typescript
class SajuAPIClient {
  constructor(private baseUrl = 'http://localhost:8000') {}

  async analyze(birthInfo: BirthInfo): Promise<SajuResult> {
    const response = await fetch(`${this.baseUrl}/api/v1/saju/analyze`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(birthInfo)
    });
    return response.json();
  }

  async aiChat(question: string, context: any): Promise<AIChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/saju/ai-chat`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question, context})
    });
    return response.json();
  }
}
```

---

## 📈 API 성능 및 제한사항

### ⚡ **성능 지표**

| API | 평균 응답시간 | 최대 동시 요청 | 처리량 |
|-----|---------------|----------------|--------|
| SAJU 기본 분석 | 2-3초 | 50개 | 1000/시간 |
| AI 채팅 | 3-8초 | 20개 | 300/시간 |
| 궁합 분석 | 4-6초 | 30개 | 500/시간 |
| 관상 분석 | 8-15초 | 10개 | 100/시간 |

### 🚨 **사용 제한**

- **요청 크기**: 최대 10MB (이미지 업로드)
- **Rate Limit**: 분당 60회, 시간당 1000회
- **동시 연결**: 서비스별 최대 100개
- **AI 타임아웃**: 30초 (Gemini API)

---

## 🔄 API 버전 관리

### 📊 **현재 버전: v1**

- **안정성**: 프로덕션 사용 가능
- **호환성**: 하위 호환성 보장
- **지원 기간**: 최소 2년

### 🚀 **향후 계획**

- **v1.1**: 출생지 기반 시차 적용
- **v1.2**: 음력 날짜 지원
- **v2.0**: GraphQL 지원, 웹소켓 실시간 업데이트

---

## 📚 추가 자료

### 🔗 **관련 문서**
- **[서비스 가이드](../03-services/)**: 각 서비스 상세 기능
- **[개발 가이드](../05-development/)**: 로컬 개발 및 커스터마이징

### 🛠️ **개발자 지원**
- **Swagger UI**: 각 API의 `/docs` 엔드포인트에서 대화형 문서
- **OpenAPI Spec**: JSON/YAML 형식의 API 명세서
- **예제 코드**: Python, JavaScript, cURL 예시 제공

---

**🎉 MSProject2 SAJU의 강력한 API를 통해 다양한 애플리케이션을 구축하세요!**

_정확한 73,442개 만세력 데이터와 최신 AI 기술이 결합된 완전한 명리학 API입니다._