import React from 'react';
import styled from 'styled-components';
import { SajuAnalysisResult } from '../types/saju';

interface SajuResultProps {
  result: SajuAnalysisResult;
  name?: string;
}

const SajuResult: React.FC<SajuResultProps> = ({ result, name }) => {
  const { palja, wuxing, ten_stars, personality, career, health, relationship, fortune } = result;

  const wuxingColors: { [key: string]: string } = {
    '목': '#4CAF50',
    '화': '#F44336', 
    '토': '#FF9800',
    '금': '#9E9E9E',
    '수': '#2196F3'
  };

  const renderWuxingBar = (element: string, count: number, max: number) => {
    const percentage = max > 0 ? (count / max) * 100 : 0;
    return (
      <WuxingItem key={element}>
        <WuxingLabel>
          <WuxingName color={wuxingColors[element]}>{element}</WuxingName>
          <WuxingCount>{count}</WuxingCount>
        </WuxingLabel>
        <WuxingBarContainer>
          <WuxingBar 
            width={percentage} 
            color={wuxingColors[element]}
          />
        </WuxingBarContainer>
      </WuxingItem>
    );
  };

  const wuxingData = [
    { name: '목', count: wuxing.wood },
    { name: '화', count: wuxing.fire },
    { name: '토', count: wuxing.earth },
    { name: '금', count: wuxing.metal },
    { name: '수', count: wuxing.water }
  ];
  
  const maxWuxing = Math.max(...wuxingData.map(item => item.count));

  return (
    <ResultContainer>
      <ResultHeader>
        <ResultTitle>
          {name ? `${name}님의 사주 분석 결과` : '사주 분석 결과'}
        </ResultTitle>
      </ResultHeader>

      {/* 사주팔자 */}
      <Section>
        <SectionTitle>사주팔자 (四柱八字)</SectionTitle>
        <PaljaContainer>
          <PaljaColumn>
            <PaljaHeader>시주</PaljaHeader>
            <PaljaChar>{palja.hour_gan}</PaljaChar>
            <PaljaChar>{palja.hour_ji}</PaljaChar>
          </PaljaColumn>
          <PaljaColumn>
            <PaljaHeader>일주</PaljaHeader>
            <PaljaChar main>{palja.day_gan}</PaljaChar>
            <PaljaChar main>{palja.day_ji}</PaljaChar>
          </PaljaColumn>
          <PaljaColumn>
            <PaljaHeader>월주</PaljaHeader>
            <PaljaChar>{palja.month_gan}</PaljaChar>
            <PaljaChar>{palja.month_ji}</PaljaChar>
          </PaljaColumn>
          <PaljaColumn>
            <PaljaHeader>년주</PaljaHeader>
            <PaljaChar>{palja.year_gan}</PaljaChar>
            <PaljaChar>{palja.year_ji}</PaljaChar>
          </PaljaColumn>
        </PaljaContainer>
      </Section>

      {/* 오행 분석 */}
      <Section>
        <SectionTitle>오행 분석</SectionTitle>
        <WuxingContainer>
          <WuxingChart>
            {wuxingData.map(item => renderWuxingBar(item.name, item.count, maxWuxing))}
          </WuxingChart>
          <WuxingInfo>
            <WuxingDetail>
              <strong>일간 강약:</strong> {wuxing.strength === 'strong' ? '신강' : '신약'}
            </WuxingDetail>
            <WuxingDetail>
              <strong>용신:</strong> <span style={{color: wuxingColors[wuxing.use_god]}}>{wuxing.use_god}</span>
            </WuxingDetail>
            <WuxingDetail>
              <strong>기신:</strong> <span style={{color: wuxingColors[wuxing.avoid_god]}}>{wuxing.avoid_god}</span>
            </WuxingDetail>
          </WuxingInfo>
        </WuxingContainer>
      </Section>

      {/* 성격 분석 */}
      <Section>
        <SectionTitle>성격 분석</SectionTitle>
        <AnalysisCard>
          <AnalysisItem>
            <AnalysisLabel>기본 성향</AnalysisLabel>
            <AnalysisContent>{personality.basic_nature}</AnalysisContent>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>장점</AnalysisLabel>
            <TagList>
              {personality.strengths.map((strength, index) => (
                <Tag key={index} type="positive">{strength}</Tag>
              ))}
            </TagList>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>주의점</AnalysisLabel>
            <TagList>
              {personality.weaknesses.map((weakness, index) => (
                <Tag key={index} type="warning">{weakness}</Tag>
              ))}
            </TagList>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>조언</AnalysisLabel>
            <AdviceList>
              {personality.recommendations.map((advice, index) => (
                <AdviceItem key={index}>{advice}</AdviceItem>
              ))}
            </AdviceList>
          </AnalysisItem>
        </AnalysisCard>
      </Section>

      {/* 직업운 */}
      <Section>
        <SectionTitle>직업운</SectionTitle>
        <AnalysisCard>
          <AnalysisItem>
            <AnalysisLabel>적성 분야</AnalysisLabel>
            <TagList>
              {career.suitable_fields.map((field, index) => (
                <Tag key={index} type="career">{field}</Tag>
              ))}
            </TagList>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>성향</AnalysisLabel>
            <AnalysisContent>{career.career_tendency}</AnalysisContent>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>성공 요인</AnalysisLabel>
            <AdviceList>
              {career.success_factors.map((factor, index) => (
                <AdviceItem key={index}>{factor}</AdviceItem>
              ))}
            </AdviceList>
          </AnalysisItem>
        </AnalysisCard>
      </Section>

      {/* 건강운 */}
      <Section>
        <SectionTitle>건강운</SectionTitle>
        <AnalysisCard>
          {health.strong_organs.length > 0 && (
            <AnalysisItem>
              <AnalysisLabel>강한 장기</AnalysisLabel>
              <TagList>
                {health.strong_organs.map((organ, index) => (
                  <Tag key={index} type="positive">{organ}</Tag>
                ))}
              </TagList>
            </AnalysisItem>
          )}
          {health.weak_organs.length > 0 && (
            <AnalysisItem>
              <AnalysisLabel>주의할 장기</AnalysisLabel>
              <TagList>
                {health.weak_organs.map((organ, index) => (
                  <Tag key={index} type="warning">{organ}</Tag>
                ))}
              </TagList>
            </AnalysisItem>
          )}
          <AnalysisItem>
            <AnalysisLabel>건강 조언</AnalysisLabel>
            <AdviceList>
              {health.health_advice.map((advice, index) => (
                <AdviceItem key={index}>{advice}</AdviceItem>
              ))}
            </AdviceList>
          </AnalysisItem>
        </AnalysisCard>
      </Section>

      {/* 대인관계운 */}
      <Section>
        <SectionTitle>대인관계운</SectionTitle>
        <AnalysisCard>
          <AnalysisItem>
            <AnalysisLabel>관계 스타일</AnalysisLabel>
            <AnalysisContent>{relationship.relationship_style}</AnalysisContent>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>사회적 성향</AnalysisLabel>
            <AnalysisContent>{relationship.social_tendency}</AnalysisContent>
          </AnalysisItem>
          {relationship.compatibility.length > 0 && (
            <AnalysisItem>
              <AnalysisLabel>좋은 궁합</AnalysisLabel>
              <AdviceList>
                {relationship.compatibility.map((comp, index) => (
                  <AdviceItem key={index}>{comp}</AdviceItem>
                ))}
              </AdviceList>
            </AnalysisItem>
          )}
        </AnalysisCard>
      </Section>

      {/* 재물운 */}
      <Section>
        <SectionTitle>재물운</SectionTitle>
        <AnalysisCard>
          <AnalysisItem>
            <AnalysisLabel>재물 성향</AnalysisLabel>
            <AnalysisContent>{fortune.wealth_tendency}</AnalysisContent>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>수입 스타일</AnalysisLabel>
            <AnalysisContent>{fortune.income_style}</AnalysisContent>
          </AnalysisItem>
          <AnalysisItem>
            <AnalysisLabel>투자 조언</AnalysisLabel>
            <AdviceList>
              {fortune.investment_advice.map((advice, index) => (
                <AdviceItem key={index}>{advice}</AdviceItem>
              ))}
            </AdviceList>
          </AnalysisItem>
        </AnalysisCard>
      </Section>
    </ResultContainer>
  );
};

