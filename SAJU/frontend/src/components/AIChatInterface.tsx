import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';

// 타입 정의
interface Message {
  id: string;
  type: 'user' | 'ai' | 'system';
  content: string;
  timestamp: string;
}

interface BirthInfo {
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: string;
  name: string;
}

interface SuggestedQuestion {
  question: string;
  category: string;
  priority: 'high' | 'medium' | 'low';
  icon: string;
}

interface AIChatProps {
  birthInfo: BirthInfo;
  isVisible: boolean;
  onClose: () => void;
}

// 스타일 컴포넌트
const ChatOverlay = styled.div<{ $isVisible: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: ${props => props.$isVisible ? 'flex' : 'none'};
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ChatContainer = styled.div`
  width: 90%;
  max-width: 600px;
  height: 80vh;
  background: white;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
`;

const ChatHeader = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 15px 15px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const HeaderTitle = styled.h3`
  margin: 0;
  font-size: 1.2rem;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background 0.3s;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
`;

const ChatMessages = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const MessageBubble = styled.div<{ type: 'user' | 'ai' | 'system' }>`
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.4;
  
  ${props => {
    switch (props.type) {
      case 'user':
        return `
          background: #667eea;
          color: white;
          align-self: flex-end;
          margin-left: auto;
        `;
      case 'ai':
        return `
          background: #f1f3f4;
          color: #333;
          align-self: flex-start;
          border: 1px solid #e1e8ed;
        `;
      case 'system':
        return `
          background: #fff3cd;
          color: #856404;
          align-self: center;
          font-size: 0.9rem;
          text-align: center;
        `;
    }
  }}
`;

const MessageTime = styled.div`
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 4px;
`;

const ChatInput = styled.div`
  padding: 20px;
  border-top: 1px solid #e1e8ed;
  display: flex;
  gap: 10px;
`;

const QuickButtons = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 15px;
  flex-wrap: wrap;
`;


const InputField = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;

  &:focus {
    border-color: #667eea;
  }

  &:disabled {
    background: #f8f9fa;
    cursor: not-allowed;
  }
`;

const SendButton = styled.button`
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;

  &:hover:not(:disabled) {
    background: #5a6fd8;
  }

  &:disabled {
    background: #ced4da;
    cursor: not-allowed;
  }
`;

const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6c757d;
  font-style: italic;
  padding: 10px 16px;
`;

const UsageStatus = styled.div`
  background: #e3f2fd;
  border: 1px solid #bbdefb;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 0.85rem;
  color: #1565c0;
`;

// 새로운 개인화된 질문 UI 컴포넌트들
const PersonalizedQuickButton = styled.button<{ 
  $category: string; 
  $priority: 'high' | 'medium' | 'low' 
}>`
  background: ${props => getCategoryColor(props.$category)};
  border: none;
  color: white;
  padding: 12px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 200px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  
  opacity: ${props => props.$priority === 'high' ? 1 : props.$priority === 'medium' ? 0.9 : 0.8};
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    opacity: 1;
  }

  &:active {
    transform: scale(0.98);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const QuestionIcon = styled.span`
  font-size: 1.2rem;
`;

const QuestionText = styled.span`
  flex: 1;
  text-align: left;
  line-height: 1.3;
`;

const CategoryBadge = styled.span<{ $category: string }>`
  background: rgba(255,255,255,0.3);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 600;
`;

const LoadingQuestions = styled.div`
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  color: #6c757d;
  font-style: italic;
  animation: pulse 1.5s ease-in-out infinite;
  
  @keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
  }
`;

const QuestionModeToggle = styled.div`
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
  justify-content: center;
`;

const ModeButton = styled.button<{ $active: boolean }>`
  background: ${props => props.$active ? '#667eea' : '#f8f9fa'};
  color: ${props => props.$active ? 'white' : '#6c757d'};
  border: 1px solid ${props => props.$active ? '#667eea' : '#dee2e6'};
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: ${props => props.$active ? '#5a6fd8' : '#e9ecef'};
  }
`;

// 카테고리별 색상 매핑 함수
const getCategoryColor = (category: string) => {
  const colors: { [key: string]: string } = {
    '연애': '#ff6b9d',
    '직업': '#4dabf7', 
    '건강': '#51cf66',
    '재물': '#ffd43b',
    '인간관계': '#9775fa',
    '성격': '#ff8787',
    '운세': '#845ef7',
    '자기계발': '#20c997'
  };
  return colors[category] || '#6c757d';
};

// 기본 질문들 (폴백용)
const getDefaultQuestions = (): SuggestedQuestion[] => [
  { question: "내 성격의 장단점을 알려주세요", category: "성격", priority: "high", icon: "🤔" },
  { question: "올해 운세는 어떤가요?", category: "운세", priority: "high", icon: "🔮" },
  { question: "직업운에 대해 알려주세요", category: "직업", priority: "medium", icon: "💼" },
  { question: "건강 관리 포인트는?", category: "건강", priority: "medium", icon: "🏥" },
  { question: "연애운은 어떤가요?", category: "연애", priority: "low", icon: "💕" }
];

// 메인 컴포넌트
const AIChatInterface: React.FC<AIChatProps> = ({ birthInfo, isVisible, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [usageStatus, setUsageStatus] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 새로운 상태들
  const [suggestedQuestions, setSuggestedQuestions] = useState<SuggestedQuestion[]>([]);
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(false);
  const [questionMode, setQuestionMode] = useState<'hybrid' | 'ai' | 'rules'>('hybrid');

  // 메시지 스크롤
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 개인화된 질문 생성
  const generateSuggestedQuestions = async (mode: 'hybrid' | 'ai' | 'rules' = 'hybrid') => {
    setIsLoadingQuestions(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/saju/suggested-questions?method=${mode}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(birthInfo)
      });
      
      const data = await response.json();
      if (data.success) {
        setSuggestedQuestions(data.data.suggested_questions);
        
        // 사용량 정보 업데이트 (AI 모드인 경우)
        if (data.data.usage_status) {
          setUsageStatus(data.data.usage_status);
        }
      } else {
        console.error('질문 생성 실패:', data);
        setSuggestedQuestions(getDefaultQuestions());
      }
    } catch (error) {
      console.error('개인화된 질문 생성 실패:', error);
      setSuggestedQuestions(getDefaultQuestions());
    } finally {
      setIsLoadingQuestions(false);
    }
  };

  // 모드 변경 핸들러
  const handleModeChange = (mode: 'hybrid' | 'ai' | 'rules') => {
    setQuestionMode(mode);
    generateSuggestedQuestions(mode);
  };

  // 사용량 조회 및 초기 설정
  useEffect(() => {
    if (isVisible) {
      fetchUsageStatus();
      generateSuggestedQuestions(questionMode);
      
      // 환영 메시지 추가
      setMessages([{
        id: Date.now().toString(),
        type: 'system',
        content: `${birthInfo.name}님의 사주를 바탕으로 궁금한 점을 물어보세요! 🤖`,
        timestamp: new Date().toLocaleTimeString()
      }]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isVisible, birthInfo.name]);

  const fetchUsageStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/saju/ai-usage');
      const data = await response.json();
      if (data.success) {
        setUsageStatus(data.usage_status);
      }
    } catch (error) {
      console.error('사용량 조회 실패:', error);
    }
  };

  const sendMessage = async (question: string) => {
    if (!question.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/saju/ai-chat?question=${encodeURIComponent(question)}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(birthInfo)
        }
      );

      const data = await response.json();

      if (data.success && data.data.ai_interpretation.success) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'ai',
          content: data.data.ai_interpretation.ai_interpretation,
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, aiMessage]);
        
        // 사용량 업데이트
        if (data.data.ai_interpretation.usage_status) {
          setUsageStatus(data.data.ai_interpretation.usage_status);
        }
      } else {
        // 에러 메시지 표시
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'system',
          content: data.data?.ai_interpretation?.message || '죄송합니다. 일시적인 오류가 발생했습니다.',
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('AI 해석 요청 실패:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: '네트워크 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question: string) => {
    sendMessage(question);
  };

  const handleInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  if (!isVisible) return null;

  return (
    <ChatOverlay $isVisible={isVisible}>
      <ChatContainer>
        <ChatHeader>
          <HeaderTitle>🤖 AI 사주 해석</HeaderTitle>
          <CloseButton onClick={onClose}>×</CloseButton>
        </ChatHeader>

        <ChatMessages>
          {usageStatus && (
            <UsageStatus>
              💡 오늘 사용량: {usageStatus.daily.used}/{usageStatus.daily.limit}회 | 
              이번 달: {usageStatus.monthly.used}/{usageStatus.monthly.limit}회 (무료)
            </UsageStatus>
          )}

          {/* 질문 생성 모드 선택 */}
          <QuestionModeToggle>
            <ModeButton 
              $active={questionMode === 'hybrid'} 
              onClick={() => handleModeChange('hybrid')}
            >
              🔄 하이브리드
            </ModeButton>
            <ModeButton 
              $active={questionMode === 'ai'} 
              onClick={() => handleModeChange('ai')}
            >
              🤖 AI 생성
            </ModeButton>
            <ModeButton 
              $active={questionMode === 'rules'} 
              onClick={() => handleModeChange('rules')}
            >
              ⚡ 빠른 생성
            </ModeButton>
          </QuestionModeToggle>

          {/* 개인화된 질문 버튼들 */}
          <QuickButtons>
            {isLoadingQuestions ? (
              <LoadingQuestions>
                🤖 {birthInfo.name}님에게 맞는 질문을 생성하는 중...
              </LoadingQuestions>
            ) : (
              suggestedQuestions.map((q, index) => (
                <PersonalizedQuickButton
                  key={index}
                  $category={q.category}
                  $priority={q.priority}
                  onClick={() => handleQuickQuestion(q.question)}
                  disabled={isLoading}
                >
                  <QuestionIcon>{q.icon}</QuestionIcon>
                  <QuestionText>{q.question}</QuestionText>
                  <CategoryBadge $category={q.category}>
                    {q.category}
                  </CategoryBadge>
                </PersonalizedQuickButton>
              ))
            )}
          </QuickButtons>

          {messages.map((message) => (
            <MessageBubble key={message.id} type={message.type}>
              <div>{message.content}</div>
              <MessageTime>{message.timestamp}</MessageTime>
            </MessageBubble>
          ))}

          {isLoading && (
            <LoadingIndicator>
              <div>🤖 AI가 해석 중입니다...</div>
            </LoadingIndicator>
          )}

          <div ref={messagesEndRef} />
        </ChatMessages>

        <ChatInput>
          <form onSubmit={handleInputSubmit} style={{ display: 'flex', gap: '10px', width: '100%' }}>
            <InputField
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="궁금한 점을 물어보세요... (예: 내 성격은 어떤가요?)"
              disabled={isLoading}
            />
            <SendButton type="submit" disabled={isLoading || !inputValue.trim()}>
              전송
            </SendButton>
          </form>
        </ChatInput>
      </ChatContainer>
    </ChatOverlay>
  );
};

export default AIChatInterface;