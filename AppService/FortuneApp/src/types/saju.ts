/**
 * SAJU API 타입 정의
 * MSProject2 SAJU 백엔드 API 응답 구조 정의
 */

// 기본 사주 정보
export interface SajuBirthInfo {
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: 'male' | 'female';
  name?: string;
}

// 사주팔자 구조
export interface SajuPalja {
  year_heavenly: string;   // 년 천간
  year_earthly: string;    // 년 지지
  month_heavenly: string;  // 월 천간
  month_earthly: string;   // 월 지지
  day_heavenly: string;    // 일 천간
  day_earthly: string;     // 일 지지
  hour_heavenly: string;   // 시 천간
  hour_earthly: string;    // 시 지지
}

// 오행 분석
export interface WuxingAnalysis {
  wood: number;    // 목
  fire: number;    // 화
  earth: number;   // 토
  metal: number;   // 금
  water: number;   // 수
  wood_strength: string;   // 목 강도
  fire_strength: string;   // 화 강도
  earth_strength: string;  // 토 강도
  metal_strength: string;  // 금 강도
  water_strength: string;  // 수 강도
  strongest_element: string;  // 가장 강한 오행
  weakest_element: string;    // 가장 약한 오행
}

// 십성 분석
export interface SipseongAnalysis {
  bias_jeonggwan: number;     // 편관
  jeonggwan: number;          // 정관
  bias_jaeseong: number;      // 편재
  jeongjae: number;           // 정재
  siksin: number;             // 식신
  sangkwan: number;           // 상관
  bias_in: number;            // 편인
  jeong_in: number;           // 정인
  bias_gyeon: number;         // 비견
  geop_jae: number;           // 겁재
}

// 기본 분석 결과
export interface BasicAnalysis {
  personality: string;      // 성격 분석
  health: string;          // 건강 분석
  wealth: string;          // 재물운
  relationships: string;   // 인간관계
  career: string;         // 직업운
  strengths: string[];    // 강점
  weaknesses: string[];   // 약점
}

// Phase 1 확장 운세
export interface ExtendedFortunePhase1 {
  love_fortune: {
    current_love_status: string;
    ideal_partner_type: string;
    love_advice: string;
    relationship_timing: string;
    compatibility_tips: string[];
  };
  personality_fortune: {
    core_personality: string;
    hidden_traits: string;
    growth_potential: string;
    social_style: string;
    stress_management: string;
  };
  relationship_fortune: {
    social_compatibility: string;
    leadership_style: string;
    conflict_resolution: string;
    network_expansion: string;
    trust_building: string;
  };
  wealth_fortune: {
    wealth_accumulation: string;
    investment_style: string;
    financial_advice: string;
    income_sources: string;
    spending_habits: string;
  };
}

// Phase 2 확장 운세
export interface ExtendedFortunePhase2 {
  career_fortune: {
    current_job_compatibility: string;
    career_change_timing: string;
    promotion_potential: string;
    skill_development: string;
    work_environment: string;
  };
  health_fortune: {
    physical_health: string;
    mental_health: string;
    disease_prevention: string;
    exercise_recommendations: string;
    dietary_advice: string;
  };
  study_fortune: {
    learning_ability: string;
    exam_luck: string;
    skill_acquisition: string;
    academic_achievement: string;
    knowledge_application: string;
  };
  family_fortune: {
    parent_relationship: string;
    sibling_harmony: string;
    child_planning: string;
    family_gatherings: string;
    generational_conflict: string;
  };
}

// 대운 분석
export interface DaeunPeriod {
  start_age: number;
  end_age: number;
  heavenly_stem: string;
  earthly_branch: string;
  description: string;
  key_events: string[];
  advice: string;
}

export interface DaeunAnalysis {
  periods: DaeunPeriod[];
  current_period: DaeunPeriod;
  next_period: DaeunPeriod;
  overall_trend: string;
}

// 세운 분석
export interface SaeunAnalysis {
  target_year: number;
  yearly_fortune: string;
  monthly_fortunes: {
    month: number;
    fortune: string;
    advice: string;
  }[];
  key_months: number[];
  overall_advice: string;
}

// 전체 사주 분석 결과
export interface SajuAnalysisResult {
  birth_info: SajuBirthInfo;
  palja: SajuPalja;
  wuxing: WuxingAnalysis;
  sipseong: SipseongAnalysis;
  basic_analysis: BasicAnalysis;
  extended_fortune_phase1?: ExtendedFortunePhase1;
  extended_fortune_phase2?: ExtendedFortunePhase2;
  daeun?: DaeunAnalysis;
  saeun?: SaeunAnalysis;
  ai_interpretation?: string;
}

// API 응답 래퍼
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// 오행 강도 매핑
export const WuxingStrengthMap = {
  '매우 약함': 0,
  '약함': 25,
  '보통': 50,
  '강함': 75,
  '매우 강함': 100,
} as const;

// 오행 한글-영문 매핑
export const WuxingNameMap = {
  '목': 'wood',
  '화': 'fire', 
  '토': 'earth',
  '금': 'metal',
  '수': 'water',
} as const;

// 성별 매핑
export const GenderMap = {
  '남자': 'male',
  '여자': 'female',
} as const;