// 스타일 컴포넌트들
const ResultContainer = styled.div`
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
`;

const ResultHeader = styled.div`
  text-align: center;
  margin-bottom: 40px;
`;

const ResultTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
`;

const Section = styled.div`
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
`;

const SectionTitle = styled.h2`
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 3px solid #667eea;
`;

const PaljaContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 20px 0;
  
  @media (max-width: 768px) {
    gap: 10px;
  }
`;

const PaljaColumn = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
`;

const PaljaHeader = styled.div`
  font-weight: bold;
  color: #666;
  font-size: 0.9rem;
`;

const PaljaChar = styled.div<{ main?: boolean }>`
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  background: ${props => props.main ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#f8f9fa'};
  color: ${props => props.main ? 'white' : '#333'};
  border: ${props => props.main ? 'none' : '2px solid #e9ecef'};
  
  @media (max-width: 768px) {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
`;

const WuxingContainer = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const WuxingChart = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const WuxingItem = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const WuxingLabel = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 60px;
`;

const WuxingName = styled.span<{ color: string }>`
  font-weight: bold;
  color: ${props => props.color};
`;

const WuxingCount = styled.span`
  font-size: 0.9rem;
  color: #666;
`;

const WuxingBarContainer = styled.div`
  flex: 1;
  height: 20px;
  background: #f1f3f5;
  border-radius: 10px;
  overflow: hidden;
`;

const WuxingBar = styled.div<{ width: number; color: string }>`
  height: 100%;
  width: ${props => props.width}%;
  background: ${props => props.color};
  transition: width 0.8s ease;
`;

const WuxingInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
`;

const WuxingDetail = styled.div`
  font-size: 1rem;
  line-height: 1.5;
`;

const AnalysisCard = styled.div`
  display: flex;
  flex-direction: column;
  gap: 25px;
`;

const AnalysisItem = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const AnalysisLabel = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: #495057;
  margin-bottom: 5px;
`;

const AnalysisContent = styled.p`
  font-size: 1rem;
  line-height: 1.6;
  color: #666;
`;

const TagList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
`;

const Tag = styled.span<{ type: 'positive' | 'warning' | 'career' }>`
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  background: ${props => {
    switch (props.type) {
      case 'positive': return '#e8f5e8';
      case 'warning': return '#fff3cd';
      case 'career': return '#e3f2fd';
      default: return '#f8f9fa';
    }
  }};
  color: ${props => {
    switch (props.type) {
      case 'positive': return '#2e7d32';
      case 'warning': return '#f57c00';
      case 'career': return '#1976d2';
      default: return '#666';
    }
  }};
`;

const AdviceList = styled.ul`
  margin: 0;
  padding-left: 20px;
`;

const AdviceItem = styled.li`
  font-size: 0.95rem;
  line-height: 1.6;
  color: #666;
  margin-bottom: 8px;
`;

export default SajuResult;