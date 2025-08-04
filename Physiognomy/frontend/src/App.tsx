
import React, { useState, useCallback } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

const App: React.FC = () => {
  const [agree, setAgree] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [luckyCharmImageUrl, setLuckyCharmImageUrl] = useState('');
  const [charmPrompt, setCharmPrompt] = useState('');
  const [analysisId, setAnalysisId] = useState<number | null>(null);
  const [isGeneratingCharm, setIsGeneratingCharm] = useState(false);
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
        setImageUrl(`http://localhost:8001${response.data.image_url}`);
        setCharmPrompt(response.data.charm_prompt);
        setAnalysisId(response.data.analysis_id);
        setLuckyCharmImageUrl(''); // 이전 부적 이미지 초기화
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

  const handleGenerateCharm = async () => {
    if (!charmPrompt || !analysisId) return;

    setIsGeneratingCharm(true);
    setError('');

    try {
      const response = await axios.post(`http://localhost:8001/generate-charm/`, null, {
        params: {
          prompt: charmPrompt,
          analysis_id: analysisId
        }
      });

      if (response.data.success) {
        setLuckyCharmImageUrl(`http://localhost:8001${response.data.lucky_charm_image_url}`);
      } else {
        setError(response.data.detail || '부적 생성에 실패했습니다.');
      }
    } catch (err: any) {
      if (err.response) {
        setError(`오류: ${err.response.data.detail || '서버에서 오류가 발생했습니다.'}`);
      } else if (err.request) {
        setError('서버에 연결할 수 없습니다.');
      } else {
        setError(`네트워크 오류가 발생했습니다: ${err.message}`);
      }
    } finally {
      setIsGeneratingCharm(false);
    }
  };

  const handleDownload = async () => {
    if (!luckyCharmImageUrl) return;

    try {
      // 외부 URL의 이미지를 fetch를 통해 blob으로 변환
      const response = await fetch(luckyCharmImageUrl);
      const blob = await response.blob();

      // Blob URL 생성
      const blobUrl = window.URL.createObjectURL(blob);

      // a 태그를 동적으로 생성하여 다운로드 실행
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = 'lucky-charm.png'; // 저장될 파일명
      document.body.appendChild(link);
      link.click();

      // 생성된 a 태그와 Blob URL 정리
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);

    } catch (error) {
      console.error("부적 이미지 다운로드 실패:", error);
      setError("이미지를 다운로드하는 중 오류가 발생했습니다.");
    }
  };

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
            {imageUrl && <ResultImage src={imageUrl} alt="분석 이미지" />}
            <pre>{result}</pre>
            
            <hr style={{ margin: '30px 0', border: 'none', borderTop: '1px solid #eee' }} />

            {isGeneratingCharm && <Loader><div></div><div></div><div></div></Loader>}

            {!luckyCharmImageUrl && !isGeneratingCharm && (
              <AnalyzeButton 
                onClick={handleGenerateCharm} 
                disabled={isLoading}
                style={{ width: '100%' }}
              >
                행운의 부적 생성
              </AnalyzeButton>
            )}

            {luckyCharmImageUrl && (
              <div>
                <h3>행운의 부적</h3>
                <ResultImage src={luckyCharmImageUrl} alt="행운의 부적" />
                <ButtonContainer>
                  <DownloadButton onClick={handleDownload}>부적 다운로드</DownloadButton>
                  <AnalyzeButton disabled>부적 만들러가기</AnalyzeButton>
                </ButtonContainer>
              </div>
            )}
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

const ResultContainer = styled.div`
  width: 100%;
  margin-top: 20px;
`;

const ResultBox = styled.div`
  width: 100%;
  background-color: #ffffff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: ${fadeIn} 0.5s ease-out;
  margin-bottom: 20px; /* 박스 간의 세로 간격 추가 */

  &:last-child {
    margin-bottom: 0; /* 마지막 박스는 간격 없음 */
  }

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

const ResultImage = styled.img`
  display: block; /* 중앙 정렬을 위해 block으로 설정 */
  margin-left: auto;
  margin-right: auto;
  max-width: 100%;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const DownloadButton = styled(AnalyzeButton)`
  background-color: #28a745; // 초록색 계열

  &:hover:not(:disabled) {
    background-color: #218838;
  }
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 10px;
  width: 100%;
  margin-top: 20px; /* 버튼 컨테이너 자체에 상단 여백 추가 */

  & > button {
    flex: 1; /* 자식 버튼들의 너비를 동일하게 설정 */
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
