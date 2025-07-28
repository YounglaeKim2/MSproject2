import React from 'react';
import styled from 'styled-components';

const App: React.FC = () => {
  return (
    <AppContainer>
      <Header>
        <Title>관상 분석 서비스</Title>
        <Subtitle>AI 기반 얼굴 인식을 통한 관상 해석</Subtitle>
      </Header>

      <MainContent>
        <ComingSoon>
          <Icon>🚧</Icon>
          <Message>서비스 준비 중입니다</Message>
          <Description>
            동료 개발자가 AI 기반 관상 분석 기능을 개발 중입니다.<br/>
            곧 만나보실 수 있습니다!
          </Description>
          
          <FeatureList>
            <FeatureTitle>예정된 기능</FeatureTitle>
            <Feature>📷 얼굴 이미지 업로드</Feature>
            <Feature>🤖 AI 기반 얼굴 특징 분석</Feature>
            <Feature>👤 전통 관상학 해석</Feature>
            <Feature>📊 성격 및 운세 분석</Feature>
          </FeatureList>
        </ComingSoon>
      </MainContent>

      <Footer>
        <FooterText>
          © 2024 MSProject2 - Physiognomy Service
        </FooterText>
      </Footer>
    </AppContainer>
  );
};

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const Header = styled.header`
  text-align: center;
  padding: 60px 20px 40px;
  color: white;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  
  @media (max-width: 768px) {
    font-size: 2.2rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.3rem;
  opacity: 0.9;
  
  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
`;

const ComingSoon = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  max-width: 600px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
`;

const Icon = styled.div`
  font-size: 4rem;
  margin-bottom: 30px;
`;

const Message = styled.h2`
  font-size: 2.2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
`;

const Description = styled.p`
  font-size: 1.2rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 40px;
`;

const FeatureList = styled.div`
  text-align: left;
  max-width: 400px;
  margin: 0 auto;
`;

const FeatureTitle = styled.h3`
  font-size: 1.3rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
`;

const Feature = styled.div`
  font-size: 1rem;
  color: #555;
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
`;

const Footer = styled.footer`
  text-align: center;
  padding: 30px 20px;
  color: rgba(255, 255, 255, 0.8);
`;

const FooterText = styled.p`
  font-size: 0.9rem;
`;

export default App;