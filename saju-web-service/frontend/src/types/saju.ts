// 출생 정보 타입
export interface BirthInfo {
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: 'male' | 'female';
  name?: string;
}

// 사주팔자 타입
export interface SajuPalja {
  year_gan: string;
  year_ji: string;
  month_gan: string;
  month_ji: string;
  day_gan: string;
  day_ji: string;
  hour_gan: string;
  hour_ji: string;
}

// 오행 분석 타입
export interface WuXingAnalysis {
  wood: number;
  fire: number;
  earth: number;
  metal: number;
  water: number;
  strength: 'strong' | 'weak';
  use_god: string;
  avoid_god: string;
}

// 십성 분석 타입
export interface TenStarsAnalysis {
  bijian: number;
  겁재: number;
  식신: number;
  상관: number;
  편재: number;
  정재: number;
  편관: number;
  정관: number;
  편인: number;
  정인: number;
}

// 운세 분석 결과 타입들
export interface PersonalityAnalysis {
  basic_nature: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

export interface CareerAnalysis {
  suitable_fields: string[];
  career_tendency: string;
  success_factors: string[];
  cautions: string[];
}

export interface HealthAnalysis {
  strong_organs: string[];
  weak_organs: string[];
  health_advice: string[];
  caution_seasons: string[];
}

export interface RelationshipAnalysis {
  relationship_style: string;
  compatibility: string[];
  social_tendency: string;
  advice: string[];
}

export interface FortuneAnalysis {
  wealth_tendency: string;
  income_style: string;
  investment_advice: string[];
  cautions: string[];
}

// 전체 사주 분석 결과 타입
export interface SajuAnalysisResult {
  palja: SajuPalja;
  wuxing: WuXingAnalysis;
  ten_stars: TenStarsAnalysis;
  personality: PersonalityAnalysis;
  career: CareerAnalysis;
  health: HealthAnalysis;
  relationship: RelationshipAnalysis;
  fortune: FortuneAnalysis;
}

// API 응답 타입
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}