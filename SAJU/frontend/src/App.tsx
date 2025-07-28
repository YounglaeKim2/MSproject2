import React, { useState } from "react";
import styled from "styled-components";
import axios from "axios";

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
`;

const Title = styled.h1`
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 2.5rem;
`;

const Form = styled.form`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;

  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  background-color: white;

  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

const Button = styled.button`
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ResultContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
`;

const SajuGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin: 20px 0;
  text-align: center;
`;

const SajuPillar = styled.div`
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 2px solid #e1e8ed;
`;

const PillarTitle = styled.div`
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
`;

const Character = styled.div`
  font-size: 24px;
  font-weight: bold;
  margin: 5px 0;
  color: #e74c3c;
`;

const AnalysisSection = styled.div`
  margin: 30px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
`;

const SectionTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
`;

const WuxingGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin: 20px 0;
`;

const WuxingCard = styled.div<{ element: string }>`
  background: ${(props) => {
    switch (props.element) {
      case "목":
        return "linear-gradient(135deg, #2ecc71, #27ae60)";
      case "화":
        return "linear-gradient(135deg, #e74c3c, #c0392b)";
      case "토":
        return "linear-gradient(135deg, #f39c12, #e67e22)";
      case "금":
        return "linear-gradient(135deg, #95a5a6, #7f8c8d)";
      case "수":
        return "linear-gradient(135deg, #3498db, #2980b9)";
      default:
        return "#f8f9fa";
    }
  }};
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
`;

const ElementName = styled.div`
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const ElementCount = styled.div`
  font-size: 24px;
  font-weight: bold;
`;

const ExtendedAnalysisContainer = styled.div`
  background: #f8f9fa;
  padding: 25px;
  border-radius: 15px;
  margin: 20px 0;
`;

const BalanceScore = styled.div`
  text-align: center;
  margin: 20px 0;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const ScoreCircle = styled.div<{ score: number }>`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    #3498db 0deg,
    #3498db ${(props) => props.score * 3.6}deg,
    #ecf0f1 ${(props) => props.score * 3.6}deg,
    #ecf0f1 360deg
  );
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
`;

const RecommendationGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
`;

const RecommendationCard = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const RecommendationTitle = styled.h4`
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 16px;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 8px;
`;

const RecommendationList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const RecommendationItem = styled.li`
  padding: 5px 0;
  color: #34495e;

  &:before {
    content: "✓ ";
    color: #27ae60;
    font-weight: bold;
  }
`;

interface FormData {
  year: number | "";
  month: number | "";
  day: number | "";
  hour: number | "";
  gender: string;
  name: string;
}

interface SajuResult {
  basic_info: any;
  saju_palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  wuxing_analysis: {
    목: number;
    화: number;
    토: number;
    금: number;
    수: number;
    extended_analysis?: {
      balance_analysis: {
        balance_score: number;
        excessive_elements: string[];
        deficient_elements: string[];
        dominant_element: string;
        weakest_element: string;
      };
      personality_analysis: {
        personality_type: string;
        strengths: string[];
        weaknesses: string[];
        dominant_traits: string[];
        advice: string;
      };
      recommendations: {
        colors: string[];
        directions: string[];
        lifestyle: string[];
        foods: string[];
        activities: string[];
      };
      wuxing_details: {
        [element: string]: {
          count: number;
          percentage: number;
          strength: string;
          meaning: string;
          characteristics: string[];
        };
      };
    };
  };
  interpretations: {
    personality: string;
    career: string;
    health: string;
    relationships: string;
    wealth: string;
  };
}

function App() {
  const [formData, setFormData] = useState<FormData>({
    year: "",
    month: "",
    day: "",
    hour: "",
    gender: "male",
    name: "",
  });

  const [result, setResult] = useState<SajuResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "year" || name === "month" || name === "day" || name === "hour"
          ? value === ""
            ? ""
            : parseInt(value)
          : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      console.log("요청 데이터:", formData);
      const response = await axios.post(
        "http://localhost:8000/api/v1/saju/analyze",
        formData
      );
      console.log("API 응답:", response.data);
      setResult(response.data);
    } catch (err: any) {
      console.error("API 오류:", err);
      console.error("응답 데이터:", err.response?.data);
      setError(err.response?.data?.detail || "분석 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title>🔮 사주팔자 분석 서비스</Title>

      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label>이름</Label>
          <Input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="이름을 입력하세요"
            required
          />
        </FormGroup>

        <FormGroup>
          <Label>생년월일</Label>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: "10px",
            }}
          >
            <Input
              type="number"
              name="year"
              value={formData.year}
              onChange={handleInputChange}
              placeholder="년 (예: 1990)"
              min="1900"
              max="2100"
              required
            />
            <Input
              type="number"
              name="month"
              value={formData.month}
              onChange={handleInputChange}
              placeholder="월 (1-12)"
              min="1"
              max="12"
              required
            />
            <Input
              type="number"
              name="day"
              value={formData.day}
              onChange={handleInputChange}
              placeholder="일 (1-31)"
              min="1"
              max="31"
              required
            />
          </div>
        </FormGroup>

        <FormGroup>
          <Label>태어난 시간</Label>
          <Select
            name="hour"
            value={formData.hour}
            onChange={handleInputChange}
            required
          >
            <option value="">시간을 선택하세요</option>
            {Array.from({ length: 24 }, (_, i) => (
              <option key={i} value={i}>
                {i}시
              </option>
            ))}
          </Select>
        </FormGroup>

        <FormGroup>
          <Label>성별</Label>
          <Select
            name="gender"
            value={formData.gender}
            onChange={handleInputChange}
          >
            <option value="male">남성</option>
            <option value="female">여성</option>
          </Select>
        </FormGroup>

        <Button type="submit" disabled={loading}>
          {loading ? "분석 중..." : "사주 분석하기"}
        </Button>
      </Form>

      {error && (
        <div
          style={{
            padding: "20px",
            background: "#fee",
            color: "#c33",
            borderRadius: "8px",
            marginBottom: "20px",
          }}
        >
          {error}
        </div>
      )}

      {result && (
        <ResultContainer>
          <h2>{result.basic_info?.name || "사용자"}님의 사주팔자</h2>

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

          <AnalysisSection>
            <SectionTitle>� 오행 분석</SectionTitle>

            <WuxingGrid>
              <WuxingCard element="목">
                <ElementName>목(木)</ElementName>
                <ElementCount>{result.wuxing_analysis.목}</ElementCount>
              </WuxingCard>
              <WuxingCard element="화">
                <ElementName>화(火)</ElementName>
                <ElementCount>{result.wuxing_analysis.화}</ElementCount>
              </WuxingCard>
              <WuxingCard element="토">
                <ElementName>토(土)</ElementName>
                <ElementCount>{result.wuxing_analysis.토}</ElementCount>
              </WuxingCard>
              <WuxingCard element="금">
                <ElementName>금(金)</ElementName>
                <ElementCount>{result.wuxing_analysis.금}</ElementCount>
              </WuxingCard>
              <WuxingCard element="수">
                <ElementName>수(水)</ElementName>
                <ElementCount>{result.wuxing_analysis.수}</ElementCount>
              </WuxingCard>
            </WuxingGrid>

            {result.wuxing_analysis.extended_analysis && (
              <ExtendedAnalysisContainer>
                <h4
                  style={{
                    color: "#2c3e50",
                    textAlign: "center",
                    marginBottom: "20px",
                  }}
                >
                  🔮 상세 오행 분석
                </h4>

                <BalanceScore>
                  <h5 style={{ color: "#2c3e50", marginBottom: "15px" }}>
                    오행 균형 점수
                  </h5>
                  <ScoreCircle
                    score={
                      result.wuxing_analysis.extended_analysis.balance_analysis
                        .balance_score
                    }
                  >
                    {
                      result.wuxing_analysis.extended_analysis.balance_analysis
                        .balance_score
                    }
                    점
                  </ScoreCircle>
                  <p style={{ color: "#7f8c8d", margin: 0 }}>
                    성격 유형:{" "}
                    <strong>
                      {
                        result.wuxing_analysis.extended_analysis
                          .personality_analysis.personality_type
                      }
                    </strong>
                  </p>
                </BalanceScore>

                <div style={{ marginTop: "20px" }}>
                  <SectionTitle>💫 오행별 상세 분석</SectionTitle>
                  {result.wuxing_analysis.extended_analysis
                    .balance_analysis && (
                    <div>
                      <p>
                        <strong>주도적 오행:</strong>{" "}
                        {
                          result.wuxing_analysis.extended_analysis
                            .balance_analysis.dominant_element
                        }
                      </p>
                      <p>
                        <strong>부족한 오행:</strong>{" "}
                        {
                          result.wuxing_analysis.extended_analysis
                            .balance_analysis.weakest_element
                        }
                      </p>

                      {result.wuxing_analysis.extended_analysis
                        .wuxing_details && (
                        <div style={{ marginTop: "20px" }}>
                          {Object.entries(
                            result.wuxing_analysis.extended_analysis
                              .wuxing_details
                          ).map(([element, data]: [string, any]) => (
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
                              <p
                                style={{
                                  margin: "5px 0 0 0",
                                  color: "#7f8c8d",
                                }}
                              >
                                강도: {data.strength} - {data.meaning}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <div style={{ marginTop: "20px" }}>
                  <SectionTitle>✨ 강점 & 약점</SectionTitle>
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr",
                      gap: "20px",
                    }}
                  >
                    <div>
                      <h5 style={{ color: "#27ae60" }}>강점</h5>
                      <ul style={{ listStyle: "none", padding: 0 }}>
                        {result.wuxing_analysis.extended_analysis.personality_analysis?.strengths?.map(
                          (strength: string, index: number) => (
                            <li
                              key={index}
                              style={{ padding: "5px 0", color: "#34495e" }}
                            >
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
                            <li
                              key={index}
                              style={{ padding: "5px 0", color: "#34495e" }}
                            >
                              ⚠ {weakness}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: "20px" }}>
                  <SectionTitle>🎯 맞춤형 조언</SectionTitle>
                  <RecommendationGrid>
                    <RecommendationCard>
                      <RecommendationTitle>🎨 추천 색상</RecommendationTitle>
                      <RecommendationList>
                        {result.wuxing_analysis.extended_analysis.recommendations?.colors?.map(
                          (color: string, index: number) => (
                            <RecommendationItem key={index}>
                              {color}
                            </RecommendationItem>
                          )
                        )}
                      </RecommendationList>
                    </RecommendationCard>

                    <RecommendationCard>
                      <RecommendationTitle>🧭 유리한 방향</RecommendationTitle>
                      <RecommendationList>
                        {result.wuxing_analysis.extended_analysis.recommendations?.directions?.map(
                          (direction: string, index: number) => (
                            <RecommendationItem key={index}>
                              {direction}
                            </RecommendationItem>
                          )
                        )}
                      </RecommendationList>
                    </RecommendationCard>

                    <RecommendationCard>
                      <RecommendationTitle>🏃‍♀️ 생활습관</RecommendationTitle>
                      <RecommendationList>
                        {result.wuxing_analysis.extended_analysis.recommendations?.lifestyle?.map(
                          (lifestyle: string, index: number) => (
                            <RecommendationItem key={index}>
                              {lifestyle}
                            </RecommendationItem>
                          )
                        )}
                      </RecommendationList>
                    </RecommendationCard>

                    <RecommendationCard>
                      <RecommendationTitle>💼 직업 조언</RecommendationTitle>
                      <RecommendationList>
                        {result.wuxing_analysis.extended_analysis.recommendations?.career_advice?.map(
                          (advice: string, index: number) => (
                            <RecommendationItem key={index}>
                              {advice}
                            </RecommendationItem>
                          )
                        )}
                      </RecommendationList>
                    </RecommendationCard>
                  </RecommendationGrid>
                </div>
              </ExtendedAnalysisContainer>
            )}
          </AnalysisSection>

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
      )}
    </Container>
  );
}

export default App;
