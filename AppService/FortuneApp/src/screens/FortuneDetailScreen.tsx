/**
 * 확장운세 상세 화면
 * 각 운세별 세부 분석 결과 표시
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../navigation/types';
import { getExtendedFortune, getExtendedFortunePhase2, getLoveFortune, getPersonalityFortune, getRelationshipFortune, getWealthFortune, getCareerFortune, getHealthFortune, getStudyFortune, getFamilyFortune } from '../services/sajuApi';
import { convertToSajuRequest } from '../utils/dataMapper';
import type { ExtendedFortunePhase1, ExtendedFortunePhase2 } from '../types/saju';

type Props = NativeStackScreenProps<RootStackParamList, 'FortuneDetail'>;

export interface FortuneDetailParams {
  fortuneType: string;
  title: string;
  icon: string;
  color: string;
  phase: 1 | 2;
  // 사주 정보 (이전 분석에서 가져오거나 재입력)
  birthInfo?: {
    birthDate: string;
    birthTime: string;
    gender: string;
    name?: string;
  };
}

const FortuneDetailScreen: React.FC<Props> = ({ navigation, route }) => {
  const { fortuneType, title, icon, color, phase, birthInfo } = route.params as FortuneDetailParams;
  
  const [fortuneData, setFortuneData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 확장운세 데이터 로드
  const loadFortuneData = async () => {
    if (!birthInfo) {
      Alert.alert('정보 필요', '사주 분석을 먼저 진행해주세요.', [
        { text: '확인', onPress: () => navigation.goBack() }
      ]);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // UI 입력값을 API 형식으로 변환
      const requestData = convertToSajuRequest(
        birthInfo.birthDate,
        birthInfo.birthTime,
        birthInfo.gender,
        birthInfo.name
      );

      if (!requestData) {
        throw new Error('사주 정보 처리에 실패했습니다.');
      }

      let response;
      if (phase === 1) {
        // Phase 1 운세별 API 호출 - 모두 getExtendedFortune 사용
        switch (fortuneType) {
          case 'love':
            response = await getLoveFortune(requestData);
            break;
          case 'residence':
          case 'transportation':
          case 'social':
          case 'hobby':
            response = await getExtendedFortune(requestData);
            break;
          default:
            response = await getExtendedFortune(requestData);
        }
      } else {
        // Phase 2 운세별 개별 API 호출
        switch (fortuneType) {
          case 'career':
            response = await getCareerFortune(requestData);
            break;
          case 'health':
            response = await getHealthFortune(requestData);
            break;
          case 'study':
            response = await getStudyFortune(requestData);
            break;
          case 'family':
            response = await getFamilyFortune(requestData);
            break;
          default:
            response = await getExtendedFortunePhase2(requestData);
        }
      }

      if (response.success && response.data) {
        console.log('🎉 확장운세 API 응답 성공:', response.data);
        console.log('🔍 fortuneType:', fortuneType);
        console.log('🔍 phase:', phase);
        // API 응답이 {success: true, data: {...}} 형태이므로 .data로 접근
        setFortuneData(response.data.data || response.data);
      } else {
        console.error('❌ 확장운세 API 응답 실패:', response);
        throw new Error(response.error || '확장운세 분석에 실패했습니다.');
      }
    } catch (error) {
      console.error('확장운세 로드 오류:', error);
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadFortuneData();
  }, []);

  // 운세 타입별 데이터 렌더링
  const renderFortuneContent = () => {
    console.log('🎨 렌더링 시작 - fortuneData:', fortuneData);
    console.log('🎨 렌더링 시작 - fortuneType:', fortuneType);
    console.log('🎨 렌더링 시작 - phase:', phase);
    
    if (!fortuneData) {
      console.log('❌ fortuneData가 null입니다');
      return null;
    }


    // Phase 1 확장운세
    if (phase === 1) {
      switch (fortuneType) {
        case 'love':
          // 연애운 전용 렌더링
          return renderLoveFortune(fortuneData.love_fortune_analysis);
        case 'residence':
          // 주거운 렌더링
          return renderExtendedFortune('🏠 주거운', fortuneData, fortuneType);
        case 'transportation':
          return renderExtendedFortune('🚗 교통운', fortuneData, fortuneType);
        case 'social':
          return renderExtendedFortune('👥 소셜운', fortuneData, fortuneType);
        case 'hobby':
          return renderExtendedFortune('🎨 취미운', fortuneData, fortuneType);
      }
    }

    // Phase 2 확장운세
    if (phase === 2) {
      switch (fortuneType) {
        case 'career':
          return renderCareerFortune(fortuneData.career_fortune);
        case 'health':
          return renderSimpleFortune('건강운', '💊', fortuneData.health_fortune);
        case 'study':
          return renderSimpleFortune('학업운', '📚', fortuneData.study_fortune);
        case 'family':
          return renderFamilyFortune(fortuneData.family_fortune);
      }
    }

    return null;
  };

  // 연애운 전용 렌더링 함수
  const renderLoveFortune = (loveData: any) => {
    if (!loveData) return null;

    return (
      <View style={styles.sectionContainer}>
        <Text style={styles.sectionTitle}>💕 연애운</Text>
        
        {/* 이상형 */}
        {loveData.ideal_type && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>✨ 이상형</Text>
            <Text style={styles.subSectionContent}>
              {loveData.ideal_type.description}
            </Text>
            {loveData.ideal_type.key_traits && (
              <Text style={styles.subSectionContent}>
                주요 특징: {loveData.ideal_type.key_traits.join(', ')}
              </Text>
            )}
          </View>
        )}

        {/* 연애 스타일 */}
        {loveData.love_style && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>💖 연애 스타일</Text>
            <Text style={styles.subSectionContent}>
              {loveData.love_style.description}
            </Text>
            {loveData.love_style.approach && (
              <Text style={styles.subSectionContent}>
                접근법: {loveData.love_style.approach}
              </Text>
            )}
            {loveData.love_style.strengths && (
              <Text style={styles.subSectionContent}>
                강점: {loveData.love_style.strengths.join(', ')}
              </Text>
            )}
          </View>
        )}

        {/* 결혼 타이밍 */}
        {loveData.marriage_timing && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>💒 결혼 타이밍</Text>
            <Text style={styles.subSectionContent}>
              이른 시기: {loveData.marriage_timing.early}세
            </Text>
            <Text style={styles.subSectionContent}>
              이상적 시기: {loveData.marriage_timing.ideal}세
            </Text>
            <Text style={styles.subSectionContent}>
              늦은 시기: {loveData.marriage_timing.late}세
            </Text>
          </View>
        )}

        {/* 월별 운세 */}
        {loveData.monthly_fortune && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>📅 월별 운세</Text>
            {loveData.monthly_fortune.best_months && (
              <Text style={styles.subSectionContent}>
                좋은 달: {loveData.monthly_fortune.best_months.join(', ')}
              </Text>
            )}
            {loveData.monthly_fortune.caution_months && (
              <Text style={styles.subSectionContent}>
                주의할 달: {loveData.monthly_fortune.caution_months.join(', ')}
              </Text>
            )}
            {loveData.monthly_fortune.advice && (
              <Text style={styles.subSectionContent}>
                조언: {loveData.monthly_fortune.advice}
              </Text>
            )}
          </View>
        )}
      </View>
    );
  };

  // Phase 1 확장운세 전용 렌더링 함수 (운세 타입별 렌더링)
  const renderExtendedFortune = (title: string, extendedData: any, fortuneType: string) => {
    if (!extendedData) return null;

    console.log(`🎨 ${title} 확장운세 데이터:`, extendedData);
    console.log(`🎯 운세 타입: ${fortuneType}`);

    // 운세 타입에 따른 데이터 키 매핑
    const fortuneKeyMap: { [key: string]: string } = {
      'residence': 'residence_fortune',
      'transportation': 'transportation_fortune', 
      'social': 'social_fortune',
      'hobby': 'hobby_fortune'
    };

    const dataKey = fortuneKeyMap[fortuneType];
    const fortuneData = extendedData[dataKey];

    console.log(`🔑 데이터 키: ${dataKey}, 운세 데이터:`, fortuneData);

    if (!fortuneData) {
      return (
        <View style={styles.sectionContainer}>
          <Text style={styles.sectionTitle}>{title}</Text>
          <Text style={styles.subSectionContent}>
            운세 데이터를 불러오는 중입니다...
          </Text>
        </View>
      );
    }

    return (
      <View style={styles.sectionContainer}>
        <Text style={styles.sectionTitle}>{title}</Text>
        
        {/* 각 운세별 필드들을 동적으로 렌더링 */}
        {Object.entries(fortuneData).map(([key, value]) => {
          if (!value) return null;
          
          return (
            <View key={key} style={styles.subSection}>
              <Text style={styles.subSectionTitle}>
                {getSubSectionTitle(key)}
              </Text>
              <Text style={styles.subSectionContent}>
                {Array.isArray(value) 
                  ? value.join(', ') 
                  : String(value)}
              </Text>
            </View>
          );
        })}
      </View>
    );
  };

  // 직업운 전용 렌더링 함수
  const renderCareerFortune = (careerData: any) => {
    if (!careerData) return null;

    return (
      <View style={styles.sectionContainer}>
        <Text style={styles.sectionTitle}>💼 직업운</Text>
        
        {/* 현재 직업 적성 */}
        {careerData.current_job_compatibility && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>🎯 현재 직업 적성</Text>
            <Text style={styles.subSectionContent}>
              {careerData.current_job_compatibility}
            </Text>
          </View>
        )}

        {/* 이직 타이밍 */}
        {careerData.career_change_timing && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>⏰ 이직 타이밍</Text>
            <Text style={styles.subSectionContent}>
              {careerData.career_change_timing}
            </Text>
          </View>
        )}

        {/* 승진 가능성 */}
        {careerData.promotion_potential && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>📈 승진 가능성</Text>
            <Text style={styles.subSectionContent}>
              {careerData.promotion_potential}
            </Text>
          </View>
        )}

        {/* 스킬 개발 */}
        {careerData.skill_development && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>💡 스킬 개발</Text>
            <Text style={styles.subSectionContent}>
              {careerData.skill_development}
            </Text>
          </View>
        )}

        {/* 업무 환경 */}
        {careerData.work_environment && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>🏢 업무 환경</Text>
            <Text style={styles.subSectionContent}>
              {careerData.work_environment}
            </Text>
          </View>
        )}
      </View>
    );
  };

  // 가족운 전용 렌더링 함수
  const renderFamilyFortune = (familyData: any) => {
    if (!familyData) return null;

    return (
      <View style={styles.sectionContainer}>
        <Text style={styles.sectionTitle}>👨‍👩‍👧‍👦 가족운</Text>
        
        {/* 부모 관계 */}
        {familyData.parent_relationship && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>👨‍👩 부모 관계</Text>
            <Text style={styles.subSectionContent}>
              {familyData.parent_relationship}
            </Text>
          </View>
        )}

        {/* 형제자매 화합 */}
        {familyData.sibling_harmony && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>👫 형제자매 화합</Text>
            <Text style={styles.subSectionContent}>
              {familyData.sibling_harmony}
            </Text>
          </View>
        )}

        {/* 자녀 계획 */}
        {familyData.child_planning && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>👶 자녀 계획</Text>
            <Text style={styles.subSectionContent}>
              {familyData.child_planning}
            </Text>
          </View>
        )}

        {/* 가족 모임 */}
        {familyData.family_gatherings && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>🎉 가족 모임</Text>
            <Text style={styles.subSectionContent}>
              {familyData.family_gatherings}
            </Text>
          </View>
        )}

        {/* 세대 갈등 */}
        {familyData.generational_conflict && (
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>⚡ 세대 갈등</Text>
            <Text style={styles.subSectionContent}>
              {familyData.generational_conflict}
            </Text>
          </View>
        )}
      </View>
    );
  };

  // 건강운/학업운 전용 렌더링 함수 (단순 텍스트용)
  const renderSimpleFortune = (title: string, icon: string, fortuneData: any) => {
    if (!fortuneData) return null;

    return (
      <View style={styles.sectionContainer}>
        <Text style={styles.sectionTitle}>{icon} {title}</Text>
        
        {/* 문자열인 경우 그대로 표시 */}
        {typeof fortuneData === 'string' ? (
          <Text style={styles.sectionContent}>{fortuneData}</Text>
        ) : (
          /* 객체인 경우 주요 필드들을 순회하며 표시 */
          Object.entries(fortuneData).map(([key, value]) => (
            <View key={key} style={styles.subSection}>
              <Text style={styles.subSectionTitle}>
                {getSubSectionTitle(key)}
              </Text>
              <Text style={styles.subSectionContent}>
                {Array.isArray(value) 
                  ? value.join(', ') 
                  : typeof value === 'object' && value !== null
                    ? JSON.stringify(value, null, 2)
                    : String(value)}
              </Text>
            </View>
          ))
        )}
      </View>
    );
  };

  // 서브섹션 제목 한글화
  const getSubSectionTitle = (key: string): string => {
    const titleMap: { [key: string]: string } = {
      // 연애운
      current_love_status: '현재 연애 상태',
      ideal_partner_type: '이상적인 파트너',
      love_advice: '연애 조언',
      relationship_timing: '연애 타이밍',
      compatibility_tips: '궁합 팁',
      
      // 주거운
      moving_direction: '🧭 이사 방향',
      avoid_direction: '⚠️ 피해야 할 방향',
      house_type: '🏠 추천 주택 유형',
      house_reason: '🔍 선택 이유',
      interior_colors: '🎨 인테리어 색상',
      room_layout: '📐 방 배치',
      best_moving_months: '📅 이사 적기',
      feng_shui_tips: '💡 풍수 팁',
      dominant_element: '⚡ 주요 원소',
      
      // 교통운
      vehicle_type: '🚗 추천 차량',
      vehicle_reason: '🔍 선택 이유',
      lucky_colors: '🌈 행운 색상',
      safe_directions: '🧭 안전 방향',
      driving_tips: '🚦 운전 팁',
      accident_prevention: '⚠️ 사고 예방',
      
      // 소셜운
      networking_style: '🤝 네트워킹 스타일',
      social_events: '🎉 추천 활동',
      communication_tips: '💬 소통 팁',
      leadership_potential: '👑 리더십 잠재력',
      relationship_advice: '💝 인간관계 조언',
      
      // 취미운
      recommended_hobbies: '🎯 추천 취미',
      creative_activities: '🎨 창작 활동',
      hobby_advice: '💡 취미 조언',
      skill_development: '📚 기술 개발',
      leisure_tips: '🌟 여가 팁',
      
      // 성격운
      core_personality: '핵심 성격',
      hidden_traits: '숨겨진 특성',
      growth_potential: '성장 가능성',
      social_style: '사회적 스타일',
      stress_management: '스트레스 관리',
      
      // 인간관계운
      social_compatibility: '사회적 호환성',
      leadership_style: '리더십 스타일',
      conflict_resolution: '갈등 해결',
      network_expansion: '네트워크 확장',
      trust_building: '신뢰 구축',
      
      // 재물운
      wealth_accumulation: '재물 축적',
      investment_style: '투자 성향',
      financial_advice: '재정 조언',
      income_sources: '수입원',
      spending_habits: '소비 습관',
      
      // 직업운
      current_job_compatibility: '현재 직업 적성',
      career_change_timing: '이직 타이밍',
      promotion_potential: '승진 가능성',
      skill_development: '스킬 개발',
      work_environment: '업무 환경',
      
      // 건강운
      physical_health: '신체 건강',
      mental_health: '정신 건강',
      disease_prevention: '질병 예방',
      exercise_recommendations: '운동 권장사항',
      dietary_advice: '식단 조언',
      
      // 학업운
      learning_ability: '학습 능력',
      exam_luck: '시험운',
      skill_acquisition: '기술 습득',
      academic_achievement: '학업 성취',
      knowledge_application: '지식 활용',
      
      // 가족운
      parent_relationship: '부모 관계',
      sibling_harmony: '형제자매 화합',
      child_planning: '자녀 계획',
      family_gatherings: '가족 모임',
      generational_conflict: '세대 갈등',
    };

    return titleMap[key] || key;
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={color} />
          <Text style={[styles.loadingText, { color }]}>
            {title} 분석 중...
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorIcon}>⚠️</Text>
          <Text style={styles.errorText}>{error}</Text>
          <TouchableOpacity
            style={[styles.retryButton, { backgroundColor: color }]}
            onPress={loadFortuneData}
          >
            <Text style={styles.retryButtonText}>다시 시도</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>돌아가기</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={[styles.header, { backgroundColor: color }]}>
        <TouchableOpacity
          style={styles.headerBackButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.headerBackText}>← 돌아가기</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{icon} {title}</Text>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.fortuneContainer}>
          {renderFortuneContent()}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFEDFA',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.3)',
  },
  headerBackButton: {
    marginRight: 15,
  },
  headerBackText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: 'white',
    flex: 1,
    textAlign: 'center',
    marginRight: 80,
  },
  content: {
    flex: 1,
  },
  fortuneContainer: {
    padding: 20,
  },
  sectionContainer: {
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#BE5985',
    marginBottom: 15,
    textAlign: 'center',
  },
  sectionContent: {
    fontSize: 14,
    color: '#BE5985',
    lineHeight: 20,
    textAlign: 'center',
  },
  subSection: {
    marginBottom: 12,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#FFE6F3',
  },
  subSectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#BE5985',
    marginBottom: 6,
  },
  subSectionContent: {
    fontSize: 13,
    color: '#BE5985',
    lineHeight: 18,
    opacity: 0.8,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 15,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorIcon: {
    fontSize: 48,
    marginBottom: 15,
  },
  errorText: {
    fontSize: 16,
    color: '#D32F2F',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 22,
  },
  retryButton: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 25,
    marginBottom: 10,
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  backButton: {
    paddingVertical: 10,
    paddingHorizontal: 20,
  },
  backButtonText: {
    color: '#BE5985',
    fontSize: 14,
    fontWeight: '500',
  },
});

export default FortuneDetailScreen;