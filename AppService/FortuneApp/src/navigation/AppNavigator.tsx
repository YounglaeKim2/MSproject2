import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/HomeScreen";
import ProfileScreen from "../screens/ProfileScreen";
import SettingsScreen from "../screens/SettingsScreen";
import ChatGPTScreen from "../screens/ChatGPTScreen";
import ApiTestScreen from "../screens/ApiTestScreen";
import FortuneDetailScreen from "../screens/FortuneDetailScreen";
import type { RootStackParamList } from "./types";

const Stack = createNativeStackNavigator<RootStackParamList>();

const AppNavigator: React.FC = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: "#BE5985",
          },
          headerTintColor: "#FFEDFA",
          headerTitleStyle: {
            fontWeight: "600",
            fontSize: 18,
          },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: "오행 분석" }}
        />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={{ title: "오행 분석" }}
        />
        <Stack.Screen
          name="Settings"
          component={SettingsScreen}
          options={{ title: "기운 보완법" }}
        />
        <Stack.Screen
          name="ChatGPT"
          component={ChatGPTScreen}
          options={{ title: "AI 운세박사" }}
        />
        <Stack.Screen
          name="ApiTest"
          component={ApiTestScreen}
          options={{ title: "API 연결 테스트" }}
        />
        <Stack.Screen
          name="FortuneDetail"
          component={FortuneDetailScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
