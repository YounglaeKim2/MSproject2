/**
 * API 설정 파일
 * 개발/운영 환경별 API 엔드포인트 관리
 */

import { Platform } from 'react-native';

// 개발 환경 설정
const isDevelopment = __DEV__ || process.env.NODE_ENV === 'development';

// 플랫폼별 호스트 IP 결정
const getApiHost = () => {
  if (!isDevelopment) {
    return 'https://your-domain.com';
  }
  
  // 웹 개발 환경에서는 localhost 사용
  if (Platform.OS === 'web') {
    return 'http://localhost:8000';
  }
  
  // 모바일 플랫폼에서는 네트워크 IP 필요 시 사용 
  // (현재는 웹에서만 실행하므로 localhost 사용)
  return 'http://localhost:8000';
};

// 네트워크 환경별 API 베이스 URL
const API_ENDPOINTS = {
  // 로컬 개발 (웹)
  LOCAL_WEB: 'http://localhost:8000/api/v1/saju',
  
  // 네트워크 개발 (모바일 기기에서 접근)
  NETWORK_DEV: 'http://192.168.219.123:8000/api/v1/saju',
  
  // Android 에뮬레이터용
  ANDROID_EMU: 'http://10.0.2.2:8000/api/v1/saju',
  
  // 운영 환경 (추후 배포 시)
  PRODUCTION: 'https://your-domain.com/api/v1/saju'
};

// 현재 사용할 API 베이스 URL 결정
export const API_BASE_URL = `${getApiHost()}/api/v1/saju`;

// API 설정
export const API_CONFIG = {
  baseUrl: API_BASE_URL,
  timeout: 30000, // 30초 (사주 분석은 시간이 걸림)
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
};

// 디버그 정보 출력
if (isDevelopment) {
  console.log('🔧 API Configuration:', {
    environment: isDevelopment ? 'development' : 'production',
    platform: Platform.OS,
    apiBaseUrl: API_BASE_URL,
    selectedHost: getApiHost(),
    available_endpoints: API_ENDPOINTS
  });
}