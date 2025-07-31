import React from 'react';
import styled, { keyframes } from 'styled-components';

// 애니메이션 정의
const sparkle = keyframes`
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.1); }
`;

const bounce = keyframes`
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
`;

// 메인 컨테이너
const CyworldContainer = styled.div`
  min-height: 100vh;
  background: 
    radial-gradient(ellipse at top left, rgba(255,182,193,0.3) 0%, transparent 50%),
    radial-gradient(ellipse at top right, rgba(221,160,221,0.3) 0%, transparent 50%),
    radial-gradient(ellipse at bottom left, rgba(173,216,230,0.3) 0%, transparent 50%),
    linear-gradient(135deg, #F0F8FF 0%, #E6E6FA 50%, #FFE4E1 100%);
  padding: 20px;
  font-family: 'Comic Sans MS', 'Malgun Gothic', sans-serif;
  position: relative;
  
  &::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(circle at 20% 30%, rgba(255,182,193,0.1) 2px, transparent 2px),
      radial-gradient(circle at 80% 70%, rgba(221,160,221,0.1) 1px, transparent 1px);
    background-size: 50px 50px, 30px 30px;
    pointer-events: none;
    z-index: 0;
  }
  
  & > * {
    position: relative;
    z-index: 1;
  }
`;

// 다이어리 노트북 스타일 컨테이너 (싸이월드 스타일)
const NotebookContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  background: #fff;
  border-radius: 15px;
  box-shadow: 
    0 0 0 2px #87CEEB,
    0 0 0 4px #fff,
    0 0 0 6px #DDA0DD,
    0 15px 40px rgba(135,206,235,0.3);
  position: relative;
  overflow: hidden;
  
  /* 노트북 링 바인딩 효과 */
  &::before {
    content: '';
    position: absolute;
    left: 25px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(to bottom, #FF69B4, #DDA0DD);
    z-index: 2;
    box-shadow: 0 0 5px rgba(255,105,180,0.5);
  }
  
  /* 링 홀 효과 */
  &::after {
    content: '';
    position: absolute;
    left: 10px;
    top: 30px;
    bottom: 30px;
    width: 12px;
    background-image: 
      radial-gradient(circle at center, transparent 3px, #FF69B4 3px, #FF69B4 5px, transparent 5px);
    background-size: 100% 25px;
    background-repeat: repeat-y;
  }
`;

// 미니홈피 헤더 (더 진짜 싸이월드 스타일)
const MinihompyHeader = styled.div`
  background: 
    linear-gradient(180deg, #87CEEB 0%, #6BB6FF 50%, #4682B4 100%);
  border-radius: 15px 15px 0 0;
  padding: 20px 50px 15px 50px;
  border-bottom: 2px solid rgba(255,255,255,0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.3);
  
  /* TODAY/TOTAL 카운터 */
  &::before {
    content: 'TODAY 1 | TOTAL 2,024';
    position: absolute;
    top: 5px;
    right: 50px;
    font-size: 10px;
    color: rgba(255,255,255,0.9);
    font-weight: bold;
    background: rgba(255,255,255,0.2);
    padding: 2px 8px;
    border-radius: 10px;
  }
  
  /* 왼쪽 상단 장식 */
  &::after {
    content: '★ SAJU MINIHOMPY ★';
    position: absolute;
    top: 5px;
    left: 50px;
    font-size: 10px;
    color: rgba(255,255,255,0.8);
    font-weight: bold;
  }
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const Avatar = styled.div`
  width: 70px;
  height: 70px;
  background: 
    radial-gradient(ellipse at 30% 30%, #FFE4E1, #DDA0DD);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  border: 4px solid #fff;
  box-shadow: 
    0 0 0 2px #87CEEB,
    0 6px 15px rgba(0,0,0,0.3),
    inset 0 2px 5px rgba(255,255,255,0.5);
  animation: ${bounce} 3s infinite;
  position: relative;
  
  /* 온라인 상태 표시 */
  &::after {
    content: '';
    position: absolute;
    top: -3px;
    right: -3px;
    width: 16px;
    height: 16px;
    background: radial-gradient(circle, #32CD32, #228B22);
    border-radius: 50%;
    border: 3px solid #fff;
    animation: ${sparkle} 2s ease-in-out infinite;
    box-shadow: 0 0 8px rgba(50,205,50,0.6);
  }
  
  /* 캐릭터 그림자 */
  &::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 8px;
    background: rgba(0,0,0,0.2);
    border-radius: 50%;
    filter: blur(3px);
  }
`;

const UserName = styled.h2`
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  margin: 0;
  font-size: 1.5rem;
`;

const DotoriCount = styled.div`
  background: rgba(255,255,255,0.9);
  padding: 8px 15px;
  border-radius: 20px;
  color: #8B4513;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 5px;
`;

// 대시보드 메인 영역 (3단 구조 - 더 넓게)
const DashboardBody = styled.div`
  background: #fff;
  min-height: 600px;
  display: grid;
  grid-template-columns: 300px 1fr 280px;
  gap: 20px;
  padding: 30px 20px 30px 20px;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    left: 20px;
    right: 20px;
    top: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, #FFB6C1, transparent);
  }
`;

// 왼쪽 프로필/캐릭터 영역
const LeftProfile = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

// 가운데 메인 컨텐츠
const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

// 오른쪽 메뉴 카테고리
const RightMenu = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

// 카드 공통 스타일 (덜 둥글게)
const Card = styled.div<{ bgColor?: string }>`
  background: ${props => props.bgColor || 'linear-gradient(135deg, #F0F8FF, #E6E6FA)'};
  border: 2px solid #DDA0DD;
  border-radius: 6px;
  padding: 15px;
  box-shadow: 
    0 2px 6px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.5);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    animation: ${sparkle} 4s ease-in-out infinite;
  }
`;

const CardTitle = styled.h3`
  color: #8B008B;
  margin: 0 0 15px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2rem;
`;

// 사주팔자 그리드
const SajuGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 15px;
`;

const SajuPillar = styled.div`
  background: linear-gradient(135deg, #FFE4E1, #F0E68C);
  border: 2px solid #FFB6C1;
  border-radius: 5px;
  padding: 12px;
  text-align: center;
  position: relative;
  box-shadow: 
    0 2px 4px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.4);
`;

const PillarTitle = styled.div`
  font-size: 12px;
  color: #8B008B;
  font-weight: bold;
  margin-bottom: 8px;
`;

const PillarChar = styled.div`
  font-size: 18px;
  font-weight: bold;
  color: #B22222;
  margin: 3px 0;
`;

// 오행 프로그레스 바
const WuxingSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const WuxingItem = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const WuxingName = styled.div<{ color: string }>`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 14px;
`;

const ProgressBar = styled.div`
  flex: 1;
  height: 18px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  border: 1px solid #ddd;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
`;

const ProgressFill = styled.div<{ width: number; color: string }>`
  width: ${props => props.width}%;
  height: 100%;
  background: ${props => props.color};
  border-radius: 3px;
  transition: width 1s ease-in-out;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    animation: ${sparkle} 2s ease-in-out infinite;
  }
`;

const WuxingCount = styled.div`
  font-weight: bold;
  color: #8B008B;
  min-width: 30px;
`;

// Updated News 섹션 (싸이월드 스타일)
const UpdatedNews = styled.div`
  background: 
    linear-gradient(135deg, #E6F3FF 0%, #F0E6FF 100%);
  border: 2px solid #87CEEB;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  position: relative;
  box-shadow: 
    inset 0 1px 0 rgba(255,255,255,0.5),
    0 3px 8px rgba(135,206,235,0.2);
  
  &::before {
    content: '📢 UPDATED NEWS';
    position: absolute;
    top: -12px;
    left: 15px;
    background: linear-gradient(135deg, #4682B4, #87CEEB);
    color: white;
    padding: 5px 15px;
    border-radius: 15px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  }
`;

const NewsItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  font-size: 12px;
  color: #4682B4;
  font-weight: 500;
  border-bottom: 1px dotted rgba(135,206,235,0.3);
  
  &:last-child {
    border-bottom: none;
  }
  
  &::before {
    content: '✨';
    font-size: 11px;
    animation: ${sparkle} 2s ease-in-out infinite;
  }
  
  &:nth-child(2n)::before {
    content: '💫';
  }
  
  &:nth-child(3n)::before {
    content: '🎊';
  }
`;

// 미니미 친구들 섹션
const MinimiFriends = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  padding: 15px;
  background: 
    radial-gradient(ellipse at center, rgba(135,206,235,0.1) 0%, transparent 70%);
  border-radius: 15px;
  margin: 15px 0;
`;

const MinimiFriend = styled.div`
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: linear-gradient(135deg, #FFE4E1, #E6E6FA);
  border: 2px solid #fff;
  box-shadow: 
    0 2px 4px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.5);
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
  }
  
  &:nth-child(odd) {
    animation: ${bounce} 3s ease-in-out infinite;
  }
`;

// 미니 방명록
const GuestBook = styled.div`
  max-height: 180px;
  overflow-y: auto;
`;

const GuestBookEntry = styled.div`
  background: rgba(255,182,193,0.1);
  border-left: 4px solid #FFB6C1;
  padding: 10px;
  margin: 8px 0;
  border-radius: 0 8px 8px 0;
`;

const GuestName = styled.div`
  font-weight: bold;
  color: #8B008B;
  font-size: 12px;
`;

const GuestMessage = styled.div`
  color: #666;
  font-size: 13px;
  margin-top: 5px;
`;

// 도토리 점수
const ScoreItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #DDA0DD;
  
  &:last-child {
    border-bottom: none;
  }
`;

const ScoreDotori = styled.div`
  display: flex;
  gap: 3px;
`;

const Dotori = styled.span<{ filled: boolean }>`
  font-size: 16px;
  opacity: ${props => props.filled ? 1 : 0.3};
  filter: ${props => props.filled ? 'drop-shadow(0 0 3px gold)' : 'none'};
`;

// BGM 플레이어 (싸이월드 스타일)
const BGMPlayer = styled.div`
  background: 
    linear-gradient(135deg, #4682B4 0%, #6BB6FF 50%, #87CEEB 100%);
  color: white;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255,255,255,0.3);
  box-shadow: 
    inset 0 1px 0 rgba(255,255,255,0.3),
    0 4px 12px rgba(70,130,180,0.3);
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    animation: ${sparkle} 3s ease-in-out infinite;
  }
`;

const PlayButton = styled.div`
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: rgba(255,255,255,0.5);
    transform: scale(1.1);
  }
`;

// 프로필 캐릭터 카드 (덜 둥글게)
const ProfileCard = styled.div`
  background: linear-gradient(135deg, #E6F3FF, #F0E6FF);
  border: 2px solid #87CEEB;
  border-radius: 6px;
  padding: 15px;
  text-align: center;
  box-shadow: 
    0 2px 6px rgba(135,206,235,0.2),
    inset 0 1px 0 rgba(255,255,255,0.6);
`;

const LargeAvatar = styled.div`
  width: 120px;
  height: 120px;
  background: 
    url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiBmaWxsPSIjRkZGIi8+CjwhLS0gZ2FsY29uZyBoYWlyIC0tPgo8ZWxsaXBzZSBjeD0iNjAiIGN5PSIyOCIgcng9IjI4IiByeT0iMzIiIGZpbGw9IiM4QjQ1MTMiLz4KPGV2aWxsaXBzZSBjeD0iNjAiIGN5PSIyNSIgcng9IjI1IiByeT0iMjgiIGZpbGw9IiNCMjIyMjIiLz4KCjwhLS0gZmFjZSAtLT4KPGVsbGlwc2UgY3g9IjYwIiBjeT0iNTUiIHJ4PSIyMCIgcnk9IjI0IiBmaWxsPSIjRkZEQkI1Ii8+Cgo8IS0tIGV5ZXMgLS0+CjxjaXJjbGUgY3g9IjUyIiBjeT0iNTAiIHI9IjMiIGZpbGw9IiMwMDAiLz4KPGNpcmNsZSBjeD0iNjgiIGN5PSI1MCIgcj0iMyIgZmlsbD0iIzAwMCIvPgo8Y2lyY2xlIGN4PSI1MSIgY3k9IjQ5IiByPSIxIiBmaWxsPSIjRkZGIi8+CjxjaXJjbGUgY3g9IjY3IiBjeT0iNDkiIHI9IjEiIGZpbGw9IiNGRkYiLz4KCjwhLS0gbm9zZSAtLT4KPGVsbGlwc2UgY3g9IjYwIiBjeT0iNTciIHJ4PSIyIiByeT0iMyIgZmlsbD0iI0ZGQzFBMCIvPgoKPCEtLSBtb3V0aCAtLT4KPGVsbGlwc2UgY3g9IjYwIiBjeT0iNjUiIHJ4PSI0IiByeT0iMiIgZmlsbD0iI0ZGNjk5NCIvPgoKPCEtLSBib2R5IC0tPgo8ZWxsaXBzZSBjeD0iNjAiIGN5PSI5MCIgcng9IjE4IiByeT0iMjAiIGZpbGw9IiM4N0NFRUIiLz4KPGVsbGlwc2UgY3g9IjYwIiBjeT0iODgiIHJ4PSIxNiIgcnk9IjE4IiBmaWxsPSIjNDY4MkI0Ii8+Cgo8IS0tIGFybXMgLS0+CjxlbGxpcHNlIGN4PSI0MyIgY3k9Ijg1IiByeD0iNiIgcnk9IjEyIiBmaWxsPSIjRkZEQkI1IiB0cmFuc2Zvcm09InJvdGF0ZSgtMzAgNDMgODUpIi8+CjxlbGxpcHNlIGN4PSI3NyIgY3k9Ijg1IiByeD0iNiIgcnk9IjEyIiBmaWxsPSIjRkZEQkI1IiB0cmFuc2Zvcm09InJvdGF0ZSgzMCA3NyA4NSkiLz4KPC9zdmc+'),
    linear-gradient(135deg, #FFF8DC, #F0E68C);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 6px;
  border: 3px solid #fff;
  box-shadow: 
    0 0 0 1px #87CEEB,
    0 3px 8px rgba(0,0,0,0.15),
    inset 0 1px 2px rgba(255,255,255,0.6);
  margin: 0 auto 15px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    top: -2px;
    right: -2px;
    width: 14px;
    height: 14px;
    background: radial-gradient(circle, #32CD32, #228B22);
    border-radius: 50%;
    border: 2px solid #fff;
    animation: ${sparkle} 2s ease-in-out infinite;
    box-shadow: 0 0 6px rgba(50,205,50,0.5);
  }
`;

const ProfileInfo = styled.div`
  text-align: center;
`;

const ProfileName = styled.div`
  font-size: 16px;
  font-weight: bold;
  color: #4682B4;
  margin-bottom: 8px;
`;

const ProfileStatus = styled.div`
  font-size: 12px;
  color: #666;
  background: rgba(135,206,235,0.1);
  padding: 5px 10px;
  border-radius: 15px;
  margin: 8px 0;
`;

// 책갈피 스타일 메뉴 카테고리 (샘플4 스타일)
const MenuCategory = styled.div`
  position: relative;
  margin-bottom: 0;
  z-index: ${props => props.index || 1};
`;

const MenuTab = styled.div<{ isActive?: boolean; tabColor?: string }>`
  background: ${props => props.tabColor || 'linear-gradient(135deg, #4169E1, #6495ED)'};
  color: white;
  padding: 8px 15px 8px 12px;
  font-size: 11px;
  font-weight: bold;
  text-align: center;
  letter-spacing: 0.3px;
  text-shadow: 0 1px 1px rgba(0,0,0,0.4);
  cursor: pointer;
  position: relative;
  border-radius: 0;
  box-shadow: 
    2px 0 4px rgba(0,0,0,0.2),
    inset 0 1px 0 rgba(255,255,255,0.3);
  transform: ${props => props.isActive ? 'translateX(0)' : 'translateX(0)'};
  transition: all 0.2s ease;
  border-left: 3px solid rgba(255,255,255,0.4);
  border-right: 1px solid rgba(0,0,0,0.2);
  
  /* 책갈피 모양 만들기 */
  &::after {
    content: '';
    position: absolute;
    right: -8px;
    top: 0;
    bottom: 0;
    width: 0;
    height: 0;
    border-left: 8px solid ${props => props.tabColor?.includes('4169E1') ? '#4169E1' : '#6495ED'};
    border-top: ${props => props.isActive ? '16px' : '15px'} solid transparent;
    border-bottom: ${props => props.isActive ? '16px' : '15px'} solid transparent;
    z-index: 1;
  }
  
  &::before {
    content: '';
    position: absolute;
    right: -9px;
    top: 0;
    bottom: 0;
    width: 0;
    height: 0;
    border-left: 9px solid rgba(0,0,0,0.1);
    border-top: ${props => props.isActive ? '16px' : '15px'} solid transparent;
    border-bottom: ${props => props.isActive ? '16px' : '15px'} solid transparent;
    z-index: 0;
  }
  
  &:hover {
    transform: translateX(-2px);
    box-shadow: 
      4px 0 6px rgba(0,0,0,0.25),
      inset 0 1px 0 rgba(255,255,255,0.4);
  }
  
  ${props => props.isActive && `
    transform: translateX(-3px);
    z-index: 10;
    box-shadow: 
      5px 0 8px rgba(0,0,0,0.3),
      inset 0 1px 0 rgba(255,255,255,0.5);
  `}
`;

const MenuContent = styled.div<{ isActive?: boolean }>`
  position: absolute;
  top: 0;
  right: -180px;
  width: 170px;
  background: rgba(255,255,255,0.98);
  border: 2px solid #87CEEB;
  border-radius: 6px;
  box-shadow: 
    0 4px 12px rgba(0,0,0,0.2),
    inset 0 1px 0 rgba(255,255,255,0.8);
  display: ${props => props.isActive ? 'block' : 'none'};
  z-index: 100;
  backdrop-filter: blur(2px);
`;

const MenuItem = styled.div`
  padding: 8px 12px;
  color: #4682B4;
  font-size: 11px;
  font-weight: normal;
  border-bottom: 1px dotted #D6E9FF;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  gap: 6px;
  position: relative;
  
  &:last-child {
    border-bottom: none;
  }
  
  &::before {
    content: '·';
    color: #87CEEB;
    font-weight: bold;
  }
  
  &:hover {
    background: linear-gradient(90deg, #E6F3FF, #F0F8FF);
    color: #2F4F4F;
    transform: translateX(2px);
  }
  
  &.active {
    background: linear-gradient(90deg, #D6E9FF, #E6F3FF);
    color: #2F4F4F;
    font-weight: bold;
    border-left: 3px solid #87CEEB;
    
    &::before {
      content: '▶';
      color: #4682B4;
    }
  }
`;

const CyworldSajuTestPage: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('home');
  
  const wuxingData = [
    { name: '木', color: '#228B22', count: 2, max: 5 },
    { name: '火', color: '#DC143C', count: 4, max: 5 },
    { name: '土', color: '#DAA520', count: 1, max: 5 },
    { name: '金', color: '#C0C0C0', count: 3, max: 5 },
    { name: '水', color: '#4169E1', count: 2, max: 5 }
  ];

  const fortuneScores = [
    { name: '연애운', score: 4 },
    { name: '재물운', score: 3 },
    { name: '건강운', score: 5 },
    { name: '사업운', score: 2 },
    { name: '학업운', score: 4 }
  ];

  const tabColors = {
    home: 'linear-gradient(135deg, #4169E1, #6495ED)',
    profile: 'linear-gradient(135deg, #FF6347, #FF7F50)', 
    diary: 'linear-gradient(135deg, #32CD32, #98FB98)',
    friends: 'linear-gradient(135deg, #FF69B4, #FFB6C1)'
  };

  return (
    <CyworldContainer>
      <NotebookContainer>
        {/* 미니홈피 헤더 */}
        <MinihompyHeader>
          <UserInfo>
            <Avatar>🔮</Avatar>
            <div>
              <UserName>홍길동님의 사주 미니홈피</UserName>
              <div style={{ color: 'rgba(255,255,255,0.9)', fontSize: '14px' }}>
                오늘도 좋은 하루 되세요! ✨
              </div>
            </div>
          </UserInfo>
          <DotoriCount>
            <span>🌰</span>
            <span>1,234 도토리</span>
          </DotoriCount>
        </MinihompyHeader>

      {/* 대시보드 메인 */}
      <DashboardBody>
        {/* 왼쪽 프로필 영역 */}
        <LeftProfile>
          {/* 프로필 캐릭터 */}
          <ProfileCard>
            <LargeAvatar></LargeAvatar>
            <ProfileInfo>
              <ProfileName>홍길동</ProfileName>
              <ProfileStatus>🌟 운세분석 중 🌟</ProfileStatus>
              <div style={{ fontSize: '11px', color: '#888', marginTop: '8px' }}>
                1990.05.15 (오후 2시)<br/>
                사주팔자 운명학 전문
              </div>
            </ProfileInfo>
          </ProfileCard>

          {/* 오늘의 운세 */}
          <Card bgColor="linear-gradient(135deg, #FFE4B5, #FFEFD5)">
            <CardTitle style={{ fontSize: '13px' }}>
              🔮 오늘의 운세
            </CardTitle>
            <div style={{ fontSize: '12px', lineHeight: '1.5', color: '#8B4513' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>종합운:</strong> ⭐⭐⭐⭐☆
              </div>
              <div style={{ fontSize: '11px', color: '#666' }}>
                오늘은 새로운 기회가 찾아올 수 있는 날입니다. 
                특히 오후에 좋은 소식이 있을 것 같아요.
              </div>
            </div>
          </Card>

          {/* BGM 플레이어 */}
          <Card bgColor="linear-gradient(135deg, #4682B4, #6BB6FF)">
            <BGMPlayer>
              <PlayButton>▶️</PlayButton>
              <div style={{ fontSize: '11px', opacity: '0.9', marginBottom: '3px' }}>
                🎵 NOW PLAYING
              </div>
              <div style={{ fontSize: '13px', fontWeight: 'bold', marginBottom: '2px' }}>
                첫사랑 - 터보
              </div>
              <div style={{ fontSize: '10px', opacity: '0.8' }}>
                추억의 BGM ♪ (무한반복)
              </div>
            </BGMPlayer>
          </Card>

          {/* 미니미 친구들 */}
          <Card bgColor="linear-gradient(135deg, #F0F8FF, #E6E6FA)">
            <CardTitle style={{ fontSize: '13px' }}>
              👫 놀러온 친구들
            </CardTitle>
            <MinimiFriends>
              <MinimiFriend>🧑</MinimiFriend>
              <MinimiFriend>👩</MinimiFriend>
              <MinimiFriend>🧑‍💼</MinimiFriend>
              <MinimiFriend>👩‍🎨</MinimiFriend>
              <MinimiFriend>🧑‍🚀</MinimiFriend>
              <MinimiFriend>👩‍🔬</MinimiFriend>
              <MinimiFriend>🧑‍🎓</MinimiFriend>
              <MinimiFriend>👩‍⚕️</MinimiFriend>
            </MinimiFriends>
            <div style={{ textAlign: 'center', fontSize: '10px', color: '#8B008B' }}>
              총 8명의 친구가 놀러왔어요! 🎉
            </div>
          </Card>

          {/* 개인 통계 */}
          <Card bgColor="linear-gradient(135deg, #E0E6FF, #F0F4FF)">
            <CardTitle style={{ fontSize: '13px' }}>
              📊 나의 통계
            </CardTitle>
            <div style={{ fontSize: '11px', color: '#4682B4' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span>총 방문수:</span>
                <strong>2,024회</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span>오늘 방문:</span>
                <strong>1회</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span>사주 분석:</span>
                <strong>15회</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>도토리:</span>
                <strong style={{ color: '#D2691E' }}>🌰 1,234개</strong>
              </div>
            </div>
          </Card>
        </LeftProfile>

        {/* 가운데 메인 컨텐츠 */}
        <MainContent>
          {/* 사주팔자 섹션 */}
          <Card bgColor="linear-gradient(135deg, #FFE4E1, #F0F8FF)">
            <CardTitle>
              🎯 나의 사주팔자
            </CardTitle>
            <SajuGrid>
              <SajuPillar>
                <PillarTitle>년주</PillarTitle>
                <PillarChar>庚</PillarChar>
                <PillarChar>午</PillarChar>
              </SajuPillar>
              <SajuPillar>
                <PillarTitle>월주</PillarTitle>
                <PillarChar>辛</PillarChar>
                <PillarChar>巳</PillarChar>
              </SajuPillar>
              <SajuPillar>
                <PillarTitle>일주</PillarTitle>
                <PillarChar>乙</PillarChar>
                <PillarChar>卯</PillarChar>
              </SajuPillar>
              <SajuPillar>
                <PillarTitle>시주</PillarTitle>
                <PillarChar>戊</PillarChar>
                <PillarChar>午</PillarChar>
              </SajuPillar>
            </SajuGrid>
            <div style={{ textAlign: 'center', color: '#8B008B', fontSize: '14px' }}>
              💫 1990년 5월 15일 14시 태생 💫
            </div>
          </Card>

          {/* 오행 분석 섹션 */}
          <Card bgColor="linear-gradient(135deg, #F0E68C, #FFE4E1)">
            <CardTitle>
              🌈 오행 밸런스 체크
            </CardTitle>
            <WuxingSection>
              {wuxingData.map((item) => (
                <WuxingItem key={item.name}>
                  <WuxingName color={item.color}>{item.name}</WuxingName>
                  <ProgressBar>
                    <ProgressFill 
                      width={(item.count / item.max) * 100} 
                      color={item.color}
                    />
                  </ProgressBar>
                  <WuxingCount>{item.count}/{item.max}</WuxingCount>
                </WuxingItem>
              ))}
            </WuxingSection>
          </Card>

          {/* 성격 분석 카드 */}
          <Card bgColor="linear-gradient(135deg, #E6E6FA, #F0F8FF)">
            <CardTitle>
              🎭 성격 분석
            </CardTitle>
            <div style={{ 
              background: 'rgba(255,182,193,0.2)', 
              padding: '15px', 
              borderRadius: '10px',
              lineHeight: '1.6'
            }}>
              <div style={{ color: '#8B008B', fontWeight: 'bold', marginBottom: '10px' }}>
                ✨ 당신은 창의적이고 감성적인 타입이에요!
              </div>
              <div style={{ color: '#666', fontSize: '14px' }}>
                • 예술적 감각이 뛰어나고 상상력이 풍부해요<br/>
                • 다른 사람의 감정을 잘 이해하는 공감 능력이 높아요<br/>
                • 때로는 완벽주의 성향으로 스트레스를 받기도 해요<br/>
                • 새로운 도전을 좋아하고 변화에 잘 적응해요
              </div>
            </div>
          </Card>
        </MainContent>

        {/* 오른쪽 책갈피 메뉴 */}
        <RightMenu>
          {/* Updated News */}
          <UpdatedNews>
            <div style={{ marginTop: '10px' }}>
              <NewsItem>사주팔자 분석 시스템 대폭 업그레이드! (신규)</NewsItem>
              <NewsItem>AI 명리학 해석 서비스 오픈 기념 이벤트 진행중</NewsItem>
              <NewsItem>친구와 궁합 분석하고 도토리 받아가세요~</NewsItem>
            </div>
          </UpdatedNews>

          {/* 운세 도토리 점수 */}
          <Card style={{ marginBottom: '15px' }}>
            <CardTitle style={{ fontSize: '12px' }}>
              🌰 운세 도토리 점수
            </CardTitle>
            {fortuneScores.map((item) => (
              <ScoreItem key={item.name}>
                <span style={{ color: '#8B008B', fontWeight: 'bold', fontSize: '11px' }}>
                  {item.name}
                </span>
                <ScoreDotori>
                  {[...Array(5)].map((_, i) => (
                    <Dotori key={i} filled={i < item.score}>
                      🌰
                    </Dotori>
                  ))}
                </ScoreDotori>
              </ScoreItem>
            ))}
          </Card>

          {/* HOME 책갈피 */}
          <MenuCategory style={{ marginBottom: '5px' }}>
            <MenuTab 
              isActive={activeTab === 'home'}
              tabColor={tabColors.home}
              onClick={() => setActiveTab(activeTab === 'home' ? '' : 'home')}
            >
              🏠 HOME
            </MenuTab>
            <MenuContent isActive={activeTab === 'home'}>
              <MenuItem className="active">🔮 사주분석</MenuItem>
              <MenuItem>💕 궁합보기</MenuItem>
              <MenuItem>🌟 오늘운세</MenuItem>
              <MenuItem>📊 통계보기</MenuItem>
            </MenuContent>
          </MenuCategory>

          {/* PROFILE 책갈피 */}
          <MenuCategory style={{ marginBottom: '5px' }}>
            <MenuTab 
              isActive={activeTab === 'profile'}
              tabColor={tabColors.profile}
              onClick={() => setActiveTab(activeTab === 'profile' ? '' : 'profile')}
            >
              👤 PROFILE
            </MenuTab>
            <MenuContent isActive={activeTab === 'profile'}>
              <MenuItem>📝 내정보</MenuItem>
              <MenuItem>🎭 성격분석</MenuItem>
              <MenuItem>💼 직업운</MenuItem>
              <MenuItem>❤️ 연애운</MenuItem>
            </MenuContent>
          </MenuCategory>

          {/* DIARY 책갈피 */}
          <MenuCategory style={{ marginBottom: '5px' }}>
            <MenuTab 
              isActive={activeTab === 'diary'}
              tabColor={tabColors.diary}
              onClick={() => setActiveTab(activeTab === 'diary' ? '' : 'diary')}
            >
              📔 DIARY
            </MenuTab>
            <MenuContent isActive={activeTab === 'diary'}>
              <MenuItem>📅 대운분석</MenuItem>
              <MenuItem>🌙 세운분석</MenuItem>
              <MenuItem>💫 운세달력</MenuItem>
              <MenuItem>📈 운세그래프</MenuItem>
            </MenuContent>
          </MenuCategory>

          {/* FRIENDS 책갈피 */}
          <MenuCategory style={{ marginBottom: '5px' }}>
            <MenuTab 
              isActive={activeTab === 'friends'}
              tabColor={tabColors.friends}
              onClick={() => setActiveTab(activeTab === 'friends' ? '' : 'friends')}
            >
              👥 FRIENDS
            </MenuTab>
            <MenuContent isActive={activeTab === 'friends'}>
              <MenuItem>💌 방명록</MenuItem>
              <MenuItem>🎁 선물하기</MenuItem>
              <MenuItem>📞 친구찾기</MenuItem>
              <MenuItem>💬 1촌평</MenuItem>
            </MenuContent>
          </MenuCategory>

          {/* 미니 방명록 */}
          <Card style={{ marginTop: '20px' }}>
            <CardTitle style={{ fontSize: '12px' }}>
              💌 운세 방명록
            </CardTitle>
            <GuestBook>
              <GuestBookEntry>
                <GuestName>🔮 운세요정</GuestName>
                <GuestMessage>
                  올해는 새로운 기회가 많이 찾아올 거예요! 용기내서 도전해보세요 ✨
                </GuestMessage>
              </GuestBookEntry>
              <GuestBookEntry>
                <GuestName>💫 별님</GuestName>
                <GuestMessage>
                  화 기운이 강해서 열정적이시네요! 건강 관리만 잘 하시면 될 것 같아요~
                </GuestMessage>
              </GuestBookEntry>
              <GuestBookEntry>
                <GuestName>🌙 달빛</GuestName>
                <GuestMessage>
                  대인관계에서 좋은 일이 생길 것 같아요. 주변 사람들을 소중히 하세요!
                </GuestMessage>
              </GuestBookEntry>
            </GuestBook>
          </Card>

          {/* 오늘의 럭키 아이템 */}
          <Card bgColor="linear-gradient(135deg, #FFE4E1, #F0E68C)">
            <CardTitle style={{ fontSize: '12px' }}>
              🍀 오늘의 럭키 아이템
            </CardTitle>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '35px', margin: '10px 0' }}>💍</div>
              <div style={{ color: '#8B008B', fontWeight: 'bold', fontSize: '13px' }}>
                금반지
              </div>
              <div style={{ fontSize: '11px', color: '#666', marginTop: '5px' }}>
                금 기운으로 재물운 UP!
              </div>
            </div>
          </Card>

          {/* 이번 주 운세 */}
          <Card bgColor="linear-gradient(135deg, #E6E6FA, #F8F8FF)">
            <CardTitle style={{ fontSize: '12px' }}>
              📅 이번 주 운세
            </CardTitle>
            <div style={{ fontSize: '11px', color: '#4B0082' }}>
              <div style={{ marginBottom: '8px', padding: '6px', background: 'rgba(75,0,130,0.1)', borderRadius: '4px' }}>
                <strong>월:</strong> 새로운 시작 🌟<br/>
                <strong>화:</strong> 인간관계 주의 ⚠️<br/>
                <strong>수:</strong> 금전운 상승 💰<br/>
                <strong>목:</strong> 건강 체크 🏥<br/>
                <strong>금:</strong> 좋은 소식 📬<br/>
                <strong>토:</strong> 휴식 필요 😴<br/>
                <strong>일:</strong> 가족과 시간 👨‍👩‍👧‍👦
              </div>
            </div>
          </Card>

          {/* 사주 통계 */}
          <Card bgColor="linear-gradient(135deg, #F0FFF0, #E0FFE0)">
            <CardTitle style={{ fontSize: '12px' }}>
              📈 사주 분석 리포트
            </CardTitle>
            <div style={{ fontSize: '11px', color: '#228B22' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span>오행 균형도:</span>
                <strong>75%</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span>행운 지수:</span>
                <strong>88%</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span>성격 적합도:</span>
                <strong>92%</strong>
              </div>
              <div style={{ marginTop: '8px', padding: '6px', background: 'rgba(34,139,34,0.1)', borderRadius: '4px', fontSize: '10px' }}>
                💡 <strong>추천:</strong> 이번 달은 새로운 취미 활동을 시작하기 좋은 시기예요!
              </div>
            </div>
          </Card>
        </RightMenu>
      </DashboardBody>
      </NotebookContainer>
    </CyworldContainer>
  );
};

export default CyworldSajuTestPage;