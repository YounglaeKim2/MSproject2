import React from 'react';
import styled from 'styled-components';

const App: React.FC = () => {
  const handleServiceSelect = (service: 'saju' | 'physiognomy') => {
    const urls = {
      saju: 'http://localhost:3000',
      physiognomy: 'http://localhost:3001'
    };
    
    window.open(urls[service], '_blank');
  };

  return (
    <AppContainer>
      <Header>
        <Title>MSProject2</Title>
        <Subtitle>전통 운명학과 현대 기술의 만남</Subtitle>
      </Header>

      <MainContent>
        <ServiceGrid>
          <ServiceCard onClick={() => handleServiceSelect('saju')}>
            <ServiceIcon>🔮</ServiceIcon>
            <ServiceTitle>사주팔자</ServiceTitle>
            <ServiceDescription>
              생년월일시를 기반으로 한<br/>
              전통 명리학 사주 분석
            </ServiceDescription>
            <ServiceFeatures>
              <Feature>• 정확한 만세력 계산</Feature>
              <Feature>• 오행 분석</Feature>
              <Feature>• 성격, 직업, 건강운</Feature>
              <Feature>• 대인관계, 재물운</Feature>
            </ServiceFeatures>
          </ServiceCard>

          <ServiceCard onClick={() => handleServiceSelect('physiognomy')}>
            <ServiceIcon>👤</ServiceIcon>
            <ServiceTitle>관상 분석</ServiceTitle>
            <ServiceDescription>
              얼굴 특징을 분석한<br/>
              AI 기반 관상 해석
            </ServiceDescription>
            <ServiceFeatures>
              <Feature>• AI 얼굴 인식</Feature>
              <Feature>• 관상학 이론 적용</Feature>
              <Feature>• 성격 특성 분석</Feature>
              <Feature>• 운세 및 적성</Feature>
            </ServiceFeatures>
          </ServiceCard>
        </ServiceGrid>

        <InfoSection>
          <InfoTitle>서비스 특징</InfoTitle>
          <InfoGrid>
            <InfoItem>
              <InfoIcon>🎯</InfoIcon>
              <InfoText>정확한 분석</InfoText>
            </InfoItem>
            <InfoItem>
              <InfoIcon>🔒</InfoIcon>
              <InfoText>개인정보 보호</InfoText>
            </InfoItem>
            <InfoItem>
              <InfoIcon>⚡</InfoIcon>
              <InfoText>실시간 결과</InfoText>
            </InfoItem>
            <InfoItem>
              <InfoIcon>📱</InfoIcon>
              <InfoText>반응형 디자인</InfoText>
            </InfoItem>
          </InfoGrid>
        </InfoSection>
      </MainContent>

      <Footer>
        <FooterText>
          © 2024 MSProject2. 전통 명리학과 현대 기술의 융합 서비스입니다.
        </FooterText>
        <FooterNote>
          * 본 서비스는 참고용이며, 중요한 결정은 전문가와 상담하시기 바랍니다.
        </FooterNote>
      </Footer>
    </AppContainer>
  );
};

// 스타일 컴포넌트들
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
  font-size: 4rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.5rem;
  opacity: 0.9;
  
  @media (max-width: 768px) {
    font-size: 1.2rem;
  }
`;

const MainContent = styled.main`
  flex: 1;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 60px;
`;

const ServiceGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 40px;
  max-width: 1000px;
  width: 100%;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 30px;
  }
`;

const ServiceCard = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  
  &:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    background: rgba(255, 255, 255, 1);
  }
`;

const ServiceIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 20px;
`;

const ServiceTitle = styled.h2`
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
`;

const ServiceDescription = styled.p`
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
`;

const ServiceFeatures = styled.div`
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Feature = styled.div`
  font-size: 0.95rem;
  color: #555;
  line-height: 1.4;
`;

const InfoSection = styled.section`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 800px;
  width: 100%;
`;

const InfoTitle = styled.h3`
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  text-align: center;
  margin-bottom: 30px;
`;

const InfoGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 30px;
`;

const InfoItem = styled.div`
  text-align: center;
  color: white;
`;

const InfoIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 10px;
`;

const InfoText = styled.div`
  font-size: 1rem;
  font-weight: 500;
`;

const Footer = styled.footer`
  text-align: center;
  padding: 40px 20px;
  color: rgba(255, 255, 255, 0.8);
`;

const FooterText = styled.p`
  font-size: 1rem;
  margin-bottom: 10px;
`;

const FooterNote = styled.p`
  font-size: 0.85rem;
  opacity: 0.7;
`;

export default App;