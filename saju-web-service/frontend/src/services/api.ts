import axios from 'axios';
import { BirthInfo, SajuAnalysisResult } from '../types/saju';

// API 기본 설정
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30초 타임아웃
});

// 요청 인터셉터 (로깅)
apiClient.interceptors.request.use(
  (config) => {
    console.log('API 요청:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API 요청 오류:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터 (에러 처리)
apiClient.interceptors.response.use(
  (response) => {
    console.log('API 응답:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API 응답 오류:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// 사주 API 서비스
export const sajuApi = {
  // 완전한 사주 분석
  analyzeSaju: async (birthInfo: BirthInfo): Promise<SajuAnalysisResult> => {
    try {
      const response = await apiClient.post('/api/v1/saju/analyze', birthInfo);
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        '사주 분석 중 오류가 발생했습니다.'
      );
    }
  },

  // 사주팔자만 추출
  getPaljaOnly: async (birthInfo: BirthInfo) => {
    try {
      const params = new URLSearchParams({
        year: birthInfo.year.toString(),
        month: birthInfo.month.toString(),
        day: birthInfo.day.toString(),
        hour: birthInfo.hour.toString(),
        gender: birthInfo.gender,
      });

      const response = await apiClient.get(`/api/v1/saju/palja-only?${params}`);
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        '사주팔자 추출 중 오류가 발생했습니다.'
      );
    }
  },

  // 오행 분석만
  getWuXingOnly: async (birthInfo: BirthInfo) => {
    try {
      const params = new URLSearchParams({
        year: birthInfo.year.toString(),
        month: birthInfo.month.toString(),
        day: birthInfo.day.toString(),
        hour: birthInfo.hour.toString(),
        gender: birthInfo.gender,
      });

      const response = await apiClient.get(`/api/v1/saju/wuxing-only?${params}`);
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        '오행 분석 중 오류가 발생했습니다.'
      );
    }
  },

  // API 상태 확인
  testConnection: async () => {
    try {
      const response = await apiClient.get('/api/v1/saju/test');
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'API 연결 테스트 실패'
      );
    }
  },

  // 서버 헬스 체크
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        '서버 상태 확인 실패'
      );
    }
  }
};

export default apiClient;