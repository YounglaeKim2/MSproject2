/**
 * SAJU API 클라이언트 서비스
 * MSProject2 SAJU 백엔드와 AppService 모바일 앱 연동
 */

import { API_BASE_URL, API_CONFIG } from '../config/api';
import { fetchWithRetry, testNetworkConnection, getNetworkDiagnostics } from '../utils/networkHelper';

// API 기본 설정
const SAJU_API_BASE = API_BASE_URL;

// API 요청 타입 정의
export interface SajuAnalysisRequest {
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: 'male' | 'female';
  name?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * SAJU API 클라이언트 클래스
 */
export class SajuApiService {
  private baseUrl: string;

  constructor(baseUrl: string = SAJU_API_BASE) {
    this.baseUrl = baseUrl;
  }

  /**
   * API 헬스 체크
   */
  async healthCheck(): Promise<ApiResponse<any>> {
    try {
      const healthUrl = `${this.baseUrl.replace('/api/v1/saju', '')}/health`;
      console.log('🏥 헬스 체크 요청:', healthUrl);
      
      const response = await fetchWithRetry(healthUrl, {
        method: 'GET'
      }, 2, 500);

      const data = await response.json();
      console.log('✅ 헬스 체크 성공:', data);
      return { success: true, data };
    } catch (error) {
      console.error('❌ Health check failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * API 테스트 엔드포인트 호출
   */
  async testApi(): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/test`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('API test failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * 기본 사주 분석 API 호출
   */
  async analyzeSaju(request: SajuAnalysisRequest): Promise<ApiResponse<any>> {
    try {
      console.log('🔮 사주 분석 요청:', request);
      console.log('🌐 API URL:', `${this.baseUrl}/analyze`);
      console.log('📱 플랫폼 정보:', getNetworkDiagnostics());
      
      // 먼저 네트워크 연결 테스트
      const isConnected = await testNetworkConnection(this.baseUrl);
      if (!isConnected) {
        throw new Error('서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.');
      }
      
      const response = await fetchWithRetry(`${this.baseUrl}/analyze`, {
        method: 'POST',
        body: JSON.stringify(request)
      });

      const data = await response.json();
      console.log('✅ 사주 분석 성공');
      return { success: true, data };
    } catch (error) {
      console.error('❌ Saju analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * 사주팔자만 조회
   */
  async getPaljaOnly(request: SajuAnalysisRequest): Promise<ApiResponse<any>> {
    try {
      const queryParams = new URLSearchParams({
        year: request.year.toString(),
        month: request.month.toString(),
        day: request.day.toString(),
        hour: request.hour.toString(),
        gender: request.gender,
      });

      const response = await fetch(`${this.baseUrl}/palja-only?${queryParams}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Palja-only analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * 오행 분석만 조회
   */
  async getWuxingOnly(request: SajuAnalysisRequest): Promise<ApiResponse<any>> {
    try {
      const queryParams = new URLSearchParams({
        year: request.year.toString(),
        month: request.month.toString(),
        day: request.day.toString(),
        hour: request.hour.toString(),
        gender: request.gender,
      });

      const response = await fetch(`${this.baseUrl}/wuxing-only?${queryParams}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Wuxing-only analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * Phase 1 확장 운세 분석
   */
  async getExtendedFortune(request: SajuAnalysisRequest): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/extended-fortune`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Extended fortune analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * Phase 2 확장 운세 분석
   */
  async getExtendedFortunePhase2(request: SajuAnalysisRequest): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/extended-fortune-phase2`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Extended fortune Phase 2 analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * 대운 분석
   */
  async getDaeunAnalysis(request: SajuAnalysisRequest): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/daeun`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Daeun analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  /**
   * 세운 분석
   */
  async getSaeunAnalysis(request: SajuAnalysisRequest, targetYear?: number): Promise<ApiResponse<any>> {
    try {
      const queryParams = targetYear ? `?target_year=${targetYear}` : '';
      
      const response = await fetch(`${this.baseUrl}/saeun${queryParams}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Saeun analysis failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }
}

// 싱글톤 인스턴스 생성
export const sajuApi = new SajuApiService();

// 편의 함수들
export const healthCheck = () => sajuApi.healthCheck();
export const testSajuApi = () => sajuApi.testApi();
export const analyzeSaju = (request: SajuAnalysisRequest) => sajuApi.analyzeSaju(request);
export const getPaljaOnly = (request: SajuAnalysisRequest) => sajuApi.getPaljaOnly(request);
export const getWuxingOnly = (request: SajuAnalysisRequest) => sajuApi.getWuxingOnly(request);
export const getExtendedFortune = (request: SajuAnalysisRequest) => sajuApi.getExtendedFortune(request);
export const getExtendedFortunePhase2 = (request: SajuAnalysisRequest) => sajuApi.getExtendedFortunePhase2(request);
export const getDaeunAnalysis = (request: SajuAnalysisRequest) => sajuApi.getDaeunAnalysis(request);
export const getSaeunAnalysis = (request: SajuAnalysisRequest, targetYear?: number) => sajuApi.getSaeunAnalysis(request, targetYear);