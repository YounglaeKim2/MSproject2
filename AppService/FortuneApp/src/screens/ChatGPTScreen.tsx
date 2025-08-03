import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import { WebView } from "react-native-webview";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../navigation/types";

type Props = NativeStackScreenProps<RootStackParamList, "ChatGPT">;

const ChatGPTScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>← 돌아가기</Text>
        </TouchableOpacity>
        <Text style={styles.title}>AI 운세박사</Text>
      </View>

      <WebView
        source={{
          uri: "https://chatgpt.com/g/g-mHCPUrEvZ-unsebagsa-gpt-ai-saju-segye-1wi-ai-sajupalja-sinnyeonunse-hangug-korean-myeongrihag",
        }}
        style={styles.webview}
        startInLoadingState={true}
        renderLoading={() => (
          <View style={styles.loadingContainer}>
            <Text style={styles.loadingText}>AI 운세박사 로딩 중...</Text>
          </View>
        )}
        onError={(error) => {
          console.error("WebView 오류:", error);
        }}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFEDFA",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    padding: 15,
    backgroundColor: "#BE5985",
    borderBottomWidth: 1,
    borderBottomColor: "#FFB8E0",
  },
  backButton: {
    marginRight: 15,
  },
  backButtonText: {
    color: "#FFEDFA",
    fontSize: 16,
    fontWeight: "600",
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
    color: "#FFEDFA",
    flex: 1,
    textAlign: "center",
    marginRight: 80, // 돌아가기 버튼만큼 오프셋
  },
  webview: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFEDFA",
  },
  loadingText: {
    color: "#BE5985",
    fontSize: 16,
    fontWeight: "600",
  },
});

export default ChatGPTScreen;
