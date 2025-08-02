import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1/saju';

// API 요청 데이터 타입
export interface SajuFormData {
  year: number | '';
  month: number | '';
  day: number | '';
  hour: number | '';
  gender: string;
  name: string;
}

// API 응답 타입들
export interface SajuResult {
  basic_info: any;
  saju_palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  wuxing_analysis: {
    목: number;
    화: number;
    토: number;
    금: number;
    수: number;
    extended_analysis?: {
      balance_analysis: {
        balance_score: number;
        excessive_elements: string[];
        deficient_elements: string[];
        dominant_element: string;
        weakest_element: string;
      };
      personality_analysis: {
        personality_type: string;
        strengths: string[];
        weaknesses: string[];
        dominant_traits: string[];
        advice: string;
      };
      recommendations: {
        colors: string[];
        directions: string[];
        lifestyle: string[];
        foods: string[];
        activities: string[];
        career_advice: string[];
        health_advice: string[];
        relationship_advice: string[];
      };
      wuxing_details: {
        [element: string]: {
          count: number;
          percentage: number;
          strength: string;
          meaning: string;
          characteristics: string[];
        };
      };
    };
  };
  interpretations: {
    personality: string;
    career: string;
    health: string;
    relationships: string;
    wealth: string;
  };
}

export interface DaeunInfo {
  period: string;
  start_age: number;
  end_age: number;
  gan: string;
  ji: string;
  gan_wuxing: string;
  ji_wuxing: string;
  is_current: boolean;
  fortune_level: string;
  characteristics: string[];
  major_events: string[];
  advice: string;
}

export interface DaeunResult {
  basic_info: any;
  palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  daeun_analysis: {
    daeun_start_age: number;
    is_forward: boolean;
    current_age: number;
    daeun_list: DaeunInfo[];
  };
}

export interface SaeunInfo {
  month: number;
  month_name: string;
  gan: string;
  ji: string;
  gan_wuxing: string;
  ji_wuxing: string;
  fortune_score: number;
  fortune_grade: string;
  interaction_analysis: {
    favorable_aspects: string[];
    challenging_aspects: string[];
    recommendations: string[];
  };
  summary: string;
}

export interface SaeunResult {
  basic_info: {
    name: string;
    birth_date: string;
    gender: string;
    target_year: number;
  };
  palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  saeun_analysis: {
    target_year: number;
    yearly_saeun: {
      gan: string;
      ji: string;
      gan_wuxing: string;
      ji_wuxing: string;
      ganzhi: string;
    };
    monthly_saeun: SaeunInfo[];
    annual_score: {
      total_score: number;
      normalized_score: number;
      grade: string;
      yearly_contribution: number;
      monthly_average: number;
    };
    saeun_interaction: {
      yearly: {
        score: number;
        fortune_level: string;
        characteristics: string[];
        opportunities: string[];
        warnings: string[];
      };
      monthly: Array<{
        score: number;
        fortune_level: string;
        characteristics: string[];
        opportunities: string[];
        warnings: string[];
        month: number;
        ganzhi: string;
      }>;
    };
    critical_periods: {
      best_months: Array<{ month: number; score: number; level: string }>;
      caution_months: Array<{ month: number; score: number; level: string }>;
      opportunity_months: Array<{ month: number; opportunities: string[] }>;
    };
    summary: string;
  };
}

// 연애운 결과 타입
export interface LoveFortuneResult {
  success: boolean;
  data: {
    basic_info: {
      name: string;
      birth_date: string;
      gender: string;
    };
    love_fortune_analysis: {
      ideal_type: {
        description: string;
        key_traits: string[];
      };
      love_style: {
        description: string;
        approach: string;
        strengths: string[];
        advice: string;
      };
      marriage_timing: {
        early: number;
        ideal: number;
        late: number;
      };
      monthly_fortune: {
        best_months: string[];
        caution_months: string[];
        advice: string;
      };
    };
  };
}

// API 서비스 함수들
export const sajuApi = {
  // 기본 사주 분석
  async analyzeSaju(formData: SajuFormData): Promise<SajuResult> {
    const response = await axios.post(`${API_BASE_URL}/analyze`, formData);
    return response.data;
  },

  // 대운 분석
  async analyzeDaeun(formData: SajuFormData): Promise<DaeunResult> {
    const response = await axios.post(`${API_BASE_URL}/daeun`, formData);
    return response.data;
  },

  // 세운 분석
  async analyzeSaeun(formData: SajuFormData, targetYear: number): Promise<SaeunResult> {
    const response = await axios.post(`${API_BASE_URL}/saeun?target_year=${targetYear}`, formData);
    return response.data;
  },

  // 연애운 분석
  async analyzeLoveFortune(formData: SajuFormData): Promise<LoveFortuneResult> {
    const response = await axios.post(`${API_BASE_URL}/love-fortune`, formData);
    return response.data;
  },

  // 헬스 체크
  async healthCheck(): Promise<{ status: string }> {
    const response = await axios.get(`${API_BASE_URL.replace('/saju', '')}/health`);
    return response.data;
  }
};

export default sajuApi;