import React from 'react';
import { SajuResult as SajuResultType } from '../../services/sajuApi';
import {
  ResultContainer,
  SectionTitle,
  AnalysisSection,
  SajuGrid,
  SajuPillar,
  PillarTitle,
  Character,
  WuxingGrid,
  WuxingCard,
  ElementName,
  ElementCount,
  ExtendedAnalysisContainer,
  BalanceScore,
  ScoreCircle,
  RecommendationGrid,
  RecommendationCard,
  RecommendationTitle,
  RecommendationList,
  RecommendationItem
} from './styles/SharedStyles';

interface SajuResultProps {
  result: SajuResultType;
}

const SajuResult: React.FC<SajuResultProps> = ({ result }) => {
  return (
    <ResultContainer>
      <h2>{result.basic_info?.name || "사용자"}님의 사주팔자</h2>

      {/* 사주팔자 표시 */}
      <SajuGrid>
        <SajuPillar>
          <PillarTitle>년주</PillarTitle>
          <Character>{result.saju_palja.year_pillar.stem}</Character>
          <Character>{result.saju_palja.year_pillar.branch}</Character>
        </SajuPillar>
        <SajuPillar>
          <PillarTitle>월주</PillarTitle>
          <Character>{result.saju_palja.month_pillar.stem}</Character>
          <Character>{result.saju_palja.month_pillar.branch}</Character>
        </SajuPillar>
        <SajuPillar>
          <PillarTitle>일주</PillarTitle>
          <Character>{result.saju_palja.day_pillar.stem}</Character>
          <Character>{result.saju_palja.day_pillar.branch}</Character>
        </SajuPillar>
        <SajuPillar>
          <PillarTitle>시주</PillarTitle>
          <Character>{result.saju_palja.hour_pillar.stem}</Character>
          <Character>{result.saju_palja.hour_pillar.branch}</Character>
        </SajuPillar>
      </SajuGrid>

      {/* 오행 분석 */}
      <AnalysisSection>
        <SectionTitle>🌟 오행 분석</SectionTitle>

        <WuxingGrid>
          <WuxingCard $element="목">
            <ElementName>목(木)</ElementName>
            <ElementCount>{result.wuxing_analysis.목}</ElementCount>
          </WuxingCard>
          <WuxingCard $element="화">
            <ElementName>화(火)</ElementName>
            <ElementCount>{result.wuxing_analysis.화}</ElementCount>
          </WuxingCard>
          <WuxingCard $element="토">
            <ElementName>토(土)</ElementName>
            <ElementCount>{result.wuxing_analysis.토}</ElementCount>
          </WuxingCard>
          <WuxingCard $element="금">
            <ElementName>금(金)</ElementName>
            <ElementCount>{result.wuxing_analysis.금}</ElementCount>
          </WuxingCard>
          <WuxingCard $element="수">
            <ElementName>수(Water)</ElementName>
            <ElementCount>{result.wuxing_analysis.수}</ElementCount>
          </WuxingCard>
        </WuxingGrid>

        {/* 확장 분석 */}
        {result.wuxing_analysis.extended_analysis && (
          <ExtendedAnalysisContainer>
            <h4 style={{ color: "#2c3e50", textAlign: "center", marginBottom: "20px" }}>
              🔮 상세 오행 분석
            </h4>

            {/* 균형 점수 */}
            <BalanceScore>
              <h5 style={{ color: "#2c3e50", marginBottom: "15px" }}>
                오행 균형 점수
              </h5>
              <ScoreCircle $score={result.wuxing_analysis.extended_analysis.balance_analysis.balance_score}>
                {result.wuxing_analysis.extended_analysis.balance_analysis.balance_score}점
              </ScoreCircle>
              <p style={{ color: "#7f8c8d", margin: 0 }}>
                성격 유형:{" "}
                <strong>
                  {result.wuxing_analysis.extended_analysis.personality_analysis.personality_type}
                </strong>
              </p>
            </BalanceScore>

            {/* 오행별 상세 분석 */}
            <div style={{ marginTop: "20px" }}>
              <SectionTitle>💫 오행별 상세 분석</SectionTitle>
              <p>
                <strong>주도적 오행:</strong>{" "}
                {result.wuxing_analysis.extended_analysis.balance_analysis.dominant_element}
              </p>
              <p>
                <strong>부족한 오행:</strong>{" "}
                {result.wuxing_analysis.extended_analysis.balance_analysis.weakest_element}
              </p>

              {result.wuxing_analysis.extended_analysis.wuxing_details && (
                <div style={{ marginTop: "20px" }}>
                  {Object.entries(result.wuxing_analysis.extended_analysis.wuxing_details).map(
                    ([element, data]: [string, any]) => (
                      <div
                        key={element}
                        style={{
                          background: "white",
                          padding: "15px",
                          margin: "10px 0",
                          borderRadius: "8px",
                          borderLeft: "4px solid #3498db",
                        }}
                      >
                        <strong>
                          {element}: {data.count}개 ({data.percentage}%)
                        </strong>
                        <p style={{ margin: "5px 0 0 0", color: "#7f8c8d" }}>
                          강도: {data.strength} - {data.meaning}
                        </p>
                      </div>
                    )
                  )}
                </div>
              )}
            </div>

            {/* 강점 & 약점 */}
            <div style={{ marginTop: "20px" }}>
              <SectionTitle>✨ 강점 & 약점</SectionTitle>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                <div>
                  <h5 style={{ color: "#27ae60" }}>강점</h5>
                  <ul style={{ listStyle: "none", padding: 0 }}>
                    {result.wuxing_analysis.extended_analysis.personality_analysis?.strengths?.map(
                      (strength: string, index: number) => (
                        <li key={index} style={{ padding: "5px 0", color: "#34495e" }}>
                          ✓ {strength}
                        </li>
                      )
                    )}
                  </ul>
                </div>
                <div>
                  <h5 style={{ color: "#e74c3c" }}>개선점</h5>
                  <ul style={{ listStyle: "none", padding: 0 }}>
                    {result.wuxing_analysis.extended_analysis.personality_analysis?.weaknesses?.map(
                      (weakness: string, index: number) => (
                        <li key={index} style={{ padding: "5px 0", color: "#34495e" }}>
                          ⚠ {weakness}
                        </li>
                      )
                    )}
                  </ul>
                </div>
              </div>
            </div>

            {/* 맞춤형 조언 */}
            <div style={{ marginTop: "20px" }}>
              <SectionTitle>🎯 맞춤형 조언</SectionTitle>
              <RecommendationGrid>
                <RecommendationCard>
                  <RecommendationTitle>🎨 추천 색상</RecommendationTitle>
                  <RecommendationList>
                    {result.wuxing_analysis.extended_analysis.recommendations?.colors?.map(
                      (color: string, index: number) => (
                        <RecommendationItem key={index}>{color}</RecommendationItem>
                      )
                    )}
                  </RecommendationList>
                </RecommendationCard>

                <RecommendationCard>
                  <RecommendationTitle>🧭 유리한 방향</RecommendationTitle>
                  <RecommendationList>
                    {result.wuxing_analysis.extended_analysis.recommendations?.directions?.map(
                      (direction: string, index: number) => (
                        <RecommendationItem key={index}>{direction}</RecommendationItem>
                      )
                    )}
                  </RecommendationList>
                </RecommendationCard>

                <RecommendationCard>
                  <RecommendationTitle>🏃‍♀️ 생활습관</RecommendationTitle>
                  <RecommendationList>
                    {result.wuxing_analysis.extended_analysis.recommendations?.lifestyle?.map(
                      (lifestyle: string, index: number) => (
                        <RecommendationItem key={index}>{lifestyle}</RecommendationItem>
                      )
                    )}
                  </RecommendationList>
                </RecommendationCard>

                <RecommendationCard>
                  <RecommendationTitle>💼 직업 조언</RecommendationTitle>
                  <RecommendationList>
                    {result.wuxing_analysis.extended_analysis.recommendations?.career_advice?.map(
                      (advice: string, index: number) => (
                        <RecommendationItem key={index}>{advice}</RecommendationItem>
                      )
                    )}
                  </RecommendationList>
                </RecommendationCard>

                <RecommendationCard>
                  <RecommendationTitle>💊 건강 관리</RecommendationTitle>
                  <RecommendationList>
                    {result.wuxing_analysis.extended_analysis.recommendations?.health_advice?.map(
                      (advice: string, index: number) => (
                        <RecommendationItem key={index}>{advice}</RecommendationItem>
                      )
                    )}
                  </RecommendationList>
                </RecommendationCard>

                <RecommendationCard>
                  <RecommendationTitle>💑 인간관계</RecommendationTitle>
                  <RecommendationList>
                    {result.wuxing_analysis.extended_analysis.recommendations?.relationship_advice?.map(
                      (advice: string, index: number) => (
                        <RecommendationItem key={index}>{advice}</RecommendationItem>
                      )
                    )}
                  </RecommendationList>
                </RecommendationCard>
              </RecommendationGrid>
            </div>
          </ExtendedAnalysisContainer>
        )}
      </AnalysisSection>

      {/* 기본 해석 */}
      <AnalysisSection>
        <SectionTitle>🌟 성격 분석</SectionTitle>
        <p>{result.interpretations.personality}</p>
      </AnalysisSection>

      <AnalysisSection>
        <SectionTitle>💪 건강운</SectionTitle>
        <p>{result.interpretations.health}</p>
      </AnalysisSection>

      <AnalysisSection>
        <SectionTitle>👥 대인관계</SectionTitle>
        <p>{result.interpretations.relationships}</p>
      </AnalysisSection>

      <AnalysisSection>
        <SectionTitle>💰 재물운</SectionTitle>
        <p>{result.interpretations.wealth}</p>
      </AnalysisSection>
    </ResultContainer>
  );
};

export default SajuResult;