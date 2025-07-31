import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { sajuApi, SajuFormData, SajuResult as SajuResultType, DaeunResult as DaeunResultType, SaeunResult as SaeunResultType } from '../services/sajuApi';
import SajuForm from '../components/saju/SajuForm';
import SajuResultComponent from '../components/saju/SajuResult';
import DaeunResultComponent from '../components/saju/DaeunResult';
import SaeunResultComponent from '../components/saju/SaeunResult';
import AIChatInterface from '../components/saju/AIChatInterface';
import {
  Container,
  Title,
  Form,
  Button,
  AIButton,
  ErrorMessage
} from '../components/saju/styles/SharedStyles';

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

const SectionContainer = styled.div`
  margin-bottom: 20px;
`;

const SajuPage: React.FC = () => {
  const [formData, setFormData] = useState<SajuFormData>({
    year: '',
    month: '',
    day: '',
    hour: '',
    gender: 'male',
    name: '',
  });

  const [result, setResult] = useState<SajuResultType | null>(null);
  const [daeunResult, setDaeunResult] = useState<DaeunResultType | null>(null);
  const [saeunResult, setSaeunResult] = useState<SaeunResultType | null>(null);
  const [loading, setLoading] = useState(false);
  const [daeunLoading, setDaeunLoading] = useState(false);
  const [saeunLoading, setSaeunLoading] = useState(false);
  const [targetYear, setTargetYear] = useState<number>(new Date().getFullYear());
  const [error, setError] = useState('');
  const [showAIChat, setShowAIChat] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === 'year' || name === 'month' || name === 'day' || name === 'hour'
          ? value === ''
            ? ''
            : parseInt(value)
          : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('요청 데이터:', formData);
      const response = await sajuApi.analyzeSaju(formData);
      console.log('API 응답:', response);
      setResult(response);
    } catch (err: any) {
      console.error('API 오류:', err);
      console.error('응답 데이터:', err.response?.data);
      setError(err.response?.data?.detail || '분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleDaeunAnalysis = async () => {
    setDaeunLoading(true);
    setError('');

    try {
      console.log('대운 분석 요청 데이터:', formData);
      const response = await sajuApi.analyzeDaeun(formData);
      console.log('대운 분석 API 응답:', response);
      setDaeunResult(response);
    } catch (err: any) {
      console.error('대운 분석 API 오류:', err);
      console.error('응답 데이터:', err.response?.data);
      setError(err.response?.data?.detail || '대운 분석 중 오류가 발생했습니다.');
    } finally {
      setDaeunLoading(false);
    }
  };

  const handleSaeunAnalysis = async () => {
    setSaeunLoading(true);
    setError('');

    try {
      console.log('세운 분석 요청 데이터:', formData, '대상연도:', targetYear);
      const response = await sajuApi.analyzeSaeun(formData, targetYear);
      console.log('세운 분석 API 응답:', response);
      setSaeunResult(response);
    } catch (err: any) {
      console.error('세운 분석 API 오류:', err);
      console.error('응답 데이터:', err.response?.data);
      setError(err.response?.data?.detail || '세운 분석 중 오류가 발생했습니다.');
    } finally {
      setSaeunLoading(false);
    }
  };

  return (
    <Container>
      <BackButton to="/">← 홈으로 돌아가기</BackButton>
      
      <Title>🔮 사주팔자 분석 서비스</Title>

      {/* 기본 사주 분석 폼 */}
      <SectionContainer>
        <SajuForm
          formData={formData}
          loading={loading}
          onInputChange={handleInputChange}
          onSubmit={handleSubmit}
        />
      </SectionContainer>

      {/* 대운 분석 섹션 */}
      <SectionContainer>
        <Form
          style={{
            marginTop: '20px',
            background: '#f8f9fa',
            border: '2px solid #e9ecef',
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: '20px' }}>
            <h3 style={{ color: '#495057', margin: '0 0 10px 0' }}>
              🌟 대운 분석
            </h3>
            <p style={{ color: '#6c757d', margin: 0, fontSize: '14px' }}>
              인생 전체의 운세 흐름을 10년 주기로 분석합니다
            </p>
          </div>
          <Button
            type="button"
            disabled={daeunLoading || !formData.name}
            onClick={handleDaeunAnalysis}
            style={{
              background: daeunLoading
                ? '#6c757d'
                : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              marginTop: '0',
            }}
          >
            {daeunLoading ? '대운 분석 중...' : '대운 분석하기'}
          </Button>
        </Form>
      </SectionContainer>

      {/* 세운 분석 섹션 */}
      <SectionContainer>
        <Form
          style={{
            marginTop: '20px',
            background: '#e8f5e8',
            border: '2px solid #c8e6c9',
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: '20px' }}>
            <h3 style={{ color: '#2e7d32', margin: '0 0 10px 0' }}>
              ⏰ 세운 분석
            </h3>
            <p style={{ color: '#4caf50', margin: 0, fontSize: '14px' }}>
              특정 연도의 월별 운세를 상세하게 분석합니다
            </p>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ color: '#2e7d32', display: 'block', marginBottom: '8px', fontWeight: 600 }}>
              분석 대상 연도
            </label>
            <input
              type="number"
              value={targetYear}
              onChange={(e) => setTargetYear(parseInt(e.target.value) || new Date().getFullYear())}
              min="2020"
              max="2030"
              style={{
                width: '100%',
                padding: '12px',
                border: '2px solid #c8e6c9',
                borderRadius: '8px',
                fontSize: '16px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <Button
            type="button"
            disabled={saeunLoading || !formData.name}
            onClick={handleSaeunAnalysis}
            style={{
              background: saeunLoading
                ? '#6c757d'
                : 'linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)',
              marginTop: '0',
            }}
          >
            {saeunLoading ? '세운 분석 중...' : `${targetYear}년 세운 분석하기`}
          </Button>
        </Form>
      </SectionContainer>

      {/* 에러 메시지 */}
      {error && <ErrorMessage>{error}</ErrorMessage>}

      {/* 결과 표시 */}
      {result && <SajuResultComponent result={result} />}
      {daeunResult && <DaeunResultComponent result={daeunResult} />}
      {saeunResult && (
        <>
          <SaeunResultComponent result={saeunResult} />
          <div style={{ textAlign: 'center', margin: '20px 0' }}>
            <AIButton onClick={() => setShowAIChat(true)}>
              🤖 AI와 상세 해석 나누기
            </AIButton>
          </div>
        </>
      )}

      {/* AI 채팅 인터페이스 */}
      {result && (
        <AIChatInterface
          birthInfo={{
            year: parseInt(formData.year.toString()),
            month: parseInt(formData.month.toString()),
            day: parseInt(formData.day.toString()),
            hour: parseInt(formData.hour.toString()),
            gender: formData.gender,
            name: formData.name
          }}
          isVisible={showAIChat}
          onClose={() => setShowAIChat(false)}
        />
      )}
    </Container>
  );
};

export default SajuPage;