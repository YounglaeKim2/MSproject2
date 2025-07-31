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

interface AIChatProps {
  birthInfo: BirthInfo;
  isVisible: boolean;
  onClose: () => void;
}

// 스타일 컴포넌트
const ChatOverlay = styled.div<{ isVisible: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: ${props => props.isVisible ? 'flex' : 'none'};
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

const QuickButton = styled.button`
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #495057;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: #e9ecef;
    border-color: #adb5bd;
  }

  &:active {
    transform: scale(0.98);
  }
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

// 메인 컴포넌트
const AIChatInterface: React.FC<AIChatProps> = ({ birthInfo, isVisible, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [usageStatus, setUsageStatus] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 퀵 버튼 질문들
  const quickQuestions = [
    "내 성격의 장단점을 알려주세요",
    "올해 운세는 어떤가요?",
    "직업운에 대해 알려주세요",
    "건강 관리 포인트는?",
    "연애운은 어떤가요?",
    "재물운에 대해 궁금해요"
  ];

  // 메시지 스크롤
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 사용량 조회
  useEffect(() => {
    if (isVisible) {
      fetchUsageStatus();
      // 환영 메시지 추가
      setMessages([{
        id: Date.now().toString(),
        type: 'system',
        content: `${birthInfo.name}님의 사주를 바탕으로 궁금한 점을 물어보세요! 🤖`,
        timestamp: new Date().toLocaleTimeString()
      }]);
    }
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
    <ChatOverlay isVisible={isVisible}>
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

          <QuickButtons>
            {quickQuestions.map((question, index) => (
              <QuickButton
                key={index}
                onClick={() => handleQuickQuestion(question)}
                disabled={isLoading}
              >
                {question}
              </QuickButton>
            ))}
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