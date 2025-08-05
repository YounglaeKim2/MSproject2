/**
 * 네트워크 요청 헬퍼 유틸리티
 * React Native/Expo 환경에서 안정적인 네트워크 요청을 위한 유틸리티
 */

import { Platform } from 'react-native';

// 재시도 가능한 네트워크 요청
export const fetchWithRetry = async (
  url: string,
  options: RequestInit = {},
  maxRetries: number = 3,
  retryDelay: number = 1000
): Promise<Response> => {
  let lastError: Error;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`🌐 네트워크 요청 시도 ${attempt}/${maxRetries}: ${url}`);
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => {
        console.log(`⏰ 요청 타임아웃 (시도 ${attempt})`);
        controller.abort();
      }, 30000); // 30초 타임아웃

      const requestOptions: RequestInit = {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers,
        },
      };

      const response = await fetch(url, requestOptions);
      clearTimeout(timeoutId);

      if (response.ok) {
        console.log(`✅ 네트워크 요청 성공 (시도 ${attempt})`);
        return response;
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      lastError = error as Error;
      console.error(`❌ 네트워크 요청 실패 (시도 ${attempt}):`, lastError.message);

      if (attempt < maxRetries) {
        console.log(`🔄 ${retryDelay}ms 후 재시도...`);
        await new Promise(resolve => setTimeout(resolve, retryDelay));
        retryDelay *= 1.5; // 지수적 백오프
      }
    }
  }

  throw lastError;
};

// 네트워크 연결 테스트
export const testNetworkConnection = async (baseUrl: string): Promise<boolean> => {
  try {
    console.log('🔍 네트워크 연결 테스트 시작...');
    
    const response = await fetchWithRetry(`${baseUrl.replace('/api/v1/saju', '')}/health`, {
      method: 'GET'
    }, 2, 500);
    
    if (response.ok) {
      console.log('✅ 네트워크 연결 성공');
      return true;
    }
    return false;
  } catch (error) {
    console.error('❌ 네트워크 연결 실패:', error);
    return false;
  }
};

// 플랫폼별 네트워크 진단 정보
export const getNetworkDiagnostics = () => {
  return {
    platform: Platform.OS,
    version: Platform.Version,
    isHermes: typeof HermesInternal === 'object' && HermesInternal !== null,
    userAgent_: typeof navigator !== 'undefined' ? navigator.userAgent : 'N/A'
  };
};