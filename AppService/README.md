# 🌟 운세의 문 - 사주 & MBTI 앱

React Native & Expo를 사용한 크로스 플랫폼 모바일 애플리케이션

## 📱 앱 기능

- **🌟 홈 화면**: 신비로운 테마의 메인 화면
- **🔮 사주보기**: 사주 분석 결과 및 오늘의 운세
- **🧠 MBTI 테스트**: 성격 유형 분석 결과

## 🚀 실행 방법

### 1. 의존성 설치

```bash
cd FortuneAppStable
npm install
```

### 2. 앱 실행

```bash
npx expo start --tunnel
```

### 3. 아이폰에서 실행

1. App Store에서 "Expo Go" 앱 다운로드
2. 터미널에 표시된 QR 코드를 카메라로 스캔
3. "Expo Go에서 열기" 탭

## 🛠 기술 스택

- **React Native**: 크로스 플랫폼 모바일 개발
- **Expo**: 빠른 개발 및 배포
- **TypeScript**: 타입 안전성
- **React Navigation**: 화면 네비게이션

## 📂 프로젝트 구조

```
FortuneAppStable/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.tsx      # 홈 화면
│   │   ├── ProfileScreen.tsx   # 사주보기 화면
│   │   └── SettingsScreen.tsx  # MBTI 테스트 화면
│   └── navigation/
│       ├── AppNavigator.tsx    # 네비게이션 설정
│       └── types.ts           # 타입 정의
├── App.tsx                    # 메인 앱 컴포넌트
├── app.json                   # Expo 설정
└── package.json              # 의존성 관리
```

## 🎨 디자인 테마

- **색상 팔레트**: 다크 테마 (#1a1a2e, #16213e, #ffd700, #6a5acd)
- **UI 컴포넌트**: 카드형 레이아웃, 그라데이션 배경
- **이모지 아이콘**: 직관적인 사용자 경험

## 📱 호환성

- **iOS**: Expo Go 앱 필요
- **Android**: Expo Go 앱 필요
- **웹**: 브라우저에서 실행 가능

---

개발자: GitHub Copilot  
날짜: 2025년 7월 7일
