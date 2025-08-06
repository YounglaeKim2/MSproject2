// 궁합 분석 관련 타입 정의

export interface PersonInfo {
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: "male" | "female";
  name: string;
}

export interface CompatibilityRequest {
  person1: PersonInfo;
  person2: PersonInfo;
}

export interface CompatibilityScore {
  overall: number;
  love: number;
  marriage: number;
  communication: number;
  values: number;
}

export interface CompatibilityDetail {
  strengths: string[];
  weaknesses: string[];
  advice: string[];
  relationship_tips: string[];
}

export interface CompatibilityData {
  success: boolean;
  person1_name: string;
  person2_name: string;
  compatibility_score: CompatibilityScore;
  analysis_details: CompatibilityDetail;
  summary: string;
  detailed_analysis: string;
  analysis_time: string;
  error?: string;
  message?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
