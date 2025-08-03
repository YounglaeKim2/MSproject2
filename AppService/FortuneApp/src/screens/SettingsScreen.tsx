import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
} from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../navigation/types";

type Props = NativeStackScreenProps<RootStackParamList, "Settings">;

const SettingsScreen: React.FC<Props> = ({ navigation }) => {
  const elementRemedies = [
    {
      element: "화(火)",
      status: "부족",
      color: "#EC7FA9",
      remedies: [
        "빨간색, 주황색 계열 의상 착용",
        "남쪽 방향에서 활동하기",
        "태양광 충전하기 (일광욕)",
        "매운 음식 섭취",
        "촛불이나 난로 근처에서 시간 보내기",
      ],
    },
    {
      element: "목(木)",
      status: "약함",
      color: "#FFB8E0",
      remedies: [
        "초록색 계열 의상 착용",
        "동쪽 방향에서 활동하기",
        "나무 소재 액세서리 착용",
        "식물 키우기, 산책하기",
        "새싹 채소, 녹색 채소 섭취",
      ],
    },
    {
      element: "토(土)",
      status: "매우 강함",
      color: "#BE5985",
      remedies: [
        "노란색, 갈색 계열 의상 피하기",
        "중앙 방향에서의 활동 자제",
        "흙, 도자기 소재 액세서리 피하기",
        "달콤한 음식 섭취 줄이기",
        "과도한 안정감 추구 자제",
      ],
    },
    {
      element: "금(金)",
      status: "보통",
      color: "#EC7FA9",
      remedies: [
        "흰색, 은색 계열 의상 적당히 착용",
        "서쪽 방향에서 활동하기",
        "금속 소재 액세서리 착용",
        "매콤하고 자극적인 음식 적당히 섭취",
        "규칙적인 운동으로 균형 유지",
      ],
    },
    {
      element: "수(水)",
      status: "강함",
      color: "#FFB8E0",
      remedies: [
        "검은색, 파란색 계열 의상 줄이기",
        "북쪽 방향에서의 활동 자제",
        "물 근처에서의 활동 적당히 하기",
        "짠 음식 섭취 줄이기",
        "과도한 유연성 추구 자제",
      ],
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>기운 보완법</Text>
          <Text style={styles.subtitle}>
            부족한 기운을 보완하고 강한 기운을 조절해보세요
          </Text>
        </View>

        <View style={styles.summaryBox}>
          <Text style={styles.summaryTitle}>당신의 오행 상태</Text>
          <Text style={styles.summaryText}>
            • 부족: 화(火), 목(木) - 적극적인 보완 필요{"\n"}• 강함: 토(土),
            수(水) - 적절한 조절 필요{"\n"}• 보통: 금(金) - 현재 상태 유지
          </Text>
        </View>

        {elementRemedies.map((item, index) => (
          <View
            key={index}
            style={[styles.remedyCard, { borderLeftColor: item.color }]}
          >
            <View style={styles.remedyHeader}>
              <Text style={styles.elementTitle}>{item.element}</Text>
              <Text
                style={[styles.statusBadge, { backgroundColor: item.color }]}
              >
                {item.status}
              </Text>
            </View>

            <View style={styles.remedyList}>
              {item.remedies.map((remedy, remedyIndex) => (
                <View key={remedyIndex} style={styles.remedyItem}>
                  <Text style={styles.bulletPoint}>•</Text>
                  <Text style={styles.remedyText}>{remedy}</Text>
                </View>
              ))}
            </View>
          </View>
        ))}

        <View style={styles.tipBox}>
          <Text style={styles.tipTitle}>💡 실천 팁</Text>
          <Text style={styles.tipText}>
            • 하루에 2-3가지 보완법을 실천해보세요{"\n"}• 강한 기운의 조절도
            중요합니다{"\n"}• 꾸준한 실천이 가장 중요합니다{"\n"}• 개인차가
            있으니 자신에게 맞는 방법을 찾아보세요
          </Text>
        </View>

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
  header: {
    alignItems: "center",
    marginBottom: 20,
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
    lineHeight: 24,
    opacity: 0.8,
  },
  summaryBox: {
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
  summaryTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 10,
    textAlign: "center",
  },
  summaryText: {
    fontSize: 14,
    color: "#BE5985",
    lineHeight: 20,
    opacity: 0.8,
  },
  remedyCard: {
    backgroundColor: "white",
    padding: 20,
    borderRadius: 20,
    marginBottom: 15,
    borderLeftWidth: 5,
    shadowColor: "#BE5985",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  remedyHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 15,
  },
  elementTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#BE5985",
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    fontSize: 12,
    fontWeight: "600",
    color: "white",
    textAlign: "center",
  },
  remedyList: {
    marginTop: 10,
  },
  remedyItem: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 8,
  },
  bulletPoint: {
    color: "#BE5985",
    fontSize: 16,
    marginRight: 8,
    marginTop: 2,
  },
  remedyText: {
    flex: 1,
    fontSize: 14,
    color: "#BE5985",
    lineHeight: 20,
    opacity: 0.8,
  },
  tipBox: {
    backgroundColor: "#FFB8E0",
    padding: 20,
    borderRadius: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: "#BE5985",
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 10,
    textAlign: "center",
  },
  tipText: {
    fontSize: 14,
    color: "#BE5985",
    lineHeight: 20,
    opacity: 0.8,
  },
  button: {
    backgroundColor: "#BE5985",
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
    alignItems: "center",
    marginTop: 10,
    shadowColor: "#BE5985",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
  },
});

export default SettingsScreen;
