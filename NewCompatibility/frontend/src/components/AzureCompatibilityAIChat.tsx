import React, { useState, useEffect } from "react";
import styled from "styled-components";
import axios from "axios";

const ChatOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ChatContainer = styled.div`
  width: 90%;
  max-width: 600px;
  max-height: 80%;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
`;

const ChatHeader = styled.div`
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 20px;
  border-radius: 15px 15px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: background 0.3s;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
`;

const ChatMessages = styled.div`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  max-height: 400px;
`;

const Message = styled.div<{ $isUser: boolean }>`
  margin: 10px 0;
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 80%;
  word-wrap: break-word;
  align-self: ${props => props.$isUser ? 'flex-end' : 'flex-start'};
  margin-left: ${props => props.$isUser ? 'auto' : '0'};
  margin-right: ${props => props.$isUser ? '0' : 'auto'};
  
  ${props => props.$isUser ? `
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
  ` : `
    background: #f8f9fa;
    color: #333;
    border: 1px solid #e9ecef;
  `}
`;

const ChatInput = styled.div`
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;

  &:focus {
    border-color: #f093fb;
  }
`;

const SendButton = styled.button`
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const LoadingDots = styled.div`
  display: inline-block;
  font-size: 20px;
  
  &::after {
    content: '💕';
    animation: pulse 1.5s infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

const QuestionButton = styled.button`
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #f093fb;
  color: #f093fb;
  padding: 8px 16px;
  margin: 4px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-block;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

interface CompatibilityInfo {
  person1: {
    name: string;
    year: number;
    month: number;
    day: number;
    hour: number;
    gender: string;
  };
  person2: {
    name: string;
    year: number;
    month: number;
    day: number;
    hour: number;
    gender: string;
  };
}

interface Message {
  text: string;
  isUser: boolean;
  timestamp: Date;
  questions?: any[];
}

interface Props {
  compatibilityInfo: CompatibilityInfo;
  isVisible: boolean;
  onClose: () => void;
}

const AzureCompatibilityAIChat: React.FC<Props> = ({ compatibilityInfo, isVisible, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "안녕하세요! 저는 Azure GPT-4.1 궁합 전문 AI입니다. 💕\n두 분의 궁합에 맞춤형 질문을 준비하고 있어요...",
      isUser: false,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [questionsGenerated, setQuestionsGenerated] = useState(false);

  const API_BASE_URL = "http://localhost:8003/api/v1/azure-compatibility";

  // 채팅창이 열릴 때 자동으로 개인화된 질문 생성
  useEffect(() => {
    if (isVisible && !questionsGenerated) {
      generateSuggestedQuestions();
    }
  }, [isVisible]);

  const generateSuggestedQuestions = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/questions`, compatibilityInfo);
      
      const questions = response.data.data.suggested_questions || [];
      
      if (questions.length > 0) {
        const suggestionsMessage: Message & { questions?: any[] } = {
          text: "💕 **두 분을 위한 맞춤 궁합 질문들**\n\n아래 질문 중 하나를 클릭하거나 직접 질문해보세요! 😊",
          isUser: false,
          timestamp: new Date(),
          questions: questions
        };

        setMessages(prev => [...prev, suggestionsMessage]);
        setQuestionsGenerated(true);
      } else {
        const fallbackMessage: Message = {
          text: "궁합 분석에 대해 궁금한 점을 자유롭게 물어보세요! 💕",
          isUser: false,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, fallbackMessage]);
      }
    } catch (error) {
      console.error("궁합 질문 생성 오류:", error);
      const errorMessage: Message = {
        text: "맞춤 질문 준비 중 문제가 발생했어요. 😅\n그래도 궁금한 점이 있으시면 언제든 물어보세요!",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuestionClick = async (questionText: string) => {
    if (isLoading) return;

    const userMessage: Message = {
      text: questionText,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/chat`,
        compatibilityInfo,
        { 
          params: { question: questionText },
          timeout: 30000
        }
      );

      const aiResponse: Message = {
        text: response.data.data.ai_interpretation.ai_interpretation || "죄송합니다. 응답을 받지 못했습니다.",
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error("Azure AI 궁합 채팅 오류:", error);
      const errorMessage: Message = {
        text: "죄송합니다. Azure AI 궁합 서비스에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      text: inputText,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText("");
    setIsLoading(true);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/chat`,
        compatibilityInfo,
        { 
          params: { question: inputText },
          timeout: 30000
        }
      );

      const aiResponse: Message = {
        text: response.data.data.ai_interpretation.ai_interpretation || "죄송합니다. 응답을 받지 못했습니다.",
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error("Azure AI 궁합 채팅 오류:", error);
      const errorMessage: Message = {
        text: "죄송합니다. Azure AI 궁합 서비스에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요.",
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isVisible) return null;

  return (
    <ChatOverlay onClick={(e) => e.target === e.currentTarget && onClose()}>
      <ChatContainer>
        <ChatHeader>
          <h3>💕 Azure GPT-4.1 궁합 해석</h3>
          <CloseButton onClick={onClose}>×</CloseButton>
        </ChatHeader>

        <ChatMessages>
          {messages.map((message, index) => (
            <div key={index}>
              <Message $isUser={message.isUser}>
                {message.text.split('\n').map((line, i) => (
                  <div key={i}>{line}</div>
                ))}
              </Message>
              {message.questions && message.questions.length > 0 && (
                <div style={{ margin: '10px 0', textAlign: 'center' }}>
                  {message.questions.map((q: any, qIndex: number) => (
                    <QuestionButton
                      key={qIndex}
                      onClick={() => handleQuestionClick(q.question)}
                      disabled={isLoading}
                    >
                      {q.icon} {q.question}
                    </QuestionButton>
                  ))}
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <Message $isUser={false}>
              <LoadingDots /> Azure AI가 궁합 해석을 준비하고 있습니다...
            </Message>
          )}
        </ChatMessages>

        <ChatInput>
          <Input
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Azure AI에게 궁합에 대해 궁금한 점을 물어보세요..."
            disabled={isLoading}
          />
          <SendButton onClick={sendMessage} disabled={isLoading || !inputText.trim()}>
            전송
          </SendButton>
        </ChatInput>
      </ChatContainer>
    </ChatOverlay>
  );
};

export default AzureCompatibilityAIChat;