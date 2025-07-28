import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
`;

const Title = styled.h1`
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 2.5rem;
`;

const Form = styled.form`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  margin-bottom: 30px;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;

  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  background-color: white;
  
  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

const Button = styled.button`
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ResultContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
`;

const SajuGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin: 20px 0;
  text-align: center;
`;

const SajuPillar = styled.div`
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 2px solid #e1e8ed;
`;

const PillarTitle = styled.div`
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
`;

const Character = styled.div`
  font-size: 24px;
  font-weight: bold;
  margin: 5px 0;
  color: #e74c3c;
`;

const AnalysisSection = styled.div`
  margin: 30px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
`;

const SectionTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
`;

interface FormData {
  year: number | '';
  month: number | '';
  day: number | '';
  hour: number | '';
  gender: string;
  name: string;
}

interface SajuResult {
  basic_info: any;
  saju_palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  wuxing_analysis: any;
  interpretations: {
    personality: string;
    career: string;
    health: string;
    relationships: string;
    wealth: string;
  };
}

function App() {
  const [formData, setFormData] = useState<FormData>({
    year: '',
    month: '',
    day: '',
    hour: '',
    gender: 'male',
    name: ''
  });
  
  const [result, setResult] = useState<SajuResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'year' || name === 'month' || name === 'day' || name === 'hour' 
        ? (value === '' ? '' : parseInt(value))
        : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      console.log('요청 데이터:', formData);
      const response = await axios.post('http://localhost:8000/api/v1/saju/analyze', formData);
      console.log('API 응답:', response.data);
      setResult(response.data);
    } catch (err: any) {
      console.error('API 오류:', err);
      console.error('응답 데이터:', err.response?.data);
      setError(err.response?.data?.detail || '분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title>🔮 사주팔자 분석 서비스</Title>
      
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label>이름</Label>
          <Input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="이름을 입력하세요"
            required
          />
        </FormGroup>

        <FormGroup>
          <Label>생년월일</Label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
            <Input
              type="number"
              name="year"
              value={formData.year}
              onChange={handleInputChange}
              placeholder="년 (예: 1990)"
              min="1900"
              max="2100"
              required
            />
            <Input
              type="number"
              name="month"
              value={formData.month}
              onChange={handleInputChange}
              placeholder="월 (1-12)"
              min="1"
              max="12"
              required
            />
            <Input
              type="number"
              name="day"
              value={formData.day}
              onChange={handleInputChange}
              placeholder="일 (1-31)"
              min="1"
              max="31"
              required
            />
          </div>
        </FormGroup>

        <FormGroup>
          <Label>태어난 시간</Label>
          <Select
            name="hour"
            value={formData.hour}
            onChange={handleInputChange}
            required
          >
            <option value="">시간을 선택하세요</option>
            {Array.from({length: 24}, (_, i) => (
              <option key={i} value={i}>{i}시</option>
            ))}
          </Select>
        </FormGroup>

        <FormGroup>
          <Label>성별</Label>
          <Select
            name="gender"
            value={formData.gender}
            onChange={handleInputChange}
          >
            <option value="male">남성</option>
            <option value="female">여성</option>
          </Select>
        </FormGroup>

        <Button type="submit" disabled={loading}>
          {loading ? '분석 중...' : '사주 분석하기'}
        </Button>
      </Form>

      {error && (
        <div style={{ padding: '20px', background: '#fee', color: '#c33', borderRadius: '8px', marginBottom: '20px' }}>
          {error}
        </div>
      )}

      {result && (
        <ResultContainer>
          <h2>{result.basic_info?.name || '사용자'}님의 사주팔자</h2>
          
          <SajuGrid>
            <SajuPillar>
              <PillarTitle>년주</PillarTitle>
              <Character>{result.saju_palja.year_pillar.stem}</Character>
              <Character>{result.saju_palja.year_pillar.branch}</Character>
            </SajuPillar>
            <SajuPillar>
              <PillarTitle>월주</PillarTitle>
              <Character>{result.saju_palja.month_pillar.stem}</Character>
              <Character>{result.saju_palja.month_pillar.branch}</Character>
            </SajuPillar>
            <SajuPillar>
              <PillarTitle>일주</PillarTitle>
              <Character>{result.saju_palja.day_pillar.stem}</Character>
              <Character>{result.saju_palja.day_pillar.branch}</Character>
            </SajuPillar>
            <SajuPillar>
              <PillarTitle>시주</PillarTitle>
              <Character>{result.saju_palja.hour_pillar.stem}</Character>
              <Character>{result.saju_palja.hour_pillar.branch}</Character>
            </SajuPillar>
          </SajuGrid>

          <AnalysisSection>
            <SectionTitle>🌟 성격 분석</SectionTitle>
            <p>{result.interpretations.personality}</p>
          </AnalysisSection>

          <AnalysisSection>
            <SectionTitle>💼 직업운</SectionTitle>
            <p>{result.interpretations.career}</p>
          </AnalysisSection>

          <AnalysisSection>
            <SectionTitle>💪 건강운</SectionTitle>
            <p>{result.interpretations.health}</p>
          </AnalysisSection>

          <AnalysisSection>
            <SectionTitle>👥 대인관계</SectionTitle>
            <p>{result.interpretations.relationships}</p>
          </AnalysisSection>

          <AnalysisSection>
            <SectionTitle>💰 재물운</SectionTitle>
            <p>{result.interpretations.wealth}</p>
          </AnalysisSection>
        </ResultContainer>
      )}
    </Container>
  );
}

export default App;