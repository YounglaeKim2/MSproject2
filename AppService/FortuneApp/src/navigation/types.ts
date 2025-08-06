export type RootStackParamList = {
  Home: {
    birthInfo?: {
      birthDate: string;
      birthTime: string;
      gender: string;
      name?: string;
    };
  } | undefined;
  Profile: undefined;
  Settings: undefined;
  ChatGPT: undefined;
  ApiTest: undefined;
  FortuneDetail: {
    fortuneType: string;
    title: string;
    icon: string;
    color: string;
    phase: 1 | 2;
    birthInfo?: {
      birthDate: string;
      birthTime: string;
      gender: string;
      name?: string;
    };
  };
};
