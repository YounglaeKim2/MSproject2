import styled from 'styled-components';

// 공통 컨테이너
export const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

export const Title = styled.h1`
  text-align: center;
  color: white;
  margin-bottom: 30px;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

// 폼 관련 스타일
export const Form = styled.form`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
`;

export const FormGroup = styled.div`
  margin-bottom: 20px;
`;

export const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
`;

export const Input = styled.input`
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
  box-sizing: border-box;

  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

export const Select = styled.select`
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  background-color: white;
  box-sizing: border-box;

  &:focus {
    outline: none;
    border-color: #3498db;
  }
`;

export const Button = styled.button`
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

export const AIButton = styled.button`
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin: 20px auto;
  display: block;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
`;

// 결과 표시 관련 스타일
export const ResultContainer = styled.div`
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
`;

export const SectionTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
`;

export const AnalysisSection = styled.div`
  margin: 30px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
`;

// 사주팔자 표시 관련
export const SajuGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin: 20px 0;
  text-align: center;
`;

export const SajuPillar = styled.div`
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 2px solid #e1e8ed;
`;

export const PillarTitle = styled.div`
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
`;

export const Character = styled.div`
  font-size: 24px;
  font-weight: bold;
  margin: 5px 0;
  color: #e74c3c;
`;

// 오행 분석 관련
export const WuxingGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin: 20px 0;
`;

export const WuxingCard = styled.div<{ $element: string }>`
  background: ${(props) => {
    switch (props.$element) {
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

export const ElementName = styled.div`
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
`;

export const ElementCount = styled.div`
  font-size: 24px;
  font-weight: bold;
`;

// 확장 분석 관련
export const ExtendedAnalysisContainer = styled.div`
  background: #f8f9fa;
  padding: 25px;
  border-radius: 15px;
  margin: 20px 0;
`;

export const BalanceScore = styled.div`
  text-align: center;
  margin: 20px 0;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

export const ScoreCircle = styled.div<{ $score: number }>`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    #3498db 0deg,
    #3498db ${(props) => props.$score * 3.6}deg,
    #ecf0f1 ${(props) => props.$score * 3.6}deg,
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

// 추천사항 관련
export const RecommendationGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
`;

export const RecommendationCard = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

export const RecommendationTitle = styled.h4`
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 16px;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 8px;
`;

export const RecommendationList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

export const RecommendationItem = styled.li`
  padding: 5px 0;
  color: #34495e;

  &:before {
    content: "✓ ";
    color: #27ae60;
    font-weight: bold;
  }
`;

// 에러 메시지
export const ErrorMessage = styled.div`
  padding: 20px;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #e74c3c;
`;