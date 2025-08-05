import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import type { NativeStackScreenProps } from "@react-navigation/native-stack";
import type { RootStackParamList } from "../navigation/types";
import { healthCheck, testSajuApi, analyzeSaju } from "../services/sajuApi";
import type { SajuBirthInfo } from "../types/saju";

type Props = NativeStackScreenProps<RootStackParamList, "ApiTest">;

const ApiTestScreen: React.FC<Props> = ({ navigation }) => {
  const [testResults, setTestResults] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addResult = (message: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const clearResults = () => {
    setTestResults([]);
  };

  const testNetworkConnection = async () => {
    setIsLoading(true);
    addResult("🌐 네트워크 연결 테스트...");
    
    try {
      // 간단한 네트워크 테스트를 위해 fetch로 HEAD 요청
      const controller = new AbortController();
      const timeoutId = setTimeout(() => {
        addResult("⏰ 네트워크 연결 시간 초과");
        controller.abort();
      }, 5000);
      
      const response = await fetch('http://192.168.219.141:8000/health', {
        method: 'GET',
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        addResult("✅ 네트워크 연결 성공!");
        addResult(`📡 응답 시간: ${Date.now() - Date.now()}ms`);
      } else {
        addResult(`❌ 네트워크 응답 오류: ${response.status}`);
      }
    } catch (error) {
      addResult(`💥 네트워크 연결 실패: ${error}`);
    }
    
    setIsLoading(false);
  };

  const testHealthCheck = async () => {
    setIsLoading(true);
    addResult("🔍 헬스 체크 시작...");
    
    try {
      const result = await healthCheck();
      if (result.success) {
        addResult("✅ 헬스 체크 성공!");
        addResult(`📊 응답: ${JSON.stringify(result.data, null, 2)}`);
      } else {
        addResult(`❌ 헬스 체크 실패: ${result.error}`);
      }
    } catch (error) {
      addResult(`💥 헬스 체크 오류: ${error}`);
    }
    
    setIsLoading(false);
  };

  const testApiEndpoint = async () => {
    setIsLoading(true);
    addResult("🔍 API 테스트 엔드포인트 호출...");
    
    try {
      const result = await testSajuApi();
      if (result.success) {
        addResult("✅ API 테스트 성공!");
        addResult(`📊 응답: ${JSON.stringify(result.data, null, 2)}`);
      } else {
        addResult(`❌ API 테스트 실패: ${result.error}`);
      }
    } catch (error) {
      addResult(`💥 API 테스트 오류: ${error}`);
    }
    
    setIsLoading(false);
  };

  const testSajuAnalysis = async () => {
    setIsLoading(true);
    addResult("🔍 사주 분석 API 테스트...");
    
    // 테스트용 더미 데이터 - 실제 API 요청과 동일한 형식
    const testData: SajuBirthInfo = {
      year: 1993,
      month: 5,
      day: 27,
      hour: 15,
      gender: 'male',
      name: '김영래'
    };
    
    addResult(`📋 요청 데이터: ${JSON.stringify(testData, null, 2)}`);
    
    try {
      const result = await analyzeSaju(testData);
      if (result.success) {
        addResult("✅ 사주 분석 성공!");
        addResult(`📊 기본 정보: ${JSON.stringify({
          name: result.data?.basic_info?.name,
          birth_date: result.data?.basic_info?.birth_date,
          palja_count: Object.keys(result.data?.saju_palja || {}).length
        }, null, 2)}`);
      } else {
        addResult(`❌ 사주 분석 실패: ${result.error}`);
      }
    } catch (error) {
      addResult(`💥 사주 분석 오류: ${error}`);
    }
    
    setIsLoading(false);
  };

  const runAllTests = async () => {
    clearResults();
    addResult("🚀 전체 API 테스트 시작!");
    
    await testHealthCheck();
    await new Promise(resolve => setTimeout(resolve, 1000)); // 1초 대기
    
    await testApiEndpoint();
    await new Promise(resolve => setTimeout(resolve, 1000)); // 1초 대기
    
    await testSajuAnalysis();
    
    addResult("🎉 전체 API 테스트 완료!");
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>← 돌아가기</Text>
        </TouchableOpacity>
        <Text style={styles.title}>API 연결 테스트</Text>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.testButton, styles.networkButton]}
            onPress={testNetworkConnection}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>🌐 네트워크 연결</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.testButton, styles.healthButton]}
            onPress={testHealthCheck}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>🏥 헬스 체크</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.testButton, styles.apiButton]}
            onPress={testApiEndpoint}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>🔧 API 테스트</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.testButton, styles.sajuButton]}
            onPress={testSajuAnalysis}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>🔮 사주 분석</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.testButton, styles.allButton]}
            onPress={runAllTests}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>🚀 전체 테스트</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.testButton, styles.clearButton]}
            onPress={clearResults}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>🗑️ 결과 지우기</Text>
          </TouchableOpacity>
        </View>

        {isLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#BE5985" />
            <Text style={styles.loadingText}>API 호출 중...</Text>
          </View>
        )}

        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>📋 테스트 결과</Text>
          {testResults.length === 0 ? (
            <Text style={styles.noResultsText}>아직 테스트 결과가 없습니다.</Text>
          ) : (
            testResults.map((result, index) => (
              <View key={index} style={styles.resultItem}>
                <Text style={styles.resultText}>{result}</Text>
              </View>
            ))
          )}
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
    marginRight: 80,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  buttonContainer: {
    marginBottom: 20,
  },
  testButton: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 15,
    marginBottom: 10,
    alignItems: "center",
  },
  networkButton: {
    backgroundColor: "#9C27B0",
  },
  healthButton: {
    backgroundColor: "#4CAF50",
  },
  apiButton: {
    backgroundColor: "#2196F3",
  },
  sajuButton: {
    backgroundColor: "#BE5985",
  },
  allButton: {
    backgroundColor: "#FF9800",
  },
  clearButton: {
    backgroundColor: "#757575",
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
  },
  loadingContainer: {
    alignItems: "center",
    padding: 20,
  },
  loadingText: {
    color: "#BE5985",
    fontSize: 16,
    marginTop: 10,
    fontWeight: "500",
  },
  resultsContainer: {
    backgroundColor: "white",
    borderRadius: 15,
    padding: 15,
    marginTop: 10,
  },
  resultsTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#BE5985",
    marginBottom: 15,
  },
  noResultsText: {
    color: "#BE5985",
    fontSize: 14,
    fontStyle: "italic",
    textAlign: "center",
    opacity: 0.7,
  },
  resultItem: {
    backgroundColor: "#FFB8E0",
    padding: 10,
    borderRadius: 8,
    marginBottom: 8,
  },
  resultText: {
    color: "#BE5985",
    fontSize: 12,
    fontFamily: "monospace",
  },
});

export default ApiTestScreen;