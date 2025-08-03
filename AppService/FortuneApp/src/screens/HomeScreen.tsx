import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
} from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../navigation/types";
import FortuneCard from "../components/FortuneCard";

type Props = NativeStackScreenProps<RootStackParamList, "Home">;

const HomeScreen: React.FC<Props> = ({ navigation }) => {
  // 사주 정보 저장 (ProfileScreen에서 분석 후 저장됨)
  const [birthInfo, setBirthInfo] = useState<{
    birthDate: string;
    birthTime: string;
    gender: string;
    name?: string;
  } | null>(null);

  // 확장운세 데이터 정의
  const fortuneCards = [
    // Phase 1 확장운세
    {
      id: 'love',
      title: '연애운',
      description: '사랑과 인연의 흐름을\n자세히 살펴보세요',
      icon: '💕',
      color: '#E91E63',
      phase: 1 as const,
    },
    {
      id: 'personality',
      title: '성격운',
      description: '숨겨진 성격과 잠재력을\n깊이 분석합니다',
      icon: '🎭',
      color: '#9C27B0',
      phase: 1 as const,
    },
    {
      id: 'relationship',
      title: '인간관계운',
      description: '사람들과의 관계에서\n성공하는 비법',
      icon: '👥',
      color: '#673AB7',
      phase: 1 as const,
    },
    {
      id: 'wealth',
      title: '재물운',
      description: '돈과 재물의 흐름을\n파악해보세요',
      icon: '💰',
      color: '#3F51B5',
      phase: 1 as const,
    },
    // Phase 2 확장운세
    {
      id: 'career',
      title: '직업운',
      description: '현재 직업 적성과\n이직 타이밍 분석',
      icon: '💼',
      color: '#2196F3',
      phase: 2 as const,
    },
    {
      id: 'health',
      title: '건강운',
      description: '체력 관리와 질병 예방\n맞춤 건강 가이드',
      icon: '💊',
      color: '#00BCD4',
      phase: 2 as const,
    },
    {
      id: 'study',
      title: '학업운',
      description: '시험운과 자기계발\n새로운 기술 학습',
      icon: '📚',
      color: '#009688',
      phase: 2 as const,
    },
    {
      id: 'family',
      title: '가족운',
      description: '부모, 형제자매와의\n화합과 소통',
      icon: '👨‍👩‍👧‍👦',
      color: '#4CAF50',
      phase: 2 as const,
    },
  ];

  // 확장운세 카드 클릭 핸들러
  const handleFortuneCardPress = (fortuneCard: typeof fortuneCards[0]) => {
    if (!birthInfo) {
      Alert.alert(
        '사주 분석 필요',
        '확장운세를 보려면 먼저 기본 사주 분석을 해주세요.',
        [
          { text: '취소', style: 'cancel' },
          { 
            text: '사주 분석하기', 
            onPress: () => navigation.navigate('Profile')
          }
        ]
      );
      return;
    }

    navigation.navigate('FortuneDetail', {
      fortuneType: fortuneCard.id,
      title: fortuneCard.title,
      icon: fortuneCard.icon,
      color: fortuneCard.color,
      phase: fortuneCard.phase,
      birthInfo,
    });
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false}>
        <View style={styles.content}>
          <Text style={styles.title}>사주 운세 분석</Text>
          <Text style={styles.subtitle}>
            생년월일로 당신의 운세를 분석해보세요{"\n"}8가지 확장 운세로 더 자세한 미래를 확인하세요
          </Text>

          {/* 기본 분석 섹션 */}
          <View style={styles.basicSection}>
            <Text style={styles.sectionTitle}>🔮 기본 사주 분석</Text>
            <View style={styles.basicCardContainer}>
              <TouchableOpacity
                style={[styles.basicCard, styles.sajuCard]}
                onPress={() => navigation.navigate("Profile")}
              >
                <Text style={styles.cardTitle}>사주팔자 분석</Text>
                <Text style={styles.cardDescription}>
                  생년월일로 당신의{"\n"}사주팔자와 오행을 분석
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.basicCard, styles.mbtiCard]}
                onPress={() => navigation.navigate("Settings")}
              >
                <Text style={styles.cardTitle}>기운 보완법</Text>
                <Text style={styles.cardDescription}>
                  부족한 기운을 보완하는{"\n"}실용적인 방법 제시
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* 확장 운세 섹션 */}
          <View style={styles.extendedSection}>
            <Text style={styles.sectionTitle}>✨ 확장 운세 (Phase 1 + 2)</Text>
            <Text style={styles.sectionSubtitle}>
              더 자세하고 전문적인 운세 분석을 받아보세요
            </Text>
            
            <View style={styles.fortuneCardsContainer}>
              {fortuneCards.map((fortuneCard) => (
                <FortuneCard
                  key={fortuneCard.id}
                  title={fortuneCard.title}
                  description={fortuneCard.description}
                  icon={fortuneCard.icon}
                  color={fortuneCard.color}
                  phase={fortuneCard.phase}
                  onPress={() => handleFortuneCardPress(fortuneCard)}
                />
              ))}
            </View>
          </View>

          {/* AI 및 기타 도구 섹션 */}
          <View style={styles.toolsSection}>
            <Text style={styles.sectionTitle}>🤖 AI 도구</Text>
            
            <TouchableOpacity
              style={[styles.card, styles.aiCard]}
              onPress={() => navigation.navigate("ChatGPT")}
            >
              <Text style={styles.cardTitle}>AI 운세박사</Text>
              <Text style={styles.cardDescription}>
                전문 AI가 당신의{"\n"}운세를 상세히 분석해드립니다
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.card, styles.testCard]}
              onPress={() => navigation.navigate("ApiTest")}
            >
              <Text style={styles.cardTitle}>🔧 API 테스트</Text>
              <Text style={styles.cardDescription}>
                SAJU 백엔드 서버와의{"\n"}연결 상태를 확인합니다
              </Text>
            </TouchableOpacity>
          </View>

          <View style={styles.bottomSection}>
            <Text style={styles.todayFortune}>오늘의 운세</Text>
            <Text style={styles.fortuneText}>
              "변화의 기운이 감지됩니다. 새로운 시작에 적합한 날이니 용기를 내어 첫 걸음을 내딛어보세요. 특히 {birthInfo ? '확장운세를 통해 더 자세한' : '사주 분석 후'} 운세를 확인해보시기 바랍니다."
            </Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFEDFA",
  },
  scrollContainer: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#BE5985",
    marginBottom: 8,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 14,
    color: "#BE5985",
    textAlign: "center",
    marginBottom: 30,
    lineHeight: 20,
    opacity: 0.8,
  },
  // 섹션 스타일
  basicSection: {
    marginBottom: 25,
  },
  extendedSection: {
    marginBottom: 25,
  },
  toolsSection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#BE5985",
    marginBottom: 12,
    textAlign: "left",
  },
  sectionSubtitle: {
    fontSize: 13,
    color: "#BE5985",
    marginBottom: 15,
    opacity: 0.7,
    textAlign: "left",
  },
  // 기본 카드 컨테이너
  basicCardContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: "100%",
  },
  basicCard: {
    width: "48%",
    padding: 20,
    borderRadius: 16,
    alignItems: "center",
    shadowColor: "#BE5985",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  // 확장운세 카드 컨테이너
  fortuneCardsContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
  },
  // 기존 카드 스타일
  card: {
    width: "100%",
    padding: 20,
    borderRadius: 16,
    alignItems: "center",
    marginBottom: 12,
    shadowColor: "#BE5985",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  sajuCard: {
    backgroundColor: "#EC7FA9",
  },
  mbtiCard: {
    backgroundColor: "#FFB8E0",
  },
  aiCard: {
    backgroundColor: "#BE5985",
  },
  testCard: {
    backgroundColor: "#6A5ACD",
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "white",
    marginBottom: 6,
    textAlign: "center",
  },
  cardDescription: {
    fontSize: 12,
    color: "rgba(255, 255, 255, 0.9)",
    textAlign: "center",
    lineHeight: 16,
  },
  bottomSection: {
    backgroundColor: "#FFB8E0",
    padding: 20,
    borderRadius: 16,
    width: "100%",
    alignItems: "center",
    marginTop: 10,
  },
  todayFortune: {
    fontSize: 16,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 8,
  },
  fortuneText: {
    fontSize: 13,
    color: "#BE5985",
    textAlign: "center",
    lineHeight: 18,
    opacity: 0.8,
  },
});

export default HomeScreen;
