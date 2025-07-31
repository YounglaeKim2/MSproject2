import React from 'react';
import styled from 'styled-components';
import { PersonInfo } from '../../services/compatibilityApi';

interface CompatibilityFormProps {
  person1: PersonInfo;
  person2: PersonInfo;
  loading: boolean;
  onPerson1Change: (field: keyof PersonInfo, value: string | number) => void;
  onPerson2Change: (field: keyof PersonInfo, value: string | number) => void;
  onSubmit: (e: React.FormEvent) => void;
}

const FormContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin-bottom: 30px;
`;

const PersonForm = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 20px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 20px;
  }
`;

const PersonSection = styled.div`
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
`;

const PersonTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.3em;
`;

const FormGroup = styled.div`
  margin-bottom: 15px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #34495e;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
  
  &:focus {
    border-color: #3498db;
    outline: none;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 10px;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
`;

const Button = styled.button`
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
  }
`;

const CompatibilityForm: React.FC<CompatibilityFormProps> = ({
  person1,
  person2,
  loading,
  onPerson1Change,
  onPerson2Change,
  onSubmit
}) => {
  return (
    <FormContainer>
      <form onSubmit={onSubmit}>
        <PersonForm>
          <PersonSection>
            <PersonTitle>첫 번째 사람 💙</PersonTitle>
            <FormGroup>
              <Label>이름</Label>
              <Input
                value={person1.name}
                onChange={(e) => onPerson1Change('name', e.target.value)}
                placeholder="이름을 입력하세요"
                required
              />
            </FormGroup>
            <FormGroup>
              <Label>출생년도</Label>
              <Input
                type="number"
                value={person1.year}
                onChange={(e) => onPerson1Change('year', parseInt(e.target.value) || 1990)}
                min="1900"
                max="2024"
                required
              />
            </FormGroup>
            <FormGroup>
              <Label>출생월</Label>
              <Select
                value={person1.month}
                onChange={(e) => onPerson1Change('month', parseInt(e.target.value))}
                required
              >
                {Array.from({length: 12}, (_, i) => (
                  <option key={i+1} value={i+1}>{i+1}월</option>
                ))}
              </Select>
            </FormGroup>
            <FormGroup>
              <Label>출생일</Label>
              <Input
                type="number"
                value={person1.day}
                onChange={(e) => onPerson1Change('day', parseInt(e.target.value) || 1)}
                min="1"
                max="31"
                required
              />
            </FormGroup>
            <FormGroup>
              <Label>출생시간</Label>
              <Select
                value={person1.hour}
                onChange={(e) => onPerson1Change('hour', parseInt(e.target.value))}
                required
              >
                {Array.from({length: 24}, (_, i) => (
                  <option key={i} value={i}>{i}시</option>
                ))}
              </Select>
            </FormGroup>
            <FormGroup>
              <Label>성별</Label>
              <Select
                value={person1.gender}
                onChange={(e) => onPerson1Change('gender', e.target.value)}
                required
              >
                <option value="male">남성</option>
                <option value="female">여성</option>
              </Select>
            </FormGroup>
          </PersonSection>

          <PersonSection>
            <PersonTitle>두 번째 사람 💖</PersonTitle>
            <FormGroup>
              <Label>이름</Label>
              <Input
                value={person2.name}
                onChange={(e) => onPerson2Change('name', e.target.value)}
                placeholder="이름을 입력하세요"
                required
              />
            </FormGroup>
            <FormGroup>
              <Label>출생년도</Label>
              <Input
                type="number"
                value={person2.year}
                onChange={(e) => onPerson2Change('year', parseInt(e.target.value) || 1990)}
                min="1900"
                max="2024"
                required
              />
            </FormGroup>
            <FormGroup>
              <Label>출생월</Label>
              <Select
                value={person2.month}
                onChange={(e) => onPerson2Change('month', parseInt(e.target.value))}
                required
              >
                {Array.from({length: 12}, (_, i) => (
                  <option key={i+1} value={i+1}>{i+1}월</option>
                ))}
              </Select>
            </FormGroup>
            <FormGroup>
              <Label>출생일</Label>
              <Input
                type="number"
                value={person2.day}
                onChange={(e) => onPerson2Change('day', parseInt(e.target.value) || 1)}
                min="1"
                max="31"
                required
              />
            </FormGroup>
            <FormGroup>
              <Label>출생시간</Label>
              <Select
                value={person2.hour}
                onChange={(e) => onPerson2Change('hour', parseInt(e.target.value))}
                required
              >
                {Array.from({length: 24}, (_, i) => (
                  <option key={i} value={i}>{i}시</option>
                ))}
              </Select>
            </FormGroup>
            <FormGroup>
              <Label>성별</Label>
              <Select
                value={person2.gender}
                onChange={(e) => onPerson2Change('gender', e.target.value)}
                required
              >
                <option value="male">남성</option>
                <option value="female">여성</option>
              </Select>
            </FormGroup>
          </PersonSection>
        </PersonForm>
        
        <Button type="submit" disabled={loading}>
          {loading ? '궁합 분석 중...' : '💕 궁합 분석하기'}
        </Button>
      </form>
    </FormContainer>
  );
};

export default CompatibilityForm;