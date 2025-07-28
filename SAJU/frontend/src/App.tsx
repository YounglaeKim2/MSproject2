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

interface DaeunInfo {
  period: string;
  start_age: number;
  end_age: number;
  gan: string;
  ji: string;
  gan_wuxing: string;
  ji_wuxing: string;
  is_current: boolean;
  fortune_level: string;
  characteristics: string[];
  major_events: string[];
  advice: string;
}

interface DaeunResult {
  basic_info: any;
  palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  daeun_analysis: {
    daeun_start_age: number;
    is_forward: boolean;
    current_age: number;
    daeun_list: DaeunInfo[];
  };
}

interface SaeunInfo {
  month: number;
  month_name: string;
  gan: string;
  ji: string;
  gan_wuxing: string;
  ji_wuxing: string;
  fortune_score: number;
  fortune_grade: string;
  interaction_analysis: {
    favorable_aspects: string[];
    challenging_aspects: string[];
    recommendations: string[];
  };
  summary: string;
}

interface SaeunResult {
  basic_info: {
    name: string;
    birth_date: string;
    gender: string;
    target_year: number;
  };
  palja: {
    year_pillar: { stem: string; branch: string };
    month_pillar: { stem: string; branch: string };
    day_pillar: { stem: string; branch: string };
    hour_pillar: { stem: string; branch: string };
  };
  saeun_analysis: {
    target_year: number;
    yearly_saeun: {
      gan: string;
      ji: string;
      gan_wuxing: string;
      ji_wuxing: string;
      ganzhi: string;
    };
    monthly_saeun: SaeunInfo[];
    annual_score: {
      total_score: number;
      normalized_score: number;
      grade: string;
      yearly_contribution: number;
      monthly_average: number;
    };
    saeun_interaction: {
      yearly: {
        score: number;
        fortune_level: string;
        characteristics: string[];
        opportunities: string[];
        warnings: string[];
      };
      monthly: Array<{
        score: number;
        fortune_level: string;
        characteristics: string[];
        opportunities: string[];
        warnings: string[];
        month: number;
        ganzhi: string;
      }>;
    };
    critical_periods: {
      best_months: Array<{ month: number; score: number; level: string }>;
      caution_months: Array<{ month: number; score: number; level: string }>;
      opportunity_months: Array<{ month: number; opportunities: string[] }>;
    };
    summary: string;
  };
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
        career_advice: string[];
        health_advice: string[];
        relationship_advice: string[];
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
  const [daeunResult, setDaeunResult] = useState<DaeunResult | null>(null);
  const [saeunResult, setSaeunResult] = useState<SaeunResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [daeunLoading, setDaeunLoading] = useState(false);
  const [saeunLoading, setSaeunLoading] = useState(false);
  const [targetYear, setTargetYear] = useState<number>(new Date().getFullYear());
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

  const handleDaeunAnalysis = async () => {
    setDaeunLoading(true);
    setError("");

    try {
      console.log("대운 분석 요청 데이터:", formData);
      const response = await axios.post(
        "http://localhost:8000/api/v1/saju/daeun",
        formData
      );
      console.log("대운 분석 API 응답:", response.data);
      setDaeunResult(response.data);
    } catch (err: any) {
      console.error("대운 분석 API 오류:", err);
      console.error("응답 데이터:", err.response?.data);
      setError(err.response?.data?.detail || "대운 분석 중 오류가 발생했습니다.");
    } finally {
      setDaeunLoading(false);
    }
  };

  const handleSaeunAnalysis = async () => {
    setSaeunLoading(true);
    setError("");

    try {
      console.log("세운 분석 요청 데이터:", formData, "대상연도:", targetYear);
      const response = await axios.post(
        `http://localhost:8000/api/v1/saju/saeun?target_year=${targetYear}`,
        formData
      );
      console.log("세운 분석 API 응답:", response.data);
      setSaeunResult(response.data);
    } catch (err: any) {
      console.error("세운 분석 API 오류:", err);
      console.error("응답 데이터:", err.response?.data);
      setError(err.response?.data?.detail || "세운 분석 중 오류가 발생했습니다.");
    } finally {
      setSaeunLoading(false);
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

      {/* 대운 분석 섹션 */}
      <Form style={{ marginTop: '20px', background: '#f8f9fa', border: '2px solid #e9ecef' }}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <h3 style={{ color: '#495057', margin: '0 0 10px 0' }}>🌟 대운 분석</h3>
          <p style={{ color: '#6c757d', margin: 0, fontSize: '14px' }}>
            인생 전체의 운세 흐름을 10년 주기로 분석합니다
          </p>
        </div>
        <Button 
          type="button" 
          disabled={daeunLoading || !formData.name}
          onClick={handleDaeunAnalysis}
          style={{ 
            background: daeunLoading ? '#6c757d' : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            marginTop: '0'
          }}
        >
          {daeunLoading ? "대운 분석 중..." : "대운 분석하기"}
        </Button>
      </Form>

      {/* 세운 분석 섹션 */}
      <Form style={{ marginTop: '20px', background: '#e8f5e8', border: '2px solid #c8e6c9' }}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <h3 style={{ color: '#2e7d32', margin: '0 0 10px 0' }}>⏰ 세운 분석</h3>
          <p style={{ color: '#4caf50', margin: 0, fontSize: '14px' }}>
            특정 연도의 월별 운세를 상세하게 분석합니다
          </p>
        </div>
        
        <FormGroup style={{ marginBottom: '20px' }}>
          <Label style={{ color: '#2e7d32' }}>분석 대상 연도</Label>
          <Input
            type="number"
            value={targetYear}
            onChange={(e) => setTargetYear(parseInt(e.target.value) || new Date().getFullYear())}
            min="2020"
            max="2030"
            style={{ border: '2px solid #c8e6c9' }}
          />
        </FormGroup>
        
        <Button 
          type="button" 
          disabled={saeunLoading || !formData.name}
          onClick={handleSaeunAnalysis}
          style={{ 
            background: saeunLoading ? '#6c757d' : 'linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)',
            marginTop: '0'
          }}
        >
          {saeunLoading ? "세운 분석 중..." : `${targetYear}년 세운 분석하기`}
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

                    <RecommendationCard>
                      <RecommendationTitle>💊 건강 관리</RecommendationTitle>
                      <RecommendationList>
                        {result.wuxing_analysis.extended_analysis.recommendations?.health_advice?.map(
                          (advice: string, index: number) => (
                            <RecommendationItem key={index}>
                              {advice}
                            </RecommendationItem>
                          )
                        )}
                      </RecommendationList>
                    </RecommendationCard>

                    <RecommendationCard>
                      <RecommendationTitle>💑 인간관계</RecommendationTitle>
                      <RecommendationList>
                        {result.wuxing_analysis.extended_analysis.recommendations?.relationship_advice?.map(
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

      {/* 대운 분석 결과 */}
      {daeunResult && (
        <ResultContainer style={{ marginTop: '30px' }}>
          <SectionTitle style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '30px' }}>
            🌟 대운 분석 결과
          </SectionTitle>
          
          {/* 기본 정보 */}
          <AnalysisSection>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
              <div>
                <strong>현재 나이:</strong> {daeunResult.daeun_analysis.current_age}세
              </div>
              <div>
                <strong>대운 시작:</strong> {daeunResult.daeun_analysis.daeun_start_age}세부터
              </div>
              <div>
                <strong>진행 방향:</strong> {daeunResult.daeun_analysis.is_forward ? '순행' : '역행'}
              </div>
            </div>
          </AnalysisSection>

          {/* 대운 타임라인 */}
          <AnalysisSection>
            <SectionTitle>📅 인생 대운 타임라인</SectionTitle>
            <div style={{ display: 'grid', gap: '20px' }}>
              {daeunResult.daeun_analysis.daeun_list.map((daeun, index) => (
                <div
                  key={index}
                  style={{
                    border: daeun.is_current ? '3px solid #f093fb' : '2px solid #e9ecef',
                    borderRadius: '15px',
                    padding: '20px',
                    background: daeun.is_current ? 'linear-gradient(135deg, #f093fb22, #f5576c22)' : 'white',
                    boxShadow: daeun.is_current ? '0 5px 20px rgba(240, 147, 251, 0.3)' : '0 2px 10px rgba(0,0,0,0.1)',
                    position: 'relative'
                  }}
                >
                  {daeun.is_current && (
                    <div style={{
                      position: 'absolute',
                      top: '-10px',
                      right: '20px',
                      background: '#f093fb',
                      color: 'white',
                      padding: '5px 15px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}>
                      현재 대운
                    </div>
                  )}
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                    <div>
                      <h4 style={{ margin: 0, color: '#2c3e50' }}>{daeun.period}</h4>
                      <p style={{ margin: '5px 0', color: '#6c757d', fontSize: '14px' }}>
                        {daeun.gan}{daeun.ji} ({daeun.gan_wuxing}·{daeun.ji_wuxing})
                      </p>
                    </div>
                    <div style={{
                      padding: '8px 16px',
                      borderRadius: '20px',
                      fontWeight: 'bold',
                      fontSize: '14px',
                      background: 
                        daeun.fortune_level === '대길' ? '#28a745' :
                        daeun.fortune_level === '소길' ? '#17a2b8' :
                        daeun.fortune_level === '평운' ? '#ffc107' :
                        daeun.fortune_level === '소흉' ? '#fd7e14' : '#dc3545',
                      color: 'white'
                    }}>
                      {daeun.fortune_level}
                    </div>
                  </div>

                  <div style={{ marginBottom: '15px' }}>
                    <strong style={{ color: '#495057', fontSize: '14px' }}>특징:</strong>
                    <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                      {daeun.characteristics.map((char, i) => (
                        <span
                          key={i}
                          style={{
                            background: '#e9ecef',
                            padding: '4px 12px',
                            borderRadius: '15px',
                            fontSize: '13px',
                            color: '#495057'
                          }}
                        >
                          {char}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div style={{ marginBottom: '15px' }}>
                    <strong style={{ color: '#495057', fontSize: '14px' }}>주요 이벤트:</strong>
                    <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
                      {daeun.major_events.map((event, i) => (
                        <li key={i} style={{ fontSize: '13px', color: '#6c757d', marginBottom: '4px' }}>
                          {event}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div style={{
                    background: '#f8f9fa',
                    padding: '12px',
                    borderRadius: '8px',
                    borderLeft: '4px solid #17a2b8'
                  }}>
                    <strong style={{ color: '#495057', fontSize: '14px' }}>조언:</strong>
                    <p style={{ margin: '8px 0 0 0', fontSize: '13px', color: '#6c757d', lineHeight: '1.5' }}>
                      {daeun.advice}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </AnalysisSection>
        </ResultContainer>
      )}

      {/* 세운 분석 결과 */}
      {saeunResult && (
        <ResultContainer style={{ marginTop: '30px' }}>
          <SectionTitle style={{ textAlign: 'center', fontSize: '2rem', marginBottom: '30px' }}>
            ⏰ {saeunResult.basic_info.target_year}년 세운 분석 결과
          </SectionTitle>
          
          {/* 연간 세운 정보 */}
          <AnalysisSection>
            <SectionTitle>📅 {saeunResult.saeun_analysis.target_year}년 연간 세운</SectionTitle>
            <div style={{ 
              background: 'linear-gradient(135deg, #4caf50, #2e7d32)', 
              color: 'white', 
              padding: '20px', 
              borderRadius: '15px',
              textAlign: 'center',
              marginBottom: '20px'
            }}>
              <h3 style={{ margin: '0 0 10px 0' }}>
                {saeunResult.saeun_analysis.yearly_saeun.gan}{saeunResult.saeun_analysis.yearly_saeun.ji}
              </h3>
              <p style={{ margin: '5px 0', fontSize: '14px', opacity: '0.9' }}>
                ({saeunResult.saeun_analysis.yearly_saeun.gan_wuxing}·{saeunResult.saeun_analysis.yearly_saeun.ji_wuxing})
              </p>
              <p style={{ margin: 0, lineHeight: '1.5' }}>
                {saeunResult.saeun_analysis.yearly_saeun.description}
              </p>
            </div>
          </AnalysisSection>

          {/* 전체 운세 요약 */}
          <AnalysisSection>
            <SectionTitle>🎯 종합 운세 점수</SectionTitle>
            <BalanceScore>
              <ScoreCircle score={saeunResult.saeun_analysis.annual_score.normalized_score}>
                {saeunResult.saeun_analysis.annual_score.normalized_score}점
              </ScoreCircle>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
                <div>
                  <h5 style={{ color: '#27ae60', marginBottom: '10px' }}>🍀 최고의 달</h5>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {saeunResult.saeun_analysis.critical_periods.best_months.map((monthData, index) => (
                      <span key={index} style={{
                        background: '#27ae60',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '14px'
                      }}>
                        {monthData.month}월 ({monthData.level})
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h5 style={{ color: '#e74c3c', marginBottom: '10px' }}>⚠️ 주의할 달</h5>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {saeunResult.saeun_analysis.critical_periods.caution_months.map((monthData, index) => (
                      <span key={index} style={{
                        background: '#e74c3c',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '14px'
                      }}>
                        {monthData.month}월 ({monthData.level})
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </BalanceScore>
          </AnalysisSection>

          {/* 월별 세운 상세 */}
          <AnalysisSection>
            <SectionTitle>📊 월별 운세 상세 분석</SectionTitle>
            <div style={{ display: 'grid', gap: '20px' }}>
              {saeunResult.saeun_analysis.monthly_saeun.map((monthData, index) => {
                const interactionData = saeunResult.saeun_analysis.saeun_interaction.monthly.find(
                  m => m.month === monthData.month
                );
                return (
                <div
                  key={index}
                  style={{
                    border: '2px solid #e9ecef',
                    borderRadius: '15px',
                    padding: '20px',
                    background: 'white',
                    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
                    borderColor: 
                      interactionData?.fortune_level === '대길' ? '#28a745' :
                      interactionData?.fortune_level === '소길' ? '#17a2b8' :
                      interactionData?.fortune_level === '평운' ? '#ffc107' :
                      interactionData?.fortune_level === '소흉' ? '#fd7e14' : '#dc3545'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                    <div>
                      <h4 style={{ margin: 0, color: '#2c3e50' }}>{monthData.month}월</h4>
                      <p style={{ margin: '5px 0', color: '#6c757d', fontSize: '14px' }}>
                        {monthData.gan}{monthData.ji} ({monthData.gan_wuxing}·{monthData.ji_wuxing})
                      </p>
                    </div>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '15px'
                    }}>
                      <div style={{
                        padding: '8px 16px',
                        borderRadius: '20px',
                        fontWeight: 'bold',
                        fontSize: '14px',
                        background: 
                          interactionData?.fortune_level === '대길' ? '#28a745' :
                          interactionData?.fortune_level === '소길' ? '#17a2b8' :
                          interactionData?.fortune_level === '평운' ? '#ffc107' :
                          interactionData?.fortune_level === '소흉' ? '#fd7e14' : '#dc3545',
                        color: 'white'
                      }}>
                        {interactionData?.fortune_level || '평운'}
                      </div>
                      <div style={{
                        fontSize: '18px',
                        fontWeight: 'bold',
                        color: '#2c3e50'
                      }}>
                        {interactionData?.score || 0}점
                      </div>
                    </div>
                  </div>

                  <div style={{ marginBottom: '15px' }}>
                    <p style={{ margin: 0, fontSize: '15px', lineHeight: '1.5', color: '#495057' }}>
                      {interactionData?.characteristics?.join(', ') || '평상시와 같은 운세입니다'}
                    </p>
                  </div>

                  {interactionData && (interactionData.opportunities.length > 0 || interactionData.warnings.length > 0) && (
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginTop: '15px' }}>
                      {interactionData.opportunities.length > 0 && (
                        <div>
                          <strong style={{ color: '#28a745', fontSize: '13px' }}>🍀 기회:</strong>
                          <ul style={{ margin: '5px 0', paddingLeft: '15px', fontSize: '12px' }}>
                            {interactionData.opportunities.map((opportunity, i) => (
                              <li key={i} style={{ color: '#495057', marginBottom: '2px' }}>{opportunity}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {interactionData.warnings.length > 0 && (
                        <div>
                          <strong style={{ color: '#dc3545', fontSize: '13px' }}>⚠️ 주의사항:</strong>
                          <ul style={{ margin: '5px 0', paddingLeft: '15px', fontSize: '12px' }}>
                            {interactionData.warnings.map((warning, i) => (
                              <li key={i} style={{ color: '#495057', marginBottom: '2px' }}>{warning}</li>
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
            <SectionTitle>💡 {saeunResult.saeun_analysis.target_year}년 종합 조언</SectionTitle>
            <div style={{
              background: '#f8f9fa',
              padding: '20px',
              borderRadius: '10px',
              borderLeft: '5px solid #4caf50'
            }}>
              <p style={{ margin: 0, fontSize: '16px', lineHeight: '1.6', color: '#495057' }}>
                {saeunResult.saeun_analysis.summary}
              </p>
            </div>
            
          </AnalysisSection>
        </ResultContainer>
      )}
    </Container>
  );
}

export default App;
