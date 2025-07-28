import React, { useState } from 'react';
import styled from 'styled-components';
import { BirthInfo } from '../types/saju';

interface BirthFormProps {
  onSubmit: (birthInfo: BirthInfo) => void;
  loading?: boolean;
}

const BirthForm: React.FC<BirthFormProps> = ({ onSubmit, loading = false }) => {
  const [formData, setFormData] = useState<BirthInfo>({
    year: new Date().getFullYear() - 30,
    month: 1,
    day: 1,
    hour: 12,
    gender: 'male',
    name: ''
  });

  const [errors, setErrors] = useState<Partial<BirthInfo>>({});

  const validateForm = (): boolean => {
    const newErrors: Partial<BirthInfo> = {};

    if (formData.year < 1900 || formData.year > 2100) {
      newErrors.year = 1900;
    }
    if (formData.month < 1 || formData.month > 12) {
      newErrors.month = 1;
    }
    if (formData.day < 1 || formData.day > 31) {
      newErrors.day = 1;
    }
    if (formData.hour < 0 || formData.hour > 23) {
      newErrors.hour = 0;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleInputChange = (field: keyof BirthInfo, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // 에러 클리어
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  const generateYearOptions = () => {
    const currentYear = new Date().getFullYear();
    const years = [];
    for (let year = currentYear; year >= 1900; year--) {
      years.push(year);
    }
    return years;
  };

  const generateDayOptions = () => {
    const daysInMonth = new Date(formData.year, formData.month, 0).getDate();
    const days = [];
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day);
    }
    return days;
  };

  return (
    <FormContainer>
      <FormTitle>사주팔자 분석</FormTitle>
      <FormSubtitle>정확한 출생 정보를 입력해주세요</FormSubtitle>
      
      <Form onSubmit={handleSubmit}>
        <InputGroup>
          <Label>이름 (선택사항)</Label>
          <Input
            type="text"
            value={formData.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            placeholder="이름을 입력하세요"
          />
        </InputGroup>

        <InputRow>
          <InputGroup>
            <Label>출생년도 *</Label>
            <Select
              value={formData.year}
              onChange={(e) => handleInputChange('year', parseInt(e.target.value))}
              error={!!errors.year}
            >
              {generateYearOptions().map(year => (
                <option key={year} value={year}>{year}년</option>
              ))}
            </Select>
            {errors.year && <ErrorText>올바른 년도를 선택해주세요</ErrorText>}
          </InputGroup>

          <InputGroup>
            <Label>출생월 *</Label>
            <Select
              value={formData.month}
              onChange={(e) => handleInputChange('month', parseInt(e.target.value))}
              error={!!errors.month}
            >
              {[...Array(12)].map((_, i) => (
                <option key={i + 1} value={i + 1}>{i + 1}월</option>
              ))}
            </Select>
            {errors.month && <ErrorText>올바른 월을 선택해주세요</ErrorText>}
          </InputGroup>

          <InputGroup>
            <Label>출생일 *</Label>
            <Select
              value={formData.day}
              onChange={(e) => handleInputChange('day', parseInt(e.target.value))}
              error={!!errors.day}
            >
              {generateDayOptions().map(day => (
                <option key={day} value={day}>{day}일</option>
              ))}
            </Select>
            {errors.day && <ErrorText>올바른 일을 선택해주세요</ErrorText>}
          </InputGroup>
        </InputRow>

        <InputRow>
          <InputGroup>
            <Label>출생시간 *</Label>
            <Select
              value={formData.hour}
              onChange={(e) => handleInputChange('hour', parseInt(e.target.value))}
              error={!!errors.hour}
            >
              {[...Array(24)].map((_, i) => (
                <option key={i} value={i}>{i}시 ({i < 12 ? '오전' : '오후'})</option>
              ))}
            </Select>
            {errors.hour && <ErrorText>올바른 시간을 선택해주세요</ErrorText>}
          </InputGroup>

          <InputGroup>
            <Label>성별 *</Label>
            <GenderContainer>
              <GenderButton
                type="button"
                active={formData.gender === 'male'}
                onClick={() => handleInputChange('gender', 'male')}
              >
                남성
              </GenderButton>
              <GenderButton
                type="button"
                active={formData.gender === 'female'}
                onClick={() => handleInputChange('gender', 'female')}
              >
                여성
              </GenderButton>
            </GenderContainer>
          </InputGroup>
        </InputRow>

        <SubmitButton type="submit" disabled={loading}>
          {loading ? '분석 중...' : '사주 분석하기'}
        </SubmitButton>
      </Form>
    </FormContainer>
  );
};

const FormContainer = styled.div`
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
`;

const FormTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const FormSubtitle = styled.p`
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
`;

const InputRow = styled.div`
  display: flex;
  gap: 15px;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const Label = styled.label`
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
`;

const Input = styled.input`
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const Select = styled.select<{ error?: boolean }>`
  padding: 12px 16px;
  border: 2px solid ${props => props.error ? '#ff6b6b' : '#e1e5e9'};
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  transition: all 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: ${props => props.error ? '#ff6b6b' : '#667eea'};
    box-shadow: 0 0 0 3px ${props => props.error ? 'rgba(255, 107, 107, 0.1)' : 'rgba(102, 126, 234, 0.1)'};
  }
`;

const GenderContainer = styled.div`
  display: flex;
  gap: 10px;
`;

const GenderButton = styled.button<{ active: boolean }>`
  flex: 1;
  padding: 12px;
  border: 2px solid ${props => props.active ? '#667eea' : '#e1e5e9'};
  border-radius: 10px;
  background: ${props => props.active ? '#667eea' : 'white'};
  color: ${props => props.active ? 'white' : '#333'};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #667eea;
    background: ${props => props.active ? '#5a6fd8' : '#f8f9ff'};
  }
`;

const ErrorText = styled.span`
  color: #ff6b6b;
  font-size: 0.85rem;
  margin-top: 4px;
`;

const SubmitButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
`;

export default BirthForm;