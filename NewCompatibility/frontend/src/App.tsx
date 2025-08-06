import React from "react";
import styled from "styled-components";
import CompatibilityForm from "./components/CompatibilityForm";
import CompatibilityResult from "./components/CompatibilityResult";
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

function App() {
  const [compatibilityResult, setCompatibilityResult] =
    React.useState<CompatibilityData | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const handleAnalysisComplete = (result: CompatibilityData) => {
    setCompatibilityResult(result);
    setError(null);
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
            <CompatibilityResult
              data={compatibilityResult}
              onReset={handleReset}
            />
          )}
        </Content>
      </Container>
    </AppContainer>
  );
}

export default App;
