import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import styled from 'styled-components'

const TestPage = ({ title, description }) => {
  const location = useLocation()
  
  return (
    <Container>
      <Header>
        <Title>{title || '테스트 페이지'}</Title>
        <Subtitle>현재 경로: {location.pathname}</Subtitle>
      </Header>
      
      <Content>
        <Description>
          {description || '이 페이지는 라우팅 테스트용입니다.'}
        </Description>
        
        <NavigationSection>
          <NavTitle>페이지 이동 테스트</NavTitle>
          <NavLinks>
            <StyledLink to="/">🏠 홈으로</StyledLink>
            <StyledLink to="/saju">🔮 사주 페이지</StyledLink>
            <StyledLink to="/compatibility">💕 궁합 페이지</StyledLink>
          </NavLinks>
        </NavigationSection>
        
        <InfoSection>
          <InfoTitle>라우팅 정보</InfoTitle>
          <InfoList>
            <InfoItem>✅ React Router v6 적용</InfoItem>
            <InfoItem>✅ SPA 방식 페이지 전환</InfoItem>
            <InfoItem>✅ 브라우저 히스토리 지원</InfoItem>
            <InfoItem>✅ 뒤로가기/앞으로가기 동작</InfoItem>
          </InfoList>
        </InfoSection>
      </Content>
    </Container>
  )
}

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
`

const Header = styled.header`
  text-align: center;
  margin-bottom: 40px;
`

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`

const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.8;
`

const Content = styled.main`
  max-width: 800px;
  margin: 0 auto;
`

const Description = styled.p`
  font-size: 1.1rem;
  text-align: center;
  margin-bottom: 40px;
  line-height: 1.6;
`

const NavigationSection = styled.section`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
`

const NavTitle = styled.h2`
  font-size: 1.5rem;
  margin-bottom: 20px;
  text-align: center;
`

const NavLinks = styled.div`
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
`

const StyledLink = styled(Link)`
  background: rgba(255, 255, 255, 0.2);
  color: white;
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 25px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }
`

const InfoSection = styled.section`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  backdrop-filter: blur(10px);
`

const InfoTitle = styled.h3`
  font-size: 1.3rem;
  margin-bottom: 15px;
  text-align: center;
`

const InfoList = styled.ul`
  list-style: none;
  padding: 0;
`

const InfoItem = styled.li`
  padding: 8px 0;
  font-size: 1rem;
`

export default TestPage