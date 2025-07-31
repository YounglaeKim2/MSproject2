import axios from 'axios';

const API_BASE_URL = 'http://localhost:8002/api/v1/compatibility';

export interface PersonInfo {
  name: string;
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: string;
}

export interface CompatibilityFormData {
  person1: PersonInfo;
  person2: PersonInfo;
}

export interface CompatibilityResult {
  total_score: number;
  grade: string;
  strengths: string[];
  weaknesses: string[];
  advice: string[];
  love_compatibility: number;
  marriage_compatibility: number;
  business_compatibility: number;
  friendship_compatibility: number;
}

export interface CompatibilityApiResponse {
  success: boolean;
  data: CompatibilityResult;
  persons_info: {
    person1: {
      name: string;
      birth_date: string;
      gender: string;
    };
    person2: {
      name: string;
      birth_date: string;
      gender: string;
    };
  };
  timestamp: string;
}

export const compatibilityApi = {
  async analyzeCompatibility(formData: CompatibilityFormData): Promise<CompatibilityApiResponse> {
    const response = await axios.post<CompatibilityApiResponse>(`${API_BASE_URL}/analyze`, formData);
    return response.data;
  },

  async testConnection(): Promise<any> {
    const response = await axios.get(`${API_BASE_URL}/test`);
    return response.data;
  },

  async healthCheck(): Promise<any> {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }
};