import React from 'react';
import styled from 'styled-components';
import { CompatibilityResult as CompatibilityResultType } from '../../services/compatibilityApi';

interface CompatibilityResultProps {
  result: CompatibilityResultType;
  personsInfo?: {
    person1: {
      name: string;
      birth_date: string;
      gender: string;
    };
    person2: {
      name: string;
      birth_date: string;
      gender: string;
    };
  };
}

const ResultContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin-bottom: 20px;
`;

const ScoreDisplay = styled.div`
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  border-radius: 15px;
`;

const ScoreNumber = styled.div`
  font-size: 4em;
  font-weight: bold;
  color: #e74c3c;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
`;

const Grade = styled.div`
  font-size: 1.5em;
  color: #2c3e50;
  font-weight: bold;
`;

const PersonsInfoContainer = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const PersonInfo = styled.div`
  text-align: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
`;

const PersonName = styled.div`
  font-size: 1.2em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
`;

const PersonBirth = styled.div`
  color: #7f8c8d;
  font-size: 0.9em;
`;

const DetailContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const DetailSection = styled.div`
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
`;

const SectionTitle = styled.h3`
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 15px;
  margin-top: 0;
`;

const ScoreGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 15px;
`;

const ScoreItem = styled.div`
  background: white;
  padding: 10px;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ecf0f1;
`;

const ScoreLabel = styled.div`
  font-size: 0.9em;
  color: #7f8c8d;
  margin-bottom: 5px;
`;

const ScoreValue = styled.div`
  font-size: 1.2em;
  font-weight: bold;
  color: #e74c3c;
`;

const ListItem = styled.div`
  margin-bottom: 8px;
  padding: 8px;
  background: white;
  border-radius: 5px;
  border-left: 4px solid #3498db;
`;

const AdviceSection = styled.div`
  background: #e8f5e8;
  padding: 20px;
  border-radius: 10px;
  border: 2px solid #27ae60;
`;

const CompatibilityResultComponent: React.FC<CompatibilityResultProps> = ({ result, personsInfo }) => {
  return (
    <ResultContainer>
      <ScoreDisplay>
        <ScoreNumber>{result.total_score}점</ScoreNumber>
        <Grade>{result.grade}</Grade>
      </ScoreDisplay>

      {personsInfo && (
        <PersonsInfoContainer>
          <PersonInfo>
            <PersonName>{personsInfo.person1.name}</PersonName>
            <PersonBirth>{personsInfo.person1.birth_date}</PersonBirth>
            <PersonBirth>{personsInfo.person1.gender}</PersonBirth>
          </PersonInfo>
          <PersonInfo>
            <PersonName>{personsInfo.person2.name}</PersonName>
            <PersonBirth>{personsInfo.person2.birth_date}</PersonBirth>
            <PersonBirth>{personsInfo.person2.gender}</PersonBirth>
          </PersonInfo>
        </PersonsInfoContainer>
      )}

      <DetailContainer>
        <DetailSection>
          <SectionTitle>📊 분야별 궁합</SectionTitle>
          <ScoreGrid>
            <ScoreItem>
              <ScoreLabel>연애 궁합</ScoreLabel>
              <ScoreValue>{result.love_compatibility}점</ScoreValue>
            </ScoreItem>
            <ScoreItem>
              <ScoreLabel>결혼 궁합</ScoreLabel>
              <ScoreValue>{result.marriage_compatibility}점</ScoreValue>
            </ScoreItem>
            <ScoreItem>
              <ScoreLabel>사업 궁합</ScoreLabel>
              <ScoreValue>{result.business_compatibility}점</ScoreValue>
            </ScoreItem>
            <ScoreItem>
              <ScoreLabel>우정 궁합</ScoreLabel>
              <ScoreValue>{result.friendship_compatibility}점</ScoreValue>
            </ScoreItem>
          </ScoreGrid>
        </DetailSection>

        <DetailSection>
          <SectionTitle>✨ 궁합의 장점</SectionTitle>
          {result.strengths.map((strength, idx) => (
            <ListItem key={idx}>• {strength}</ListItem>
          ))}
        </DetailSection>
      </DetailContainer>

      {result.weaknesses.length > 0 && (
        <DetailSection style={{ marginBottom: '25px' }}>
          <SectionTitle>⚠️ 주의사항</SectionTitle>
          {result.weaknesses.map((weakness, idx) => (
            <ListItem key={idx} style={{ borderLeftColor: '#e74c3c' }}>• {weakness}</ListItem>
          ))}
        </DetailSection>
      )}

      <AdviceSection>
        <SectionTitle style={{ borderBottomColor: '#27ae60', color: '#27ae60' }}>
          💡 관계 개선 조언
        </SectionTitle>
        {result.advice.map((advice, idx) => (
          <ListItem key={idx} style={{ borderLeftColor: '#27ae60', background: '#f0fff0' }}>
            • {advice}
          </ListItem>
        ))}
      </AdviceSection>
    </ResultContainer>
  );
};

export default CompatibilityResultComponent;