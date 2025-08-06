import React, { useState } from "react";
import styled from "styled-components";
import {
  PersonInfo,
  CompatibilityRequest,
  CompatibilityData,
} from "../types/compatibility";
import CompatibilityAPI from "../services/api";

const FormContainer = styled.div`
  background: #f8f9fa;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
`;

const Title = styled.h2`
  color: #333;
  margin-bottom: 30px;
  text-align: center;
  font-size: 1.8rem;
`;

const PersonFormSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
`;

const PersonTitle = styled.h3`
  color: #495057;
  margin-bottom: 20px;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const FormRow = styled.div`
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  align-items: center;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 10px;
  }
`;

const Label = styled.label`
  font-weight: 600;
  color: #495057;
  min-width: 80px;
  display: block;

  @media (max-width: 768px) {
    min-width: auto;
    align-self: flex-start;
  }
`;

const Input = styled.input`
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 120px;

  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
  }

  &:invalid {
    border-color: #dc3545;
  }
`;

const Select = styled.select`
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  flex: 1;
  background: white;

  &:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
  }
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
  flex-wrap: wrap;
`;

const Button = styled.button<{ variant?: "primary" | "secondary" }>`
  padding: 15px 30px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;

  ${(props) =>
    props.variant === "primary"
      ? `
    background: linear-gradient(45deg, #007bff, #0056b3);
    color: white;
    
    &:hover:not(:disabled) {
      background: linear-gradient(45deg, #0056b3, #003d82);
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
    }
  `
      : `
    background: #6c757d;
    color: white;
    
    &:hover:not(:disabled) {
      background: #545b62;
    }
  `}

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const LoadingSpinner = styled.div`
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s ease-in-out infinite;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const ErrorMessage = styled.div`
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
`;

interface Props {
  onAnalysisComplete: (result: CompatibilityData) => void;
  onAnalysisStart: () => void;
  onAnalysisEnd: () => void;
  onError: (error: string) => void;
  isLoading: boolean;
}

const CompatibilityForm: React.FC<Props> = ({
  onAnalysisComplete,
  onAnalysisStart,
  onAnalysisEnd,
  onError,
  isLoading,
}) => {
  const [person1, setPerson1] = useState<PersonInfo>({
    name: "김민수",
    year: 1990,
    month: 5,
    day: 15,
    hour: 14,
    gender: "male",
  });

  const [person2, setPerson2] = useState<PersonInfo>({
    name: "이지은",
    year: 1992,
    month: 8,
    day: 20,
    hour: 10,
    gender: "female",
  });

  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const updatePerson1 = (field: keyof PersonInfo, value: any) => {
    setPerson1((prev) => ({ ...prev, [field]: value }));
  };

  const updatePerson2 = (field: keyof PersonInfo, value: any) => {
    setPerson2((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const request: CompatibilityRequest = { person1, person2 };

    // 유효성 검증
    const errors = CompatibilityAPI.validateCompatibilityRequest(request);
    if (errors.length > 0) {
      setValidationErrors(errors);
      return;
    }

    setValidationErrors([]);
    onAnalysisStart();

    try {
      const result = await CompatibilityAPI.analyzeCompatibility(request);
      onAnalysisComplete(result);
    } catch (error: any) {
      onError(error.message || "궁합 분석 중 오류가 발생했습니다.");
    } finally {
      onAnalysisEnd();
    }
  };

  const handleTestConnection = async () => {
    const request: CompatibilityRequest = { person1, person2 };

    try {
      const result = await CompatibilityAPI.testConnection(request);
      alert("SAJU API 연결 테스트 성공!\n" + result.summary);
    } catch (error: any) {
      alert("연결 테스트 실패: " + error.message);
    }
  };

  return (
    <FormContainer>
      <Title>🔮 궁합 분석 정보 입력</Title>

      {validationErrors.length > 0 && (
        <ErrorMessage>
          <h4>⚠️ 입력 오류</h4>
          <ul>
            {validationErrors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </ErrorMessage>
      )}

      <form onSubmit={handleSubmit}>
        {/* 첫 번째 사람 */}
        <PersonFormSection>
          <PersonTitle>👤 첫 번째 사람</PersonTitle>

          <FormRow>
            <Label>이름:</Label>
            <Input
              type="text"
              value={person1.name}
              onChange={(e) => updatePerson1("name", e.target.value)}
              placeholder="이름을 입력하세요"
              required
            />
          </FormRow>

          <FormRow>
            <Label>생년월일:</Label>
            <Input
              type="number"
              value={person1.year}
              onChange={(e) => updatePerson1("year", parseInt(e.target.value))}
              placeholder="년"
              min="1900"
              max="2030"
              required
            />
            <Input
              type="number"
              value={person1.month}
              onChange={(e) => updatePerson1("month", parseInt(e.target.value))}
              placeholder="월"
              min="1"
              max="12"
              required
            />
            <Input
              type="number"
              value={person1.day}
              onChange={(e) => updatePerson1("day", parseInt(e.target.value))}
              placeholder="일"
              min="1"
              max="31"
              required
            />
            <Input
              type="number"
              value={person1.hour}
              onChange={(e) => updatePerson1("hour", parseInt(e.target.value))}
              placeholder="시"
              min="0"
              max="23"
              required
            />
          </FormRow>

          <FormRow>
            <Label>성별:</Label>
            <Select
              value={person1.gender}
              onChange={(e) =>
                updatePerson1("gender", e.target.value as "male" | "female")
              }
              required
            >
              <option value="male">남성</option>
              <option value="female">여성</option>
            </Select>
          </FormRow>
        </PersonFormSection>

        {/* 두 번째 사람 */}
        <PersonFormSection>
          <PersonTitle>👤 두 번째 사람</PersonTitle>

          <FormRow>
            <Label>이름:</Label>
            <Input
              type="text"
              value={person2.name}
              onChange={(e) => updatePerson2("name", e.target.value)}
              placeholder="이름을 입력하세요"
              required
            />
          </FormRow>

          <FormRow>
            <Label>생년월일:</Label>
            <Input
              type="number"
              value={person2.year}
              onChange={(e) => updatePerson2("year", parseInt(e.target.value))}
              placeholder="년"
              min="1900"
              max="2030"
              required
            />
            <Input
              type="number"
              value={person2.month}
              onChange={(e) => updatePerson2("month", parseInt(e.target.value))}
              placeholder="월"
              min="1"
              max="12"
              required
            />
            <Input
              type="number"
              value={person2.day}
              onChange={(e) => updatePerson2("day", parseInt(e.target.value))}
              placeholder="일"
              min="1"
              max="31"
              required
            />
            <Input
              type="number"
              value={person2.hour}
              onChange={(e) => updatePerson2("hour", parseInt(e.target.value))}
              placeholder="시"
              min="0"
              max="23"
              required
            />
          </FormRow>

          <FormRow>
            <Label>성별:</Label>
            <Select
              value={person2.gender}
              onChange={(e) =>
                updatePerson2("gender", e.target.value as "male" | "female")
              }
              required
            >
              <option value="female">여성</option>
              <option value="male">남성</option>
            </Select>
          </FormRow>
        </PersonFormSection>

        <ButtonContainer>
          <Button
            type="button"
            variant="secondary"
            onClick={handleTestConnection}
            disabled={isLoading}
          >
            연결 테스트
          </Button>

          <Button type="submit" variant="primary" disabled={isLoading}>
            {isLoading ? (
              <>
                <LoadingSpinner />
                <span style={{ marginLeft: "10px" }}>분석 중...</span>
              </>
            ) : (
              "궁합 분석 시작"
            )}
          </Button>
        </ButtonContainer>
      </form>
    </FormContainer>
  );
};

export default CompatibilityForm;
