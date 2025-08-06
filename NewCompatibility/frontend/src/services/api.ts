import axios from "axios";
import {
  CompatibilityRequest,
  CompatibilityData,
} from "../types/compatibility";

const API_BASE_URL = "http://localhost:8003";

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초 타임아웃
  headers: {
    "Content-Type": "application/json",
  },
});

// 응답 인터셉터 (에러 처리)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === "ECONNABORTED") {
      throw new Error("요청 시간이 초과되었습니다. 다시 시도해주세요.");
    }
    if (error.response?.status === 500) {
      throw new Error("서버 내부 오류가 발생했습니다.");
    }
    if (error.response?.status === 503) {
      throw new Error(
        "서비스를 사용할 수 없습니다. 잠시 후 다시 시도해주세요."
      );
    }
    if (!error.response) {
      throw new Error("네트워크 연결을 확인해주세요.");
    }
    throw error;
  }
);

export class CompatibilityAPI {
  /**
   * 서버 헬스 체크
   */
  static async checkHealth(): Promise<any> {
    try {
      const response = await apiClient.get("/health");
      return response.data;
    } catch (error) {
      console.error("헬스 체크 실패:", error);
      throw new Error("서버 연결을 확인할 수 없습니다.");
    }
  }

  /**
   * SAJU API 연결 테스트
   */
  static async testConnection(
    request: CompatibilityRequest
  ): Promise<CompatibilityData> {
    try {
      const response = await apiClient.post(
        "/api/v1/compatibility/test",
        request
      );
      return response.data;
    } catch (error: any) {
      console.error("연결 테스트 실패:", error);
      if (error.response?.data?.message) {
        throw new Error(error.response.data.message);
      }
      throw new Error("SAJU API 연결 테스트에 실패했습니다.");
    }
  }

  /**
   * 궁합 분석 실행
   */
  static async analyzeCompatibility(
    request: CompatibilityRequest
  ): Promise<CompatibilityData> {
    try {
      console.log("궁합 분석 요청:", request);

      const response = await apiClient.post(
        "/api/v1/compatibility/analyze",
        request
      );

      console.log("궁합 분석 응답:", response.data);

      if (!response.data.success) {
        throw new Error(response.data.message || "궁합 분석에 실패했습니다.");
      }

      return response.data;
    } catch (error: any) {
      console.error("궁합 분석 실패:", error);

      // 입력 데이터 검증 오류
      if (error.response?.status === 422) {
        throw new Error("입력한 정보가 올바르지 않습니다. 다시 확인해주세요.");
      }

      // API 응답 오류 메시지 사용
      if (error.response?.data?.message) {
        throw new Error(error.response.data.message);
      }

      // 기본 오류 메시지
      throw new Error(
        "궁합 분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
      );
    }
  }

  /**
   * 입력 데이터 유효성 검증
   */
  static validatePersonInfo(person: any): string[] {
    const errors: string[] = [];

    if (!person.name || person.name.trim().length === 0) {
      errors.push("이름을 입력해주세요");
    }

    if (!person.year || person.year < 1900 || person.year > 2030) {
      errors.push("출생년도를 올바르게 입력해주세요 (1900-2030)");
    }

    if (!person.month || person.month < 1 || person.month > 12) {
      errors.push("출생월을 올바르게 입력해주세요 (1-12)");
    }

    if (!person.day || person.day < 1 || person.day > 31) {
      errors.push("출생일을 올바르게 입력해주세요 (1-31)");
    }

    if (person.hour === undefined || person.hour < 0 || person.hour > 23) {
      errors.push("출생시간을 올바르게 입력해주세요 (0-23)");
    }

    if (!person.gender || !["male", "female"].includes(person.gender)) {
      errors.push("성별을 선택해주세요");
    }

    return errors;
  }

  /**
   * 궁합 분석 요청 유효성 검증
   */
  static validateCompatibilityRequest(request: CompatibilityRequest): string[] {
    const errors: string[] = [];

    const person1Errors = this.validatePersonInfo(request.person1).map(
      (err) => `첫 번째 사람: ${err}`
    );
    const person2Errors = this.validatePersonInfo(request.person2).map(
      (err) => `두 번째 사람: ${err}`
    );

    errors.push(...person1Errors, ...person2Errors);

    return errors;
  }
}

export default CompatibilityAPI;
