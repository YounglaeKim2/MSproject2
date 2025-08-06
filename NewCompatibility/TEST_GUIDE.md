# 🧪 NewCompatibility 서비스 테스트 가이드

## 📋 테스트 순서

### 1단계: 서버 실행 확인

```bash
# SAJU API 서버 상태 확인 (포트 8000)
curl http://localhost:8000/health

# NewCompatibility 서버 시작
cd c:\workspace\MSproject2\NewCompatibility
start_new_compatibility.bat
```

### 2단계: 웹 브라우저 테스트

1. `test_page.html` 파일을 브라우저에서 열기
2. 자동으로 헬스 체크가 실행됨
3. 각 테스트 버튼을 순서대로 클릭

### 3단계: 커맨드라인 테스트 (Windows PowerShell)

#### 헬스 체크

```powershell
curl http://localhost:8003/health
```

#### 서비스 정보

```powershell
curl http://localhost:8003/info
```

#### SAJU API 연결 테스트

```powershell
$body = @{
    person1 = @{
        year = 1990; month = 5; day = 15; hour = 14
        gender = "male"; name = "김민수"
    }
    person2 = @{
        year = 1992; month = 8; day = 20; hour = 10
        gender = "female"; name = "이지은"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8003/api/v1/compatibility/test" -Method POST -Body $body -ContentType "application/json"
```

#### 실제 궁합 분석

```powershell
$body = @{
    person1 = @{
        year = 1990; month = 5; day = 15; hour = 14
        gender = "male"; name = "김민수"
    }
    person2 = @{
        year = 1992; month = 8; day = 20; hour = 10
        gender = "female"; name = "이지은"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8003/api/v1/compatibility/analyze" -Method POST -Body $body -ContentType "application/json"
```

## 🎯 예상 결과

### 성공적인 헬스 체크

```json
{
  "status": "healthy",
  "service": "NewCompatibility",
  "version": "1.0.0",
  "timestamp": "2025-08-06T...",
  "dependencies": {
    "saju_api": {
      "status": "healthy",
      "saju_api_response": {...}
    }
  }
}
```

### 성공적인 궁합 분석

```json
{
  "success": true,
  "person1_name": "김민수",
  "person2_name": "이지은",
  "compatibility_score": {
    "overall": 75,
    "love": 78,
    "marriage": 72,
    "communication": 80,
    "values": 70
  },
  "analysis_details": {
    "strengths": [...],
    "weaknesses": [...],
    "advice": [...]
  },
  "summary": "김민수님과 이지은님은 좋은 궁합을 가지고 있습니다...",
  "detailed_analysis": "오행 분석... 십성 분석..."
}
```

## 🚨 문제 해결

### SAJU API 연결 실패

```json
{
  "status": "degraded",
  "dependencies": {
    "saju_api": {
      "status": "disconnected",
      "error": "SAJU API 서버에 연결할 수 없습니다"
    }
  }
}
```

**해결**: SAJU API 서버(포트 8000)가 실행 중인지 확인

### NewCompatibility 서버 연결 실패

**해결**:

1. `start_new_compatibility.bat` 실행
2. 포트 8003이 다른 프로세스에서 사용 중인지 확인
3. 의존성 설치: `pip install -r requirements.txt`

## 📊 성능 테스트

### 응답 시간 기준

- 헬스 체크: < 1초
- SAJU 연결 테스트: < 5초
- 궁합 분석: < 10초 (SAJU API 2회 호출 + 계산)

### 동시 요청 테스트

```bash
# 10개의 동시 요청
for i in {1..10}; do
  curl -X POST http://localhost:8003/api/v1/compatibility/test \
    -H "Content-Type: application/json" \
    -d '{"person1":{"year":1990,"month":5,"day":15,"hour":14,"gender":"male","name":"테스트'$i'"},"person2":{"year":1992,"month":8,"day":20,"hour":10,"gender":"female","name":"테스트2"}}' &
done
wait
```

## 📈 테스트 체크리스트

- [ ] SAJU API 서버 실행 중 (포트 8000)
- [ ] NewCompatibility 서버 실행 중 (포트 8003)
- [ ] 헬스 체크 성공 (status: healthy)
- [ ] 서비스 정보 조회 성공
- [ ] SAJU API 연결 테스트 성공
- [ ] 기본 데이터 궁합 분석 성공
- [ ] 커스텀 데이터 궁합 분석 성공
- [ ] 에러 핸들링 테스트 (잘못된 데이터 입력)
- [ ] 응답 시간 기준 충족
- [ ] JSON 응답 구조 검증
