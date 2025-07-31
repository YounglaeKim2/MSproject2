import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
`;

const Title = styled.h1`
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 2.5em;
`;

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
  gap: 20px;
  margin-bottom: 20px;
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
  
  &:hover {
    transform: translateY(-2px);
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
  }
`;

const ResultContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
`;

const ScoreDisplay = styled.div`
  text-align: center;
  margin-bottom: 30px;
`;

const ScoreNumber = styled.div`
  font-size: 4em;
  font-weight: bold;
  color: #e74c3c;
  margin-bottom: 10px;
`;

const Grade = styled.div`
  font-size: 1.5em;
  color: #2c3e50;
  font-weight: bold;
`;

const DetailSection = styled.div`
  margin-bottom: 25px;
`;

const SectionTitle = styled.h3`
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 15px;
`;

const Loading = styled.div`
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #7f8c8d;
`;

interface PersonInfo {
  name: string;
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: string;
}

interface CompatibilityResult {
  total_score: number;
  grade: string;
  strengths: string[];
  weaknesses: string[];
  advice: string[];
  love_compatibility: number;
  marriage_compatibility: number;
  business_compatibility: number;
  friendship_compatibility: number;
}

const App: React.FC = () => {
  const [person1, setPerson1] = useState<PersonInfo>({
    name: '', year: 1990, month: 1, day: 1, hour: 12, gender: 'male'
  });
  
  const [person2, setPerson2] = useState<PersonInfo>({
    name: '', year: 1990, month: 1, day: 1, hour: 12, gender: 'female'
  });
  
  const [result, setResult] = useState<CompatibilityResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!person1.name || !person2.name) {
      alert('두 사람의 이름을 모두 입력해주세요.');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('/api/v1/compatibility/analyze', {
        person1,
        person2
      });
      
      setResult(response.data.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '궁합 분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const updatePerson1 = (field: keyof PersonInfo, value: string | number) => {
    setPerson1(prev => ({ ...prev, [field]: value }));
  };

  const updatePerson2 = (field: keyof PersonInfo, value: string | number) => {
    setPerson2(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Container>
      <Title>🔮 궁합 분석 서비스</Title>
      
      <FormContainer>
        <PersonForm>
          <div>
            <h3>첫 번째 사람</h3>
            <FormGroup>
              <Label>이름</Label>
              <Input
                value={person1.name}
                onChange={(e) => updatePerson1('name', e.target.value)}
                placeholder="이름을 입력하세요"
              />
            </FormGroup>
            <FormGroup>
              <Label>출생년도</Label>
              <Input
                type="number"
                value={person1.year}
                onChange={(e) => updatePerson1('year', parseInt(e.target.value))}
                min="1900"
                max="2024"
              />
            </FormGroup>
            <FormGroup>
              <Label>출생월</Label>
              <Select
                value={person1.month}
                onChange={(e) => updatePerson1('month', parseInt(e.target.value))}
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
                onChange={(e) => updatePerson1('day', parseInt(e.target.value))}
                min="1"
                max="31"
              />
            </FormGroup>
            <FormGroup>
              <Label>출생시간</Label>
              <Select
                value={person1.hour}
                onChange={(e) => updatePerson1('hour', parseInt(e.target.value))}
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
                onChange={(e) => updatePerson1('gender', e.target.value)}
              >
                <option value="male">남성</option>
                <option value="female">여성</option>
              </Select>
            </FormGroup>
          </div>

          <div>
            <h3>두 번째 사람</h3>
            <FormGroup>
              <Label>이름</Label>
              <Input
                value={person2.name}
                onChange={(e) => updatePerson2('name', e.target.value)}
                placeholder="이름을 입력하세요"
              />
            </FormGroup>
            <FormGroup>
              <Label>출생년도</Label>
              <Input
                type="number"
                value={person2.year}
                onChange={(e) => updatePerson2('year', parseInt(e.target.value))}
                min="1900"
                max="2024"
              />
            </FormGroup>
            <FormGroup>
              <Label>출생월</Label>
              <Select
                value={person2.month}
                onChange={(e) => updatePerson2('month', parseInt(e.target.value))}
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
                onChange={(e) => updatePerson2('day', parseInt(e.target.value))}
                min="1"
                max="31"
              />
            </FormGroup>
            <FormGroup>
              <Label>출생시간</Label>
              <Select
                value={person2.hour}
                onChange={(e) => updatePerson2('hour', parseInt(e.target.value))}
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
                onChange={(e) => updatePerson2('gender', e.target.value)}
              >
                <option value="male">남성</option>
                <option value="female">여성</option>
              </Select>
            </FormGroup>
          </div>
        </PersonForm>
        
        <Button onClick={handleAnalyze} disabled={loading}>
          {loading ? '분석 중...' : '궁합 분석하기'}
        </Button>
      </FormContainer>

      {loading && <Loading>궁합을 분석하고 있습니다... 잠시만 기다려주세요.</Loading>}
      
      {error && (
        <ResultContainer>
          <div style={{color: '#e74c3c', textAlign: 'center', fontSize: '18px'}}>
            {error}
          </div>
        </ResultContainer>
      )}

      {result && !loading && (
        <ResultContainer>
          <ScoreDisplay>
            <ScoreNumber>{result.total_score}점</ScoreNumber>
            <Grade>{result.grade}</Grade>
          </ScoreDisplay>

          <PersonForm style={{marginBottom: '30px'}}>
            <div>
              <SectionTitle>분야별 궁합</SectionTitle>
              <div>연애 궁합: {result.love_compatibility}점</div>
              <div>결혼 궁합: {result.marriage_compatibility}점</div>
              <div>사업 궁합: {result.business_compatibility}점</div>
              <div>우정 궁합: {result.friendship_compatibility}점</div>
            </div>
            <div>
              <SectionTitle>궁합의 장점</SectionTitle>
              {result.strengths.map((strength, idx) => (
                <div key={idx}>• {strength}</div>
              ))}
            </div>
          </PersonForm>

          {result.weaknesses.length > 0 && (
            <DetailSection>
              <SectionTitle>주의사항</SectionTitle>
              {result.weaknesses.map((weakness, idx) => (
                <div key={idx}>• {weakness}</div>
              ))}
            </DetailSection>
          )}

          <DetailSection>
            <SectionTitle>조언</SectionTitle>
            {result.advice.map((advice, idx) => (
              <div key={idx}>• {advice}</div>
            ))}
          </DetailSection>
        </ResultContainer>
      )}
    </Container>
  );
};

export default App;