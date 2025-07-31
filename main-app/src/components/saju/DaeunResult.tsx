import React from 'react';
import { DaeunResult as DaeunResultType } from '../../services/sajuApi';
import {
  ResultContainer,
  SectionTitle,
  AnalysisSection
} from './styles/SharedStyles';

interface DaeunResultProps {
  result: DaeunResultType;
}

const DaeunResult: React.FC<DaeunResultProps> = ({ result }) => {
  return (
    <ResultContainer style={{ marginTop: "30px" }}>
      <SectionTitle
        style={{
          textAlign: "center",
          fontSize: "2rem",
          marginBottom: "30px",
        }}
      >
        🌟 대운 분석 결과
      </SectionTitle>

      {/* 기본 정보 */}
      <AnalysisSection>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "20px",
            flexWrap: "wrap",
            gap: "20px"
          }}
        >
          <div>
            <strong>현재 나이:</strong>{" "}
            {result.daeun_analysis.current_age}세
          </div>
          <div>
            <strong>대운 시작:</strong>{" "}
            {result.daeun_analysis.daeun_start_age}세부터
          </div>
          <div>
            <strong>진행 방향:</strong>{" "}
            {result.daeun_analysis.is_forward ? "순행" : "역행"}
          </div>
        </div>
      </AnalysisSection>

      {/* 대운 타임라인 */}
      <AnalysisSection>
        <SectionTitle>📅 인생 대운 타임라인</SectionTitle>
        <div style={{ display: "grid", gap: "20px" }}>
          {result.daeun_analysis.daeun_list.map((daeun, index) => (
            <div
              key={index}
              style={{
                border: daeun.is_current
                  ? "3px solid #f093fb"
                  : "2px solid #e9ecef",
                borderRadius: "15px",
                padding: "20px",
                background: daeun.is_current
                  ? "linear-gradient(135deg, #f093fb22, #f5576c22)"
                  : "white",
                boxShadow: daeun.is_current
                  ? "0 5px 20px rgba(240, 147, 251, 0.3)"
                  : "0 2px 10px rgba(0,0,0,0.1)",
                position: "relative",
              }}
            >
              {daeun.is_current && (
                <div
                  style={{
                    position: "absolute",
                    top: "-10px",
                    right: "20px",
                    background: "#f093fb",
                    color: "white",
                    padding: "5px 15px",
                    borderRadius: "20px",
                    fontSize: "12px",
                    fontWeight: "bold",
                  }}
                >
                  현재 대운
                </div>
              )}

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
                    {daeun.period}
                  </h4>
                  <p
                    style={{
                      margin: "5px 0",
                      color: "#6c757d",
                      fontSize: "14px",
                    }}
                  >
                    {daeun.gan}{daeun.ji} ({daeun.gan_wuxing}·{daeun.ji_wuxing})
                  </p>
                </div>
                <div
                  style={{
                    padding: "8px 16px",
                    borderRadius: "20px",
                    fontWeight: "bold",
                    fontSize: "14px",
                    background:
                      daeun.fortune_level === "대길"
                        ? "#28a745"
                        : daeun.fortune_level === "소길"
                        ? "#17a2b8"
                        : daeun.fortune_level === "평운"
                        ? "#ffc107"
                        : daeun.fortune_level === "소흉"
                        ? "#fd7e14"
                        : "#dc3545",
                    color: "white",
                  }}
                >
                  {daeun.fortune_level}
                </div>
              </div>

              {/* 특징 */}
              <div style={{ marginBottom: "15px" }}>
                <strong style={{ color: "#495057", fontSize: "14px" }}>
                  특징:
                </strong>
                <div
                  style={{
                    marginTop: "8px",
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "8px",
                  }}
                >
                  {daeun.characteristics.map((char, i) => (
                    <span
                      key={i}
                      style={{
                        background: "#e9ecef",
                        padding: "4px 12px",
                        borderRadius: "15px",
                        fontSize: "13px",
                        color: "#495057",
                      }}
                    >
                      {char}
                    </span>
                  ))}
                </div>
              </div>

              {/* 주요 이벤트 */}
              <div style={{ marginBottom: "15px" }}>
                <strong style={{ color: "#495057", fontSize: "14px" }}>
                  주요 이벤트:
                </strong>
                <ul style={{ margin: "8px 0", paddingLeft: "20px" }}>
                  {daeun.major_events.map((event, i) => (
                    <li
                      key={i}
                      style={{
                        fontSize: "13px",
                        color: "#6c757d",
                        marginBottom: "4px",
                      }}
                    >
                      {event}
                    </li>
                  ))}
                </ul>
              </div>

              {/* 조언 */}
              <div
                style={{
                  background: "#f8f9fa",
                  padding: "12px",
                  borderRadius: "8px",
                  borderLeft: "4px solid #17a2b8",
                }}
              >
                <strong style={{ color: "#495057", fontSize: "14px" }}>
                  조언:
                </strong>
                <p
                  style={{
                    margin: "8px 0 0 0",
                    fontSize: "13px",
                    color: "#6c757d",
                    lineHeight: "1.5",
                  }}
                >
                  {daeun.advice}
                </p>
              </div>
            </div>
          ))}
        </div>
      </AnalysisSection>
    </ResultContainer>
  );
};

export default DaeunResult;