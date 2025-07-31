
import React, { useState, useCallback } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

const App: React.FC = () => {
  const [agree, setAgree] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError('');
      setResult('');
    }
  };

  const handleAnalyze = useCallback(async () => {
    if (!selectedFile) {
      setError('분석할 이미지를 선택해주세요.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setIsLoading(true);
    setError('');
    setResult('');

    try {
            const response = await axios.post('http://localhost:8001/analyze/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.data.success) {
        setResult(response.data.report);
      } else {
        setError(response.data.detail || '분석에 실패했습니다.');
      }
    } catch (err: any) {
      if (err.response) {
        setError(`오류: ${err.response.data.detail || '서버에서 오류가 발생했습니다.'}`);
      } else if (err.request) {
        setError('서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.');
      } else {
        setError(`네트워크 오류가 발생했습니다: ${err.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  }, [selectedFile]);

  return (
    <AppContainer>
      <Header>
        <Title>AI 관상 분석 (엔터테인먼트용)</Title>
      </Header>

      <MainContent>
        <Disclaimer>
          <h3>※ 중요 고지 사항 ※</h3>
          <p>
            본 AI 관상 분석은 <strong>오직 오락 및 재미를 위한 목적</strong>으로 제공됩니다. 관상학은 과학적 근거가 없는 전통적인 믿음 체계입니다.
            분석 결과는 예술적, 문화적 해석에 기반한 것이며, 자신이나 타인에 대한 어떠한 판단이나 중요한 결정을 내리는 데 사용되어서는 안 됩니다.
            기반 AI 기술에는 알려진 편향과 한계가 존재할 수 있습니다.
          </p>
          <label>
            <input type="checkbox" checked={agree} onChange={() => setAgree(!agree)} />
            &nbsp;위 내용을 모두 읽고 이해했으며, 본 서비스가 비과학적인 오락용 콘텐츠임에 동의합니다.
          </label>
        </Disclaimer>

        <UploadSection>
          <FileInput type="file" accept="image/jpeg, image/png" onChange={handleFileChange} disabled={!agree || isLoading} />
          <AnalyzeButton onClick={handleAnalyze} disabled={!agree || !selectedFile || isLoading}>
            {isLoading ? '분석 중...' : '분석 시작'}
          </AnalyzeButton>
        </UploadSection>

        {isLoading && <Loader><div></div><div></div><div></div></Loader>}
        
        {error && <ErrorBox>{error}</ErrorBox>}
        
        {result && (
          <ResultBox>
            <h3>분석 결과</h3>
            <pre>{result}</pre>
          </ResultBox>
        )}
      </MainContent>
      
      <Footer>
        <FooterText>© 2024 MSProject2 - Physiognomy Service</FooterText>
      </Footer>
    </AppContainer>
  );
};

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f0f2f5;
  color: #333;
  font-family: 'Noto Sans KR', sans-serif;
`;

const Header = styled.header`
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
`;

const Disclaimer = styled.div`
  border: 2px solid #ff4d4f;
  padding: 20px;
  margin-bottom: 30px;
  background-color: #fff1f0;
  border-radius: 8px;
  width: 100%;
  animation: ${fadeIn} 0.5s ease-out;

  h3 {
    margin-top: 0;
    color: #cf1322;
  }
  p {
    line-height: 1.6;
  }
  label {
    display: flex;
    align-items: center;
    font-weight: 500;
    cursor: pointer;
  }
`;

const UploadSection = styled.div`
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  width: 100%;
  animation: ${fadeIn} 0.7s ease-out;
`;

const FileInput = styled.input`
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  &:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }
`;

const AnalyzeButton = styled.button`
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: 500;
  color: white;
  background-color: #1890ff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover:not(:disabled) {
    background-color: #40a9ff;
  }

  &:disabled {
    background-color: #a0d911;
    cursor: not-allowed;
  }
`;

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const Loader = styled.div`
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
  margin: 30px 0;
  div {
    box-sizing: border-box;
    display: block;
    position: absolute;
    width: 64px;
    height: 64px;
    margin: 8px;
    border: 8px solid #764ba2;
    border-radius: 50%;
    animation: ${spin} 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    border-color: #764ba2 transparent transparent transparent;
  }
  div:nth-child(1) { animation-delay: -0.45s; }
  div:nth-child(2) { animation-delay: -0.3s; }
  div:nth-child(3) { animation-delay: -0.15s; }
`;

const ResultBox = styled.div`
  width: 100%;
  margin-top: 20px;
  background-color: #ffffff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: ${fadeIn} 0.5s ease-out;

  h3 {
    margin-top: 0;
    border-bottom: 2px solid #764ba2;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }

  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1rem;
    line-height: 1.8;
  }
`;

const ErrorBox = styled.div`
  width: 100%;
  margin-top: 20px;
  padding: 15px;
  background-color: #fff1f0;
  color: #cf1322;
  border: 1px solid #ffccc7;
  border-radius: 4px;
  animation: ${fadeIn} 0.5s ease-out;
`;

const Footer = styled.footer`
  text-align: center;
  padding: 30px 20px;
  color: #8c8c8c;
  background-color: #e0e0e0;
`;

const FooterText = styled.p`
  font-size: 0.9rem;
`;

export default App;
