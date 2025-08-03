import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../navigation/types";

type Props = NativeStackScreenProps<RootStackParamList, "Settings">;

const SettingsScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>🔄 기운 보완법</Text>
        <Text style={styles.subtitle}>
          부족한 기운을 보완하고 강한 기운을 조절해보세요
        </Text>

        <View style={styles.summaryBox}>
          <Text style={styles.summaryTitle}>📊 당신의 오행 상태</Text>
          <Text style={styles.summaryText}>
            • 부족: 화(火), 목(木) - 적극적인 보완 필요{"\n"}• 강함: 토(土),
            수(水) - 적절한 조절 필요{"\n"}• 보통: 금(金) - 현재 상태 유지
          </Text>
        </View>

        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.buttonText}>돌아가기</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#1a1a2e",
  },
  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#50c878",
    marginBottom: 10,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 16,
    color: "#e0e0e0",
    textAlign: "center",
    marginBottom: 30,
    lineHeight: 24,
  },
  summaryBox: {
    backgroundColor: "#16213e",
    padding: 20,
    borderRadius: 15,
    marginBottom: 20,
    width: "100%",
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#ffd700",
    marginBottom: 10,
    textAlign: "center",
  },
  summaryText: {
    fontSize: 14,
    color: "#e0e0e0",
    lineHeight: 20,
  },
  button: {
    backgroundColor: "#50c878",
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
  },
});

export default SettingsScreen;
