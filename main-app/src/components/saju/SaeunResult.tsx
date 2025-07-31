import React from 'react';
import { SaeunResult as SaeunResultType } from '../../services/sajuApi';
import {
  ResultContainer,
  SectionTitle,
  AnalysisSection,
  BalanceScore,
  ScoreCircle
} from './styles/SharedStyles';

interface SaeunResultProps {
  result: SaeunResultType;
}

const SaeunResult: React.FC<SaeunResultProps> = ({ result }) => {
  return (
    <ResultContainer style={{ marginTop: "30px" }}>
      <SectionTitle
        style={{
          textAlign: "center",
          fontSize: "2rem",
          marginBottom: "30px",
        }}
      >
        ⏰ {result.basic_info.target_year}년 세운 분석 결과
      </SectionTitle>

      {/* 연간 세운 정보 */}
      <AnalysisSection>
        <SectionTitle>
          📅 {result.saeun_analysis.target_year}년 연간 세운
        </SectionTitle>
        <div
          style={{
            background: "linear-gradient(135deg, #4caf50, #2e7d32)",
            color: "white",
            padding: "20px",
            borderRadius: "15px",
            textAlign: "center",
            marginBottom: "20px",
          }}
        >
          <h3 style={{ margin: "0 0 10px 0" }}>
            {result.saeun_analysis.yearly_saeun.gan}
            {result.saeun_analysis.yearly_saeun.ji}
          </h3>
          <p style={{ margin: "5px 0", fontSize: "14px", opacity: "0.9" }}>
            ({result.saeun_analysis.yearly_saeun.gan_wuxing}·
            {result.saeun_analysis.yearly_saeun.ji_wuxing})
          </p>
        </div>
      </AnalysisSection>

      {/* 전체 운세 요약 */}
      <AnalysisSection>
        <SectionTitle>🎯 종합 운세 점수</SectionTitle>
        <BalanceScore>
          <ScoreCircle $score={result.saeun_analysis.annual_score.normalized_score}>
            {result.saeun_analysis.annual_score.normalized_score}점
          </ScoreCircle>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "20px",
              marginTop: "20px",
            }}
          >
            <div>
              <h5 style={{ color: "#27ae60", marginBottom: "10px" }}>
                🍀 최고의 달
              </h5>
              <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                {result.saeun_analysis.critical_periods.best_months.map(
                  (monthData, index) => (
                    <span
                      key={index}
                      style={{
                        background: "#27ae60",
                        color: "white",
                        padding: "4px 12px",
                        borderRadius: "15px",
                        fontSize: "14px",
                      }}
                    >
                      {monthData.month}월 ({monthData.level})
                    </span>
                  )
                )}
              </div>
            </div>

            <div>
              <h5 style={{ color: "#e74c3c", marginBottom: "10px" }}>
                ⚠️ 주의할 달
              </h5>
              <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                {result.saeun_analysis.critical_periods.caution_months.map(
                  (monthData, index) => (
                    <span
                      key={index}
                      style={{
                        background: "#e74c3c",
                        color: "white",
                        padding: "4px 12px",
                        borderRadius: "15px",
                        fontSize: "14px",
                      }}
                    >
                      {monthData.month}월 ({monthData.level})
                    </span>
                  )
                )}
              </div>
            </div>
          </div>
        </BalanceScore>
      </AnalysisSection>

      {/* 월별 세운 상세 */}
      <AnalysisSection>
        <SectionTitle>📊 월별 운세 상세 분석</SectionTitle>
        <div style={{ display: "grid", gap: "20px" }}>
          {result.saeun_analysis.monthly_saeun.map((monthData, index) => {
            const interactionData = result.saeun_analysis.saeun_interaction.monthly.find(
              (m) => m.month === monthData.month
            );
            return (
              <div
                key={index}
                style={{
                  border: "2px solid #e9ecef",
                  borderRadius: "15px",
                  padding: "20px",
                  background: "white",
                  boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
                  borderColor:
                    interactionData?.fortune_level === "대길"
                      ? "#28a745"
                      : interactionData?.fortune_level === "소길"
                      ? "#17a2b8"
                      : interactionData?.fortune_level === "평운"
                      ? "#ffc107"
                      : interactionData?.fortune_level === "소흉"
                      ? "#fd7e14"
                      : "#dc3545",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "15px",
                    flexWrap: "wrap",
                    gap: "10px"
                  }}
                >
                  <div>
                    <h4 style={{ margin: 0, color: "#2c3e50" }}>
                      {monthData.month}월
                    </h4>
                    <p
                      style={{
                        margin: "5px 0",
                        color: "#6c757d",
                        fontSize: "14px",
                      }}
                    >
                      {monthData.gan}{monthData.ji} ({monthData.gan_wuxing}·
                      {monthData.ji_wuxing})
                    </p>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "15px",
                    }}
                  >
                    <div
                      style={{
                        padding: "8px 16px",
                        borderRadius: "20px",
                        fontWeight: "bold",
                        fontSize: "14px",
                        background:
                          interactionData?.fortune_level === "대길"
                            ? "#28a745"
                            : interactionData?.fortune_level === "소길"
                            ? "#17a2b8"
                            : interactionData?.fortune_level === "평운"
                            ? "#ffc107"
                            : interactionData?.fortune_level === "소흉"
                            ? "#fd7e14"
                            : "#dc3545",
                        color: "white",
                      }}
                    >
                      {interactionData?.fortune_level || "평운"}
                    </div>
                    <div
                      style={{
                        fontSize: "18px",
                        fontWeight: "bold",
                        color: "#2c3e50",
                      }}
                    >
                      {interactionData?.score || 0}점
                    </div>
                  </div>
                </div>

                {/* 특징 */}
                <div style={{ marginBottom: "15px" }}>
                  <p
                    style={{
                      margin: 0,
                      fontSize: "15px",
                      lineHeight: "1.5",
                      color: "#495057",
                    }}
                  >
                    {interactionData?.characteristics?.join(", ") ||
                      "평상시와 같은 운세입니다"}
                  </p>
                </div>

                {/* 기회와 주의사항 */}
                {interactionData &&
                  (interactionData.opportunities.length > 0 ||
                    interactionData.warnings.length > 0) && (
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns: "1fr 1fr",
                        gap: "15px",
                        marginTop: "15px",
                      }}
                    >
                      {interactionData.opportunities.length > 0 && (
                        <div>
                          <strong style={{ color: "#28a745", fontSize: "13px" }}>
                            🍀 기회:
                          </strong>
                          <ul
                            style={{
                              margin: "5px 0",
                              paddingLeft: "15px",
                              fontSize: "12px",
                            }}
                          >
                            {interactionData.opportunities.map((opportunity, i) => (
                              <li
                                key={i}
                                style={{
                                  color: "#495057",
                                  marginBottom: "2px",
                                }}
                              >
                                {opportunity}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {interactionData.warnings.length > 0 && (
                        <div>
                          <strong style={{ color: "#dc3545", fontSize: "13px" }}>
                            ⚠️ 주의사항:
                          </strong>
                          <ul
                            style={{
                              margin: "5px 0",
                              paddingLeft: "15px",
                              fontSize: "12px",
                            }}
                          >
                            {interactionData.warnings.map((warning, i) => (
                              <li
                                key={i}
                                style={{
                                  color: "#495057",
                                  marginBottom: "2px",
                                }}
                              >
                                {warning}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
              </div>
            );
          })}
        </div>
      </AnalysisSection>

      {/* 연간 조언 */}
      <AnalysisSection>
        <SectionTitle>
          💡 {result.saeun_analysis.target_year}년 종합 조언
        </SectionTitle>
        <div
          style={{
            background: "#f8f9fa",
            padding: "20px",
            borderRadius: "10px",
            borderLeft: "5px solid #4caf50",
          }}
        >
          <p
            style={{
              margin: 0,
              fontSize: "16px",
              lineHeight: "1.6",
              color: "#495057",
            }}
          >
            {result.saeun_analysis.summary}
          </p>
        </div>
      </AnalysisSection>
    </ResultContainer>
  );
};

export default SaeunResult;