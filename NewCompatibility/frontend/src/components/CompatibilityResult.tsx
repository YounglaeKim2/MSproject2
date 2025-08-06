import React from "react";
import styled from "styled-components";
import { CompatibilityData } from "../types/compatibility";

const ResultContainer = styled.div`
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 20px;
  padding: 30px;
  margin-top: 30px;
  animation: fadeIn 0.5s ease-in-out;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: 30px;
`;

const Title = styled.h2`
  color: #333;
  font-size: 2rem;
  margin-bottom: 10px;
`;

const NamesSubtitle = styled.h3`
  color: #666;
  font-size: 1.3rem;
  margin-bottom: 15px;
`;

const Summary = styled.div`
  background: white;
  padding: 25px;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: 1.1rem;
  line-height: 1.6;
  color: #444;
  text-align: center;
`;

const ScoresContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const ScoreCard = styled.div<{ $score: number }>`
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  border-left: 5px solid
    ${(props) =>
      props.$score >= 70
        ? "#28a745"  // 좋은 궁합 (70-100) - 녹색
        : "#dc3545"}; // 나쁜 궁합 (0-30) - 빨간색
`;

const ScoreTitle = styled.h4`
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
`;

const ScoreValue = styled.div<{ $score: number }>`
  font-size: 2.5rem;
  font-weight: bold;
  color: ${(props) =>
    props.$score >= 70
      ? "#28a745"  // 좋은 궁합 (70-100) - 녹색
      : "#dc3545"}; // 나쁜 궁합 (0-30) - 빨간색
  margin-bottom: 5px;
`;

const ScoreLabel = styled.div`
  font-size: 0.8rem;
  color: #888;
`;

const AnalysisSection = styled.div`
  background: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
`;

const SectionTitle = styled.h4`
  color: #333;
  margin-bottom: 15px;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const ItemList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const Item = styled.li`
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  color: #555;
  line-height: 1.5;

  &:last-child {
    border-bottom: none;
  }

  &:before {
    content: "•";
    color: #007bff;
    font-weight: bold;
    margin-right: 10px;
  }
`;

const DetailedAnalysis = styled.div`
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #666;
  white-space: pre-line;
`;

const ButtonContainer = styled.div`
  text-align: center;
  margin-top: 30px;
`;

const ResetButton = styled.button`
  background: linear-gradient(45deg, #6c757d, #495057);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: linear-gradient(45deg, #495057, #343a40);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(108, 117, 125, 0.3);
  }
`;

const getScoreDescription = (score: number): string => {
  if (score >= 70) {
    // 좋은 궁합 (70-100점)
    if (score >= 90) return "완벽한 궁합 ✨";
    if (score >= 80) return "매우 좋은 궁합 💕";
    return "좋은 궁합 💖";
  } else {
    // 나쁜 궁합 (0-30점)
    if (score <= 10) return "매우 어려운 관계 ⚠️";
    if (score <= 20) return "어려운 관계 🤔";
    return "힘든 관계 😔";
  }
};

interface Props {
  data: CompatibilityData;
  onReset: () => void;
}

const CompatibilityResult: React.FC<Props> = ({ data, onReset }) => {
  const { compatibility_score, analysis_details, person1_name, person2_name } =
    data;

  return (
    <ResultContainer>
      <Header>
        <Title>🎉 궁합 분석 결과</Title>
        <NamesSubtitle>
          {person1_name} ♥ {person2_name}
        </NamesSubtitle>
      </Header>

      <Summary>{data.summary}</Summary>

      <ScoresContainer>
        <ScoreCard $score={compatibility_score.overall}>
          <ScoreTitle>전체 궁합</ScoreTitle>
          <ScoreValue $score={compatibility_score.overall}>
            {compatibility_score.overall}
          </ScoreValue>
          <ScoreLabel>
            {getScoreDescription(compatibility_score.overall)}
          </ScoreLabel>
        </ScoreCard>

        <ScoreCard $score={compatibility_score.love}>
          <ScoreTitle>연애 궁합</ScoreTitle>
          <ScoreValue $score={compatibility_score.love}>
            {compatibility_score.love}
          </ScoreValue>
          <ScoreLabel>
            {getScoreDescription(compatibility_score.love)}
          </ScoreLabel>
        </ScoreCard>

        <ScoreCard $score={compatibility_score.marriage}>
          <ScoreTitle>결혼 궁합</ScoreTitle>
          <ScoreValue $score={compatibility_score.marriage}>
            {compatibility_score.marriage}
          </ScoreValue>
          <ScoreLabel>
            {getScoreDescription(compatibility_score.marriage)}
          </ScoreLabel>
        </ScoreCard>

        <ScoreCard $score={compatibility_score.communication}>
          <ScoreTitle>소통 궁합</ScoreTitle>
          <ScoreValue $score={compatibility_score.communication}>
            {compatibility_score.communication}
          </ScoreValue>
          <ScoreLabel>
            {getScoreDescription(compatibility_score.communication)}
          </ScoreLabel>
        </ScoreCard>

        <ScoreCard $score={compatibility_score.values}>
          <ScoreTitle>가치관 궁합</ScoreTitle>
          <ScoreValue $score={compatibility_score.values}>
            {compatibility_score.values}
          </ScoreValue>
          <ScoreLabel>
            {getScoreDescription(compatibility_score.values)}
          </ScoreLabel>
        </ScoreCard>
      </ScoresContainer>

      {analysis_details.strengths.length > 0 && (
        <AnalysisSection>
          <SectionTitle>💪 강점</SectionTitle>
          <ItemList>
            {analysis_details.strengths.map((strength, index) => (
              <Item key={index}>{strength}</Item>
            ))}
          </ItemList>
        </AnalysisSection>
      )}

      {analysis_details.weaknesses.length > 0 && (
        <AnalysisSection>
          <SectionTitle>⚠️ 주의점</SectionTitle>
          <ItemList>
            {analysis_details.weaknesses.map((weakness, index) => (
              <Item key={index}>{weakness}</Item>
            ))}
          </ItemList>
        </AnalysisSection>
      )}

      {analysis_details.advice.length > 0 && (
        <AnalysisSection>
          <SectionTitle>💡 조언</SectionTitle>
          <ItemList>
            {analysis_details.advice.map((advice, index) => (
              <Item key={index}>{advice}</Item>
            ))}
          </ItemList>
        </AnalysisSection>
      )}

      {analysis_details.relationship_tips.length > 0 && (
        <AnalysisSection>
          <SectionTitle>💖 관계 팁</SectionTitle>
          <ItemList>
            {analysis_details.relationship_tips.map((tip, index) => (
              <Item key={index}>{tip}</Item>
            ))}
          </ItemList>
        </AnalysisSection>
      )}

      <AnalysisSection>
        <SectionTitle>📝 상세 분석</SectionTitle>
        <DetailedAnalysis>{data.detailed_analysis}</DetailedAnalysis>
      </AnalysisSection>

      <ButtonContainer>
        <ResetButton onClick={onReset}>새로운 궁합 분석하기</ResetButton>
      </ButtonContainer>
    </ResultContainer>
  );
};

export default CompatibilityResult;
