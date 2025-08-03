/**
 * 데이터 매핑 유틸리티
 * UI 입력 데이터를 SAJU API 형식으로 변환
 */

import type { SajuBirthInfo } from '../types/saju';

/**
 * 생년월일 문자열을 파싱하여 연/월/일로 분리
 * @param dateString - "1990-05-15" 형식의 날짜 문자열
 * @returns {year, month, day} 객체 또는 null
 */
export const parseBirthDate = (dateString: string): { year: number; month: number; day: number } | null => {
  // 다양한 형식 지원: 1990-05-15, 1990/05/15, 1990.05.15, 19900515
  const cleanDate = dateString.replace(/[^\d]/g, ''); // 숫자만 추출
  
  if (cleanDate.length === 8) {
    // YYYYMMDD 형식
    const year = parseInt(cleanDate.substring(0, 4));
    const month = parseInt(cleanDate.substring(4, 6));
    const day = parseInt(cleanDate.substring(6, 8));
    
    if (isValidDate(year, month, day)) {
      return { year, month, day };
    }
  }
  
  // 구분자가 있는 형식 처리
  const parts = dateString.split(/[-/.]/);
  if (parts.length === 3) {
    const year = parseInt(parts[0]);
    const month = parseInt(parts[1]);
    const day = parseInt(parts[2]);
    
    if (isValidDate(year, month, day)) {
      return { year, month, day };
    }
  }
  
  return null;
};

/**
 * 시간 문자열을 24시간 형식 숫자로 변환
 * @param timeString - "14", "14시", "오후 2시" 등의 시간 문자열
 * @returns 24시간 형식 숫자 (0-23) 또는 null
 */
export const parseTime = (timeString: string): number | null => {
  // 숫자만 추출
  const numbers = timeString.match(/\d+/g);
  if (!numbers || numbers.length === 0) {
    return null;
  }
  
  let hour = parseInt(numbers[0]);
  
  // 오전/오후 처리
  if (timeString.includes('오후') || timeString.includes('PM')) {
    if (hour !== 12) {
      hour += 12;
    }
  } else if (timeString.includes('오전') || timeString.includes('AM')) {
    if (hour === 12) {
      hour = 0;
    }
  }
  
  // 시간 범위 검증
  if (hour >= 0 && hour <= 23) {
    return hour;
  }
  
  return null;
};

/**
 * 성별 문자열을 API 형식으로 변환
 * @param genderString - "남자", "여자", "남성", "여성" 등
 * @returns "male" | "female" | null
 */
export const parseGender = (genderString: string): 'male' | 'female' | null => {
  const gender = genderString.toLowerCase().trim();
  
  if (gender.includes('남') || gender === 'male' || gender === 'm') {
    return 'male';
  }
  
  if (gender.includes('여') || gender === 'female' || gender === 'f') {
    return 'female';
  }
  
  return null;
};

/**
 * UI 입력 데이터를 SAJU API 요청 형식으로 변환
 * @param birthDate - "1990-05-15" 형식의 생년월일
 * @param birthTime - "14" 형식의 태어난 시간
 * @param gender - "남자" | "여자"
 * @param name - 이름 (선택사항)
 * @returns SajuBirthInfo 객체 또는 null (변환 실패시)
 */
export const convertToSajuRequest = (
  birthDate: string,
  birthTime: string,
  gender: string,
  name?: string
): SajuBirthInfo | null => {
  // 생년월일 파싱
  const parsedDate = parseBirthDate(birthDate);
  if (!parsedDate) {
    return null;
  }
  
  // 시간 파싱
  const parsedTime = parseTime(birthTime);
  if (parsedTime === null) {
    return null;
  }
  
  // 성별 파싱
  const parsedGender = parseGender(gender);
  if (!parsedGender) {
    return null;
  }
  
  return {
    year: parsedDate.year,
    month: parsedDate.month,
    day: parsedDate.day,
    hour: parsedTime,
    gender: parsedGender,
    name: name || undefined,
  };
};

/**
 * 날짜 유효성 검증
 * @param year - 연도
 * @param month - 월 (1-12)
 * @param day - 일 (1-31)
 * @returns 유효한 날짜인지 여부
 */
const isValidDate = (year: number, month: number, day: number): boolean => {
  // 기본 범위 검증
  if (year < 1900 || year > 2100) return false;
  if (month < 1 || month > 12) return false;
  if (day < 1 || day > 31) return false;
  
  // 월별 일수 검증
  const daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  
  // 윤년 검사
  const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
  if (month === 2 && isLeapYear) {
    daysInMonth[1] = 29;
  }
  
  return day <= daysInMonth[month - 1];
};

/**
 * 입력값 검증 및 에러 메시지 생성
 * @param birthDate - 생년월일 문자열
 * @param birthTime - 시간 문자열
 * @param gender - 성별 문자열
 * @returns 에러 메시지 배열 (빈 배열이면 유효)
 */
export const validateInput = (
  birthDate: string,
  birthTime: string,
  gender: string
): string[] => {
  const errors: string[] = [];
  
  // 생년월일 검증
  if (!birthDate.trim()) {
    errors.push('생년월일을 입력해주세요.');
  } else {
    const parsedDate = parseBirthDate(birthDate);
    if (!parsedDate) {
      errors.push('올바른 생년월일 형식을 입력해주세요. (예: 1990-05-15)');
    }
  }
  
  // 시간 검증
  if (!birthTime.trim()) {
    errors.push('태어난 시간을 입력해주세요.');
  } else {
    const parsedTime = parseTime(birthTime);
    if (parsedTime === null) {
      errors.push('올바른 시간을 입력해주세요. (예: 14 또는 오후 2시)');
    }
  }
  
  // 성별 검증
  if (!gender.trim()) {
    errors.push('성별을 선택해주세요.');
  } else {
    const parsedGender = parseGender(gender);
    if (!parsedGender) {
      errors.push('올바른 성별을 선택해주세요.');
    }
  }
  
  return errors;
};

/**
 * 오행 강도를 백분율로 변환
 * @param strength - "매우 약함", "약함", "보통", "강함", "매우 강함"
 * @returns 0-100 사이의 숫자
 */
export const strengthToPercentage = (strength: string): number => {
  const strengthMap: { [key: string]: number } = {
    '매우 약함': 10,
    '약함': 30,
    '보통': 50,
    '강함': 70,
    '매우 강함': 90,
  };
  
  return strengthMap[strength] || 50;
};

/**
 * 오행 색상 매핑
 * @param element - 오행 이름 ("목", "화", "토", "금", "수")
 * @returns 해당 오행의 색상 코드
 */
export const getElementColor = (element: string): string => {
  const colorMap: { [key: string]: string } = {
    '목': '#4CAF50', // 초록색
    '화': '#F44336', // 빨간색
    '토': '#FF9800', // 주황색
    '금': '#FFC107', // 금색
    '수': '#2196F3', // 파란색
  };
  
  return colorMap[element] || '#BE5985';
};