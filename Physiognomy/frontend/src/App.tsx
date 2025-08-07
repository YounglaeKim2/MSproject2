import React, { useState, useCallback } from 'react';
import styled, { createGlobalStyle, keyframes } from 'styled-components';
import axios from 'axios';

// 데이터 구조 정의
interface AnalysisResult {
  totalAnalysis: string;
  goldenAge: string;
  personalityAndPotential: string;
  socialLife: string;
  wealthAndCareer: string;
  successTips: string;
  luckyCharm: {
    message: string;
    dallePrompt: string;
  };
  celebrityLookAlike: string;
  hiddenCharm: string;
  error?: string;
}

// 전역 스타일
const GlobalStyle = createGlobalStyle`
  * {
    box-sizing: border-box;
  }

  body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #f0f0f0;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    margin: 0;
  }
`;

// 메인 앱 컴포넌트
const App: React.FC = () => {
  // 상태 변수들
  const [agree, setAgree] = useState(false);
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // 부적 관련 상태 변수 복원
  const [charmPrompt, setCharmPrompt] = useState<string | null>(null);
  const [analysisId, setAnalysisId] = useState<number | null>(null);
  const [luckyCharmImageUrl, setLuckyCharmImageUrl] = useState<string | null>(null);
  const [isCharmLoading, setIsCharmLoading] = useState(false);
  const [charmError, setCharmError] = useState<string | null>(null);

  // 이미지 변경 핸들러
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImage(file);
      setPreview(URL.createObjectURL(file));
      // 모든 결과 상태 초기화
      setAnalysisResult(null);
      setLuckyCharmImageUrl(null);
      setError(null);
      setCharmError(null);
    }
  };

  // 관상 분석 핸들러
  const handleSubmit = async () => {
    if (!image) {
      setError('이미지를 먼저 선택해주세요.');
      return;
    }
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);
    setLuckyCharmImageUrl(null);
    setCharmError(null);

    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await axios.post('http://localhost:8001/analyze/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const resultData = JSON.parse(response.data.report);
      setAnalysisResult(resultData);
      // 부적 생성을 위한 정보 저장
      setCharmPrompt(response.data.charm_prompt);
      setAnalysisId(response.data.analysis_id);
    } catch (err) {
      setError('분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // 행운의 부적 생성 핸들러 (복원)
  const handleGenerateCharm = async () => {
    if (!charmPrompt || !analysisId) {
        setCharmError('부적을 생성하기 위한 정보가 부족합니다. 먼저 관상 분석을 실행해주세요.');
        return;
    }
    setIsCharmLoading(true);
    setCharmError(null);

    try {
                const response = await axios.post('http://localhost:8001/generate-charm/', { 
            prompt: charmPrompt,
            analysis_id: analysisId
        });
        if (response.data.success) {
            setLuckyCharmImageUrl(`http://localhost:8001${response.data.lucky_charm_image_url}`);
        } else {
            setCharmError(response.data.detail || '부적 생성에 실패했습니다.');
        }
    } catch (err) {
        setCharmError('부적 생성 중 오류가 발생했습니다.');
        console.error(err);
    } finally {
        setIsCharmLoading(false);
    }
  };
  
  // 부적 다운로드 핸들러 (복원)
  const handleDownload = async () => {
    if (!luckyCharmImageUrl) return;
    try {
      const response = await fetch(luckyCharmImageUrl);
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = 'lucky-charm.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("부적 이미지 다운로드 실패:", error);
      setCharmError("이미지를 다운로드하는 중 오류가 발생했습니다.");
    }
  };

  return (
    <>
      <GlobalStyle />
      <AppContainer>
        <Header>
          <Title>AI 관상 분석</Title>
          <Subtitle>당신의 얼굴에 숨겨진 이야기를 발견해보세요</Subtitle>
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

          <UploadBox>
            <input type="file" accept="image/*" onChange={handleImageChange} disabled={!agree || isLoading} />
            <button onClick={handleSubmit} disabled={!agree || !image || isLoading}>
              {isLoading ? '분석 중...' : '결과 보기'}
            </button>
          </UploadBox>

          {preview && <ImagePreview src={preview} alt="Preview" />}
          {error && <ErrorBox>{error}</ErrorBox>}
          {isLoading && <Loader>분석 중입니다...</Loader>}

          {analysisResult && !analysisResult.error && (
            <ResultContainer>
              <ResultCard icon="💡" title="총평" content={analysisResult.totalAnalysis} />
              <ResultCard icon="🌟" title="인생의 황금기" content={analysisResult.goldenAge} />
              <ResultCard icon="👤" title="성격과 잠재력" content={analysisResult.personalityAndPotential} />
              <ResultCard icon="🤝" title="사회생활과 인간관계" content={analysisResult.socialLife} />
              <ResultCard icon="💼" title="재물운과 직업운" content={analysisResult.wealthAndCareer} />
              <ResultCard icon="🚀" title="성공을 위한 조언" content={analysisResult.successTips} />
              <ResultCard icon="💖" title="행운의 메시지" content={analysisResult.luckyCharm.message} />
              <ResultCard icon="✨" title="숨겨진 매력" content={analysisResult.hiddenCharm} />
              <ResultCard icon="🎭" title="유사 유명인/동물상" content={analysisResult.celebrityLookAlike} />
              
              {/* 부적 생성 섹션 */}
              <CharmSection>
                {!luckyCharmImageUrl && (
                    <button onClick={handleGenerateCharm} disabled={isCharmLoading} className="charm-button">
                        {isCharmLoading ? '부적 생성 중...' : '🍀 행운의 부적 생성하기'}
                    </button>
                )}
                {isCharmLoading && <Loader>부적을 만들고 있어요...</Loader>}
                {charmError && <ErrorBox>{charmError}</ErrorBox>}
                {luckyCharmImageUrl && (
                    <>
                        <h3 style={{ color: '#ffdfba' }}>🍀 행운의 부적이 도착했습니다 🍀</h3>
                        <ImagePreview src={luckyCharmImageUrl} alt="Lucky Charm" />
                        <ButtonContainer>
                          <button onClick={handleDownload} className="download-button">부적 다운로드</button>
                          <button disabled className="disabled-button">부적 만들러가기</button>
                        </ButtonContainer>
                    </>
                )}
              </CharmSection>
            </ResultContainer>
          )}

          {analysisResult && analysisResult.error && (
            <ErrorBox>{analysisResult.error}</ErrorBox>
          )}
        </MainContent>
      </AppContainer>
    </>
  );
};

// 스타일 컴포넌트들 (기존과 동일하게 유지)
const AppContainer = styled.div`
  text-align: center;
  padding: 50px 20px;
`;

const Header = styled.header`
  margin-bottom: 50px;
`;

const Title = styled.h1`
  font-size: 3rem;
  color: #ffd700;
  font-weight: 900;
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: #b0c4de;
`;

const MainContent = styled.main`
  max-width: 800px;
  margin: 0 auto;
`;

const Disclaimer = styled.div`
  border: 2px solid #ff4d4f;
  padding: 20px;
  margin-bottom: 30px;
  background-color: rgba(255, 241, 240, 0.1);
  border-radius: 8px;
  width: 100%;

  h3 {
    margin-top: 0;
    color: #ff4d4f;
  }
  p {
    line-height: 1.6;
    color: #ffccc7;
  }
  label {
    display: flex;
    align-items: center;
    font-weight: 500;
    cursor: pointer;
    color: #f0f0f0;
  }
`;

const UploadBox = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);

  input[type="file"] {
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    padding: 20px;
    width: 100%;
    color: #f0f0f0;
    margin-bottom: 20px;
  }

  button {
    background: linear-gradient(135deg, #ffd700, #ffb700);
    color: #1a1a2e;
    border: none;
    padding: 15px 30px;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover:not(:disabled) {
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(255, 215, 0, 0.2);
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
`;

const ImagePreview = styled.img`
  max-width: 100%;
  max-height: 300px;
  border-radius: 15px;
  margin-bottom: 30px;
  border: 3px solid #ffd700;
`;

const Loader = styled.div`
  color: #ffd700;
  font-size: 1.2rem;
  margin: 30px 0;
`;

const ErrorBox = styled.div`
  background: rgba(255, 0, 0, 0.2);
  color: #ffcccc;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
`;

const ResultContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
`;

const ResultCard: React.FC<{ title: string; content: string; icon: string }> = ({ title, content, icon }) => (
  <div style={{ 
    background: 'rgba(255, 255, 255, 0.1)',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    borderRadius: '15px',
    padding: '20px',
    backdropFilter: 'blur(10px)',
    boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
  }}>
    <h3 style={{ color: '#ffdfba', borderBottom: '2px solid #ffdfba', paddingBottom: '10px', marginBottom: '15px' }}>
      <span style={{ marginRight: '10px' }}>{icon}</span>{title}
    </h3>
    <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{content}</p>
  </div>
);

const ButtonContainer = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 20px;

  button {
    flex: 1;
    padding: 15px 30px;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
  }

  .download-button {
    background: linear-gradient(135deg, #28a745, #218838);
    color: white;
    &:hover:not(:disabled) {
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(40, 167, 69, 0.2);
    }
  }

  .disabled-button {
    background: #8c8c8c;
    color: #595959;
    cursor: not-allowed;
  }
`;

const CharmSection = styled.div`
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);

  .charm-button {
    background: linear-gradient(135deg, #28a745, #218838);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover:not(:disabled) {
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(40, 167, 69, 0.2);
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
`;

export default App;
