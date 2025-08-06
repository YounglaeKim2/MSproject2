import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  TextInput,
  Alert,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../navigation/types";
import { analyzeSaju } from "../services/sajuApi";
import { convertToSajuRequest, validateInput, strengthToPercentage, getElementColor, transformApiResponse } from "../utils/dataMapper";
import type { SajuAnalysisResult } from "../types/saju";

type Props = NativeStackScreenProps<RootStackParamList, "Profile">;

const ProfileScreen: React.FC<Props> = ({ navigation }) => {
  const [birthDate, setBirthDate] = useState("");
  const [birthTime, setBirthTime] = useState("");
  const [calendarType, setCalendarType] = useState<"양력" | "음력">("양력");
  const [gender, setGender] = useState<"남자" | "여자">("남자");
  const [name, setName] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<SajuAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyzeBirthDate = async () => {
    // 입력값 검증
    const errors = validateInput(birthDate, birthTime, gender);
    if (errors.length > 0) {
      Alert.alert("입력 오류", errors.join("\n"));
      return;
    }

    // API 요청 데이터 변환
    const requestData = convertToSajuRequest(birthDate, birthTime, gender, name);
    if (!requestData) {
      Alert.alert("변환 오류", "입력된 정보를 처리할 수 없습니다. 형식을 확인해주세요.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      console.log("사주 분석 요청:", requestData);
      const response = await analyzeSaju(requestData);
      
      if (response.success && response.data) {
        console.log("사주 분석 성공:", response.data);
        // API 응답을 모바일 앱 형식으로 변환
        const transformedData = transformApiResponse(response.data);
        setAnalysisResult(transformedData);
        setShowResult(true);
      } else {
        throw new Error(response.error || "사주 분석에 실패했습니다.");
      }
    } catch (error) {
      console.error("사주 분석 오류:", error);
      const errorMessage = error instanceof Error ? error.message : "알 수 없는 오류가 발생했습니다.";
      setError(errorMessage);
      Alert.alert("분석 실패", errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // 실제 API 결과 렌더링 함수
  const renderWuxingElement = (element: string, value: number, strength: string) => {
    const percentage = strengthToPercentage(strength);
    const color = getElementColor(element);
    
    return (
      <View key={element} style={styles.elementItem}>
        <Text style={styles.elementLabel}>{element}</Text>
        <View style={styles.strengthBar}>
          <View 
            style={[
              styles.strengthFill, 
              { 
                width: `${percentage}%`,
                backgroundColor: color,
              }
            ]} 
          />
        </View>
        <Text style={styles.strengthText}>{strength}</Text>
      </View>
    );
  };

  if (showResult && analysisResult) {
    const { wuxing, basic_analysis, palja } = analysisResult;
    
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView contentContainerStyle={styles.scrollContent}>
          <Text style={styles.title}>사주 분석 결과</Text>
          <Text style={styles.subtitle}>AI 기반 만세력 분석</Text>

          <View style={styles.resultContainer}>
            <Text style={styles.birthInfo}>
              {calendarType} {birthDate} {birthTime}시{"\n"}
              {gender} {name && `• ${name}`}
            </Text>

            {/* 사주팔자 표시 */}
            {palja && (
              <View style={styles.paljaContainer}>
                <Text style={styles.paljaTitle}>사주팔자</Text>
                <View style={styles.paljaGrid}>
                  <View style={styles.paljaColumn}>
                    <Text style={styles.paljaLabel}>년주</Text>
                    <Text style={styles.paljaValue}>{palja.year_heavenly}</Text>
                    <Text style={styles.paljaValue}>{palja.year_earthly}</Text>
                  </View>
                  <View style={styles.paljaColumn}>
                    <Text style={styles.paljaLabel}>월주</Text>
                    <Text style={styles.paljaValue}>{palja.month_heavenly}</Text>
                    <Text style={styles.paljaValue}>{palja.month_earthly}</Text>
                  </View>
                  <View style={styles.paljaColumn}>
                    <Text style={styles.paljaLabel}>일주</Text>
                    <Text style={styles.paljaValue}>{palja.day_heavenly}</Text>
                    <Text style={styles.paljaValue}>{palja.day_earthly}</Text>
                  </View>
                  <View style={styles.paljaColumn}>
                    <Text style={styles.paljaLabel}>시주</Text>
                    <Text style={styles.paljaValue}>{palja.hour_heavenly}</Text>
                    <Text style={styles.paljaValue}>{palja.hour_earthly}</Text>
                  </View>
                </View>
              </View>
            )}

            {/* 오행 분석 */}
            {wuxing && (
              <View style={styles.elementContainer}>
                <Text style={styles.elementTitle}>오행 기운 분석</Text>
                {renderWuxingElement("목(木)", wuxing.wood, wuxing.wood_strength)}
                {renderWuxingElement("화(火)", wuxing.fire, wuxing.fire_strength)}
                {renderWuxingElement("토(土)", wuxing.earth, wuxing.earth_strength)}
                {renderWuxingElement("금(金)", wuxing.metal, wuxing.metal_strength)}
                {renderWuxingElement("수(水)", wuxing.water, wuxing.water_strength)}
                
                <View style={styles.wuxingSummary}>
                  <Text style={styles.wuxingSummaryText}>
                    💪 가장 강한 기운: {wuxing.strongest_element}{"\n"}
                    🔋 가장 약한 기운: {wuxing.weakest_element}
                  </Text>
                </View>
              </View>
            )}

            {/* 기본 분석 결과 */}
            {basic_analysis && (
              <View style={styles.analysisBox}>
                <Text style={styles.analysisTitle}>종합 분석</Text>
                <Text style={styles.analysisText}>
                  🎭 성격: {basic_analysis.personality}{"\n\n"}
                  💊 건강: {basic_analysis.health}{"\n\n"}
                  💰 재물운: {basic_analysis.wealth}{"\n\n"}
                  👥 인간관계: {basic_analysis.relationships}
                </Text>
                
                {/* 강점과 약점 */}
                {basic_analysis.strengths && basic_analysis.strengths.length > 0 && (
                  <View style={styles.strengthsWeaknesses}>
                    <Text style={styles.strengthsTitle}>💪 강점</Text>
                    {basic_analysis.strengths.map((strength, index) => (
                      <Text key={index} style={styles.strengthItem}>• {strength}</Text>
                    ))}
                  </View>
                )}
                
                {basic_analysis.weaknesses && basic_analysis.weaknesses.length > 0 && (
                  <View style={styles.strengthsWeaknesses}>
                    <Text style={styles.weaknessesTitle}>🔋 개선점</Text>
                    {basic_analysis.weaknesses.map((weakness, index) => (
                      <Text key={index} style={styles.weaknessItem}>• {weakness}</Text>
                    ))}
                  </View>
                )}
              </View>
            )}
          </View>

          <TouchableOpacity
            style={styles.button}
            onPress={() => {
              setShowResult(false);
              setAnalysisResult(null);
              setError(null);
            }}
          >
            <Text style={styles.buttonText}>다시 분석하기</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.backButton]}
            onPress={() => {
              // HomeScreen으로 생년월일 정보와 함께 돌아가기
              navigation.navigate('Home', {
                birthInfo: {
                  birthDate,
                  birthTime,
                  gender,
                  name
                }
              });
            }}
          >
            <Text style={styles.buttonText}>확장운세 보러가기</Text>
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>오행 분석</Text>
        <Text style={styles.subtitle}>
          정확한 사주 분석을 위해 아래 정보를 입력해주세요
        </Text>

        {/* 양력/음력 선택 */}
        <View style={styles.sectionContainer}>
          <Text style={styles.sectionTitle}>달력 구분</Text>
          <View style={styles.toggleContainer}>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                calendarType === "양력" && styles.toggleButtonActive,
              ]}
              onPress={() => setCalendarType("양력")}
            >
              <Text
                style={[
                  styles.toggleText,
                  calendarType === "양력" && styles.toggleTextActive,
                ]}
              >
                양력
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                calendarType === "음력" && styles.toggleButtonActive,
              ]}
              onPress={() => setCalendarType("음력")}
            >
              <Text
                style={[
                  styles.toggleText,
                  calendarType === "음력" && styles.toggleTextActive,
                ]}
              >
                음력
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* 성별 선택 */}
        <View style={styles.sectionContainer}>
          <Text style={styles.sectionTitle}>성별</Text>
          <View style={styles.toggleContainer}>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                gender === "남자" && styles.toggleButtonActive,
              ]}
              onPress={() => setGender("남자")}
            >
              <Text
                style={[
                  styles.toggleText,
                  gender === "남자" && styles.toggleTextActive,
                ]}
              >
                남자
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.toggleButton,
                gender === "여자" && styles.toggleButtonActive,
              ]}
              onPress={() => setGender("여자")}
            >
              <Text
                style={[
                  styles.toggleText,
                  gender === "여자" && styles.toggleTextActive,
                ]}
              >
                여자
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* 생년월일 입력 */}
        <View style={styles.inputContainer}>
          <Text style={styles.inputLabel}>생년월일</Text>
          <TextInput
            style={styles.input}
            placeholder="예: 1990-01-01"
            placeholderTextColor="#BE5985"
            value={birthDate}
            onChangeText={setBirthDate}
            keyboardType="numeric"
          />
        </View>

        {/* 태어난 시간 입력 */}
        <View style={styles.inputContainer}>
          <Text style={styles.inputLabel}>태어난 시간</Text>
          <TextInput
            style={styles.input}
            placeholder="예: 14 (24시간 형식, 모를 경우 12 입력)"
            placeholderTextColor="#BE5985"
            value={birthTime}
            onChangeText={setBirthTime}
            keyboardType="numeric"
          />
          <Text style={styles.helpText}>
            정확한 시간을 모르면 12시(오정시)로 입력하세요
          </Text>
        </View>

        {/* 이름 입력 (선택사항) */}
        <View style={styles.inputContainer}>
          <Text style={styles.inputLabel}>이름 (선택사항)</Text>
          <TextInput
            style={styles.input}
            placeholder="예: 홍길동"
            placeholderTextColor="#BE5985"
            value={name}
            onChangeText={setName}
          />
          <Text style={styles.helpText}>
            이름을 입력하시면 더 개인화된 분석 결과를 받을 수 있습니다
          </Text>
        </View>

        {/* 로딩 상태 표시 */}
        {isLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#BE5985" />
            <Text style={styles.loadingText}>사주를 분석 중입니다...</Text>
            <Text style={styles.loadingSubText}>잠시만 기다려주세요</Text>
          </View>
        ) : (
          <TouchableOpacity
            style={styles.analyzeButton}
            onPress={analyzeBirthDate}
          >
            <Text style={styles.buttonText}>🔮 사주 분석하기</Text>
          </TouchableOpacity>
        )}

        {/* 에러 메시지 표시 */}
        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>⚠️ {error}</Text>
            <TouchableOpacity
              style={styles.retryButton}
              onPress={() => setError(null)}
            >
              <Text style={styles.retryButtonText}>다시 시도</Text>
            </TouchableOpacity>
          </View>
        )}

        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.buttonText}>돌아가기</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFEDFA",
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  sectionContainer: {
    width: "100%",
    marginBottom: 25,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 12,
  },
  toggleContainer: {
    flexDirection: "row",
    borderRadius: 25,
    backgroundColor: "#FFB8E0",
    padding: 4,
  },
  toggleButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 20,
    alignItems: "center",
  },
  toggleButtonActive: {
    backgroundColor: "#BE5985",
  },
  toggleText: {
    fontSize: 16,
    color: "#BE5985",
    fontWeight: "500",
  },
  toggleTextActive: {
    color: "white",
    fontWeight: "600",
  },
  helpText: {
    fontSize: 12,
    color: "#BE5985",
    marginTop: 5,
    fontStyle: "italic",
    opacity: 0.7,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#BE5985",
    marginBottom: 10,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 16,
    color: "#BE5985",
    textAlign: "center",
    marginBottom: 30,
    lineHeight: 24,
    opacity: 0.8,
  },
  inputContainer: {
    width: "100%",
    marginBottom: 20,
  },
  inputLabel: {
    fontSize: 16,
    color: "#BE5985",
    marginBottom: 8,
    fontWeight: "500",
  },
  input: {
    backgroundColor: "white",
    color: "#BE5985",
    padding: 15,
    borderRadius: 15,
    fontSize: 16,
    borderWidth: 2,
    borderColor: "#FFB8E0",
  },
  analyzeButton: {
    backgroundColor: "#BE5985",
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
    marginBottom: 20,
    shadowColor: "#BE5985",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  button: {
    backgroundColor: "#FFB8E0",
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 20,
    marginBottom: 10,
  },
  backButton: {
    backgroundColor: "#EC7FA9",
  },
  buttonText: {
    color: "#BE5985",
    fontSize: 16,
    fontWeight: "600",
    textAlign: "center",
  },
  resultContainer: {
    width: "100%",
    backgroundColor: "white",
    padding: 20,
    borderRadius: 20,
    marginBottom: 20,
    shadowColor: "#BE5985",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
  },
  birthInfo: {
    fontSize: 16,
    color: "#BE5985",
    textAlign: "center",
    marginBottom: 20,
    fontWeight: "500",
  },
  elementContainer: {
    marginBottom: 20,
  },
  elementTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 15,
    textAlign: "center",
  },
  elementItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12,
  },
  elementLabel: {
    fontSize: 16,
    color: "#BE5985",
    width: 80,
    fontWeight: "500",
  },
  strengthBar: {
    flex: 1,
    height: 20,
    backgroundColor: "#FFB8E0",
    borderRadius: 10,
    marginHorizontal: 10,
    overflow: "hidden",
  },
  strengthFill: {
    height: "100%",
    backgroundColor: "#BE5985",
    borderRadius: 10,
  },
  strengthText: {
    fontSize: 12,
    color: "#BE5985",
    width: 60,
    textAlign: "center",
    fontWeight: "500",
  },
  analysisBox: {
    backgroundColor: "#FFB8E0",
    padding: 15,
    borderRadius: 15,
  },
  analysisTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 10,
  },
  analysisText: {
    fontSize: 14,
    color: "#BE5985",
    lineHeight: 20,
    opacity: 0.8,
  },
  // 새로운 스타일들
  loadingContainer: {
    alignItems: "center",
    padding: 20,
    marginVertical: 10,
  },
  loadingText: {
    color: "#BE5985",
    fontSize: 16,
    fontWeight: "600",
    marginTop: 10,
  },
  loadingSubText: {
    color: "#BE5985",
    fontSize: 14,
    opacity: 0.7,
    marginTop: 5,
  },
  errorContainer: {
    backgroundColor: "#FFE6E6",
    padding: 15,
    borderRadius: 10,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: "#FFB3B3",
  },
  errorText: {
    color: "#D32F2F",
    fontSize: 14,
    fontWeight: "500",
    textAlign: "center",
    marginBottom: 10,
  },
  retryButton: {
    backgroundColor: "#D32F2F",
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    alignSelf: "center",
  },
  retryButtonText: {
    color: "white",
    fontSize: 12,
    fontWeight: "600",
  },
  // 사주팔자 관련 스타일
  paljaContainer: {
    marginBottom: 20,
    backgroundColor: "#F8F4FF",
    padding: 15,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: "#E0D4FF",
  },
  paljaTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#BE5985",
    textAlign: "center",
    marginBottom: 15,
  },
  paljaGrid: {
    flexDirection: "row",
    justifyContent: "space-around",
  },
  paljaColumn: {
    alignItems: "center",
    flex: 1,
  },
  paljaLabel: {
    fontSize: 12,
    color: "#BE5985",
    fontWeight: "600",
    marginBottom: 8,
  },
  paljaValue: {
    fontSize: 14,
    color: "#BE5985",
    fontWeight: "700",
    backgroundColor: "white",
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 8,
    marginVertical: 2,
    minWidth: 32,
    textAlign: "center",
  },
  // 오행 요약
  wuxingSummary: {
    backgroundColor: "#FFF3E0",
    padding: 12,
    borderRadius: 10,
    marginTop: 15,
  },
  wuxingSummaryText: {
    fontSize: 13,
    color: "#BE5985",
    fontWeight: "500",
    textAlign: "center",
    lineHeight: 18,
  },
  // 강점/약점 스타일
  strengthsWeaknesses: {
    marginTop: 15,
  },
  strengthsTitle: {
    fontSize: 14,
    fontWeight: "600",
    color: "#4CAF50",
    marginBottom: 8,
  },
  weaknessesTitle: {
    fontSize: 14,
    fontWeight: "600",
    color: "#FF9800",
    marginBottom: 8,
  },
  strengthItem: {
    fontSize: 13,
    color: "#4CAF50",
    marginBottom: 4,
    lineHeight: 18,
  },
  weaknessItem: {
    fontSize: 13,
    color: "#FF9800",
    marginBottom: 4,
    lineHeight: 18,
  },
});

export default ProfileScreen;
