import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { 
  compatibilityApi, 
  CompatibilityFormData, 
  PersonInfo, 
  CompatibilityApiResponse 
} from '../services/compatibilityApi';
import CompatibilityForm from '../components/compatibility/CompatibilityForm';
import CompatibilityResultComponent from '../components/compatibility/CompatibilityResult';
import { Container, Title, ErrorMessage } from '../components/saju/styles/SharedStyles';

const BackButton = styled(Link)`
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 25px;
  margin-bottom: 20px;
  transition: all 0.3s;
  border: 2px solid transparent;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }
`;

const Loading = styled.div`
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #7f8c8d;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin-bottom: 20px;
`;

const CompatibilityPage: React.FC = () => {
  const [person1, setPerson1] = useState<PersonInfo>({
    name: '',
    year: 1990,
    month: 1,
    day: 1,
    hour: 12,
    gender: 'male'
  });

  const [person2, setPerson2] = useState<PersonInfo>({
    name: '',
    year: 1992,
    month: 1,
    day: 1,
    hour: 12,
    gender: 'female'
  });

  const [result, setResult] = useState<CompatibilityApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePerson1Change = (field: keyof PersonInfo, value: string | number) => {
    setPerson1(prev => ({ ...prev, [field]: value }));
  };

  const handlePerson2Change = (field: keyof PersonInfo, value: string | number) => {
    setPerson2(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!person1.name.trim() || !person2.name.trim()) {
      setError('두 사람의 이름을 모두 입력해주세요.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const formData: CompatibilityFormData = { person1, person2 };
      console.log('궁합 분석 요청 데이터:', formData);
      
      const response = await compatibilityApi.analyzeCompatibility(formData);
      console.log('궁합 분석 API 응답:', response);
      
      setResult(response);
    } catch (err: any) {
      console.error('궁합 분석 API 오류:', err);
      console.error('응답 데이터:', err.response?.data);
      setError(err.response?.data?.detail || '궁합 분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <BackButton to="/">← 홈으로 돌아가기</BackButton>
      
      <Title>💕 궁합 분석 서비스</Title>

      <CompatibilityForm
        person1={person1}
        person2={person2}
        loading={loading}
        onPerson1Change={handlePerson1Change}
        onPerson2Change={handlePerson2Change}
        onSubmit={handleSubmit}
      />

      {loading && (
        <Loading>
          🔮 두 분의 궁합을 분석하고 있습니다... 잠시만 기다려주세요.
        </Loading>
      )}

      {error && <ErrorMessage>{error}</ErrorMessage>}

      {result && !loading && (
        <CompatibilityResultComponent 
          result={result.data} 
          personsInfo={result.persons_info}
        />
      )}
    </Container>
  );
};

export default CompatibilityPage;