/**
 * 확장운세 카드 컴포넌트
 * Phase 1+2 확장운세를 카드 형태로 표시
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';

export interface FortuneCardProps {
  title: string;
  description: string;
  icon: string;
  color: string;
  phase: 1 | 2;
  onPress: () => void;
}

const FortuneCard: React.FC<FortuneCardProps> = ({
  title,
  description,
  icon,
  color,
  phase,
  onPress,
}) => {
  return (
    <TouchableOpacity
      style={[styles.card, { backgroundColor: color }]}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <View style={styles.cardHeader}>
        <Text style={styles.cardIcon}>{icon}</Text>
        <View style={styles.phaseIndicator}>
          <Text style={styles.phaseText}>Phase {phase}</Text>
        </View>
      </View>
      
      <Text style={styles.cardTitle}>{title}</Text>
      <Text style={styles.cardDescription}>{description}</Text>
      
      <View style={styles.cardFooter}>
        <Text style={styles.tapText}>눌러서 자세히 보기</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    width: '48%',
    padding: 16,
    borderRadius: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
    minHeight: 140,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  cardIcon: {
    fontSize: 28,
    marginBottom: 4,
  },
  phaseIndicator: {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
  },
  phaseText: {
    fontSize: 10,
    color: 'white',
    fontWeight: '600',
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
    marginBottom: 6,
  },
  cardDescription: {
    fontSize: 12,
    color: 'rgba(255, 255, 255, 0.9)',
    lineHeight: 16,
    flex: 1,
  },
  cardFooter: {
    marginTop: 8,
    alignItems: 'center',
  },
  tapText: {
    fontSize: 10,
    color: 'rgba(255, 255, 255, 0.7)',
    fontWeight: '500',
  },
});

export default FortuneCard;