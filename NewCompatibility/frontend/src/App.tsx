import React from "react";
import styled from "styled-components";
import CompatibilityForm from "./components/CompatibilityForm";
import CompatibilityResult from "./components/CompatibilityResult";
import CompatibilityAIChat from "./components/CompatibilityAIChat";
import AzureCompatibilityAIChat from "./components/AzureCompatibilityAIChat";
import { CompatibilityData } from "./types/compatibility";
import "./App.css";

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const Header = styled.header`
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin: 0 0 10px 0;
  font-weight: 700;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.9;
`;

const Content = styled.div`
  padding: 40px 20px;
`;

const AIButtonContainer = styled.div`
  display: flex;
  gap: 15px;
  justify-content: center;
  margin: 20px 0;
`;

const AIButton = styled.button`
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(240, 147, 251, 0.6);
  }

  &:active {
    transform: translateY(0);
  }
`;

const AzureButton = styled.button`
  background: linear-gradient(45deg, #0078d4 0%, #106ebe 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 120, 212, 0.4);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 120, 212, 0.6);
  }

  &:active {
    transform: translateY(0);
  }
`;

function App() {
  const [compatibilityResult, setCompatibilityResult] =
    React.useState<CompatibilityData | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [showAIChat, setShowAIChat] = React.useState(false);
  const [showAzureChat, setShowAzureChat] = React.useState(false);
  const [compatibilityInfo, setCompatibilityInfo] = React.useState<any>(null);

  const handleAnalysisComplete = (
    result: CompatibilityData,
    formData?: any
  ) => {
    setCompatibilityResult(result);
    setError(null);
    if (formData) {
      setCompatibilityInfo(formData);
    }
  };

  const handleAnalysisStart = () => {
    setIsLoading(true);
    setError(null);
    setCompatibilityResult(null);
  };

  const handleAnalysisEnd = () => {
    setIsLoading(false);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setIsLoading(false);
    setCompatibilityResult(null);
  };

  const handleReset = () => {
    setCompatibilityResult(null);
    setError(null);
    setIsLoading(false);
  };

  return (
    <AppContainer>
      <Container>
        <Header>
          <Title>🎯 새로운 궁합 분석</Title>
          <Subtitle>전통 사주 이론을 바탕으로 한 과학적 궁합 분석</Subtitle>
        </Header>
        <Content>
          <CompatibilityForm
            onAnalysisComplete={handleAnalysisComplete}
            onAnalysisStart={handleAnalysisStart}
            onAnalysisEnd={handleAnalysisEnd}
            onError={handleError}
            isLoading={isLoading}
          />

          {error && (
            <div
              style={{
                margin: "20px 0",
                padding: "20px",
                background: "#f8d7da",
                border: "1px solid #f5c6cb",
                borderRadius: "10px",
                color: "#721c24",
              }}
            >
              <h4>⚠️ 오류가 발생했습니다</h4>
              <p>{error}</p>
              <button
                onClick={handleReset}
                style={{
                  padding: "10px 20px",
                  background: "#dc3545",
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                다시 시도
              </button>
            </div>
          )}

          {compatibilityResult && (
            <>
              <CompatibilityResult
                data={compatibilityResult}
                onReset={handleReset}
              />

              {compatibilityInfo && (
                <AIButtonContainer>
                  <AIButton onClick={() => setShowAIChat(true)}>
                    💕 Gemini AI 궁합 해석
                  </AIButton>
                  <AzureButton onClick={() => setShowAzureChat(true)}>
                    ⚡ Azure GPT-4.1 궁합 해석
                  </AzureButton>
                </AIButtonContainer>
              )}
            </>
          )}
        </Content>
      </Container>

      {/* AI 채팅 인터페이스 */}
      {compatibilityInfo && (
        <>
          <CompatibilityAIChat
            compatibilityInfo={compatibilityInfo}
            isVisible={showAIChat}
            onClose={() => setShowAIChat(false)}
          />
          <AzureCompatibilityAIChat
            compatibilityInfo={compatibilityInfo}
            isVisible={showAzureChat}
            onClose={() => setShowAzureChat(false)}
          />
        </>
      )}
    </AppContainer>
  );
}

export default App;
