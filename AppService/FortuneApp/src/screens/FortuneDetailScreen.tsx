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
import { getExtendedFortune, getExtendedFortunePhase2 } from '../services/sajuApi';
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
        response = await getExtendedFortune(requestData);
      } else {
        response = await getExtendedFortunePhase2(requestData);
      }

      if (response.success && response.data) {
        setFortuneData(response.data);
      } else {
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
    if (!fortuneData) return null;

    const renderFortuneSection = (sectionTitle: string, content: any) => {
      if (typeof content === 'string') {
        return (
          <View style={styles.sectionContainer}>
            <Text style={styles.sectionTitle}>{sectionTitle}</Text>
            <Text style={styles.sectionContent}>{content}</Text>
          </View>
        );
      }

      if (typeof content === 'object' && content !== null) {
        return (
          <View style={styles.sectionContainer}>
            <Text style={styles.sectionTitle}>{sectionTitle}</Text>
            {Object.entries(content).map(([key, value]) => (
              <View key={key} style={styles.subSection}>
                <Text style={styles.subSectionTitle}>
                  {getSubSectionTitle(key)}
                </Text>
                <Text style={styles.subSectionContent}>
                  {Array.isArray(value) ? value.join(', ') : String(value)}
                </Text>
              </View>
            ))}
          </View>
        );
      }

      return null;
    };

    // Phase 1 확장운세
    if (phase === 1) {
      const data = fortuneData as ExtendedFortunePhase1;
      switch (fortuneType) {
        case 'love':
          return renderFortuneSection('💕 연애운', data.love_fortune);
        case 'personality':
          return renderFortuneSection('🎭 성격운', data.personality_fortune);
        case 'relationship':
          return renderFortuneSection('👥 인간관계운', data.relationship_fortune);
        case 'wealth':
          return renderFortuneSection('💰 재물운', data.wealth_fortune);
      }
    }

    // Phase 2 확장운세
    if (phase === 2) {
      const data = fortuneData as ExtendedFortunePhase2;
      switch (fortuneType) {
        case 'career':
          return renderFortuneSection('💼 직업운', data.career_fortune);
        case 'health':
          return renderFortuneSection('💊 건강운', data.health_fortune);
        case 'study':
          return renderFortuneSection('📚 학업운', data.study_fortune);
        case 'family':
          return renderFortuneSection('👨‍👩‍👧‍👦 가족운', data.family_fortune);
      }
    }

    return null;
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