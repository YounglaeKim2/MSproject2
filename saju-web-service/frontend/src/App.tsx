import React, { useState } from 'react';
import styled from 'styled-components';
import BirthForm from './components/BirthForm';
import SajuResult from './components/SajuResult';
import { BirthInfo, SajuAnalysisResult } from './types/saju';
import { sajuApi } from './services/api';

const App: React.FC = () => {
  const [result, setResult] = useState<SajuAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentBirthInfo, setCurrentBirthInfo] = useState<BirthInfo | null>(null);

  const handleFormSubmit = async (birthInfo: BirthInfo) => {
    setLoading(true);
    setError(null);
    setCurrentBirthInfo(birthInfo);

    try {
      console.log('사주 분석 요청:', birthInfo);
      const analysisResult = await sajuApi.analyzeSaju(birthInfo);
      console.log('사주 분석 결과:', analysisResult);
      setResult(analysisResult);
    } catch (err: any) {
      console.error('사주 분석 오류:', err);
      setError(err.message || '사주 분석 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setCurrentBirthInfo(null);
  };

  return (
    <AppContainer>
      <Header>
        <HeaderTitle onClick={handleReset}>사주 웹 서비스</HeaderTitle>
        <HeaderSubtitle>전통 명리학 기반 사주팔자 분석</HeaderSubtitle>
      </Header>

      <MainContent>
        {!result ? (
          <FormSection>
            <BirthForm onSubmit={handleFormSubmit} loading={loading} />
            
            {loading && (
              <LoadingSection>
                <LoadingSpinner />
                <LoadingText>사주를 분석하고 있습니다...</LoadingText>
                <LoadingSubtext>잠시만 기다려주세요</LoadingSubtext>
              </LoadingSection>
            )}

            {error && (
              <ErrorSection>
                <ErrorIcon>⚠️</ErrorIcon>
                <ErrorText>{error}</ErrorText>
                <RetryButton onClick={() => setError(null)}>
                  다시 시도
                </RetryButton>
              </ErrorSection>
            )}
          </FormSection>
        ) : (
          <ResultSection>
            <ActionButtons>
              <BackButton onClick={handleReset}>
                ← 새로운 사주 보기
              </BackButton>
            </ActionButtons>
            <SajuResult 
              result={result} 
              name={currentBirthInfo?.name}
            />
          </ResultSection>
        )}
      </MainContent>

      <Footer>
        <FooterText>
          © 2024 사주 웹 서비스. 전통 명리학을 현대적으로 해석한 서비스입니다.
        </FooterText>
        <FooterNote>
          * 이 서비스는 참고용이며, 중요한 결정은 전문가와 상담하시기 바랍니다.
        </FooterNote>
      </Footer>
    </AppContainer>
  );
};

// 스타일 컴포넌트들
const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
`;

const Header = styled.header`
  text-align: center;
  padding: 40px 20px;
  color: white;
`;

const HeaderTitle = styled.h1`
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
  }
  
  @media (max-width: 768px) {
    font-size: 2.2rem;
  }
`;

const HeaderSubtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  
  @media (max-width: 768px) {
    font-size: 1rem;
  }
`;

const MainContent = styled.main`
  flex: 1;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
`;

const FormSection = styled.div`
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 30px;
`;

const ResultSection = styled.div`
  width: 100%;
  max-width: 1000px;
`;

const ActionButtons = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
`;

const BackButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }
`;

const LoadingSection = styled.div`
  background: white;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
`;

const LoadingSpinner = styled.div`
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingText = styled.h3`
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 10px;
`;

const LoadingSubtext = styled.p`
  color: #666;
  font-size: 1rem;
`;

const ErrorSection = styled.div`
  background: white;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border-left: 5px solid #ff6b6b;
`;

const ErrorIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 15px;
`;

const ErrorText = styled.p`
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 20px;
  line-height: 1.5;
`;

const RetryButton = styled.button`
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: #ff5252;
    transform: translateY(-2px);
  }
`;

const Footer = styled.footer`
  text-align: center;
  padding: 30px 20px;
  color: rgba(255, 255, 255, 0.8);
`;

const FooterText = styled.p`
  font-size: 0.9rem;
  margin-bottom: 5px;
`;

const FooterNote = styled.p`
  font-size: 0.8rem;
  opacity: 0.7;
`;

export default App;