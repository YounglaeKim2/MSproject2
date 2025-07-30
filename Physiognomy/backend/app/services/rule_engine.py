# rule_engine.py

from typing import Dict, List

def analyze_gwansang_rules(metrics: Dict[str, float]) -> List[str]:
    """
    기하학적 특징 딕셔너리를 입력받아, 정의된 규칙에 따라
    관상학적 해석 키 리스트를 반환합니다.

    Args:
        metrics (Dict[str, float]): calculate_geometric_metrics에서 계산된 특징 딕셔너리.

    Returns:
        List[str]: 관상학적 해석에 해당하는 키들의 리스트.
    """
    interpretations = []

    # 얼굴형 분석
    if 'face_aspect_ratio' in metrics:
        if metrics['face_aspect_ratio'] < 1.05: # 원형에 가까운 비율
            interpretations.append('FACE_SHAPE_ROUND')
        elif metrics['face_aspect_ratio'] > 1.2: # 긴 얼굴형
            interpretations.append('FACE_SHAPE_LONG')
        else: # 1.05 ~ 1.2 사이의 계란형/밸런스형
            interpretations.append('FACE_SHAPE_BALANCED')

    # 이마 분석
    if 'forehead_ratio' in metrics:
        if metrics['forehead_ratio'] > 0.33:
            interpretations.append('FOREHEAD_WIDE')
        elif metrics['forehead_ratio'] < 0.30:
            interpretations.append('FOREHEAD_NARROW')
        else:
            interpretations.append('FOREHEAD_BALANCED')
    
    # 눈 분석
    if 'eye_spacing_ratio' in metrics:
        if metrics['eye_spacing_ratio'] > 1.1:
            interpretations.append('EYES_SPACED_WIDE')
        elif metrics['eye_spacing_ratio'] < 0.9:
            interpretations.append('EYES_SPACED_NARROW')
        else:
            interpretations.append('EYES_SPACED_BALANCED')

    # 코 분석
    if 'nose_prominence' in metrics and metrics['nose_prominence'] > 0.02:
        interpretations.append('NOSE_PROMINENT')
    if 'nose_width_ratio' in metrics and metrics['nose_width_ratio'] > 0.25:
        interpretations.append('NOSE_WIDE')

    # 입 분석
    if 'lip_thickness_ratio' in metrics and metrics['lip_thickness_ratio'] > 0.4:
        interpretations.append('LIPS_THICK')
    if 'mouth_corner_angle' in metrics and metrics['mouth_corner_angle'] > 1.5:
        interpretations.append('MOUTH_CORNERS_UP')
    elif 'mouth_corner_angle' in metrics and metrics['mouth_corner_angle'] < -1.5:
        interpretations.append('MOUTH_CORNERS_DOWN')

    return interpretations

# --- 테스트용 코드 ---
if __name__ == '__main__':
    # 실제 모듈을 임포트하는 대신 테스트를 위한 더미 함수를 사용합니다.
    def get_dummy_metrics() -> Dict[str, float]:
        """테스트를 위한 기하학적 특징 더미 데이터 생성"""
        print("테스트용 더미 특징 데이터를 생성합니다.")
        return {
            'face_aspect_ratio': 1.0,      # 둥근 얼굴
            'forehead_ratio': 0.35,        # 넓은 이마
            'eye_spacing_ratio': 1.2,      # 넓은 미간
            'nose_prominence': 0.03,       # 높은 코
            'nose_width_ratio': 0.28,      # 넓은 콧방울
            'lip_thickness_ratio': 0.5,    # 두꺼운 입술
            'mouth_corner_angle': 2.0      # 올라간 입꼬리
        }

    geometric_metrics = get_dummy_metrics()
    gwansang_keys = analyze_gwansang_rules(geometric_metrics)
    
    print("\n관상 분석 결과 (해석 키):")
    print(gwansang_keys)

    # 다른 시나리오 테스트
    print("\n--- 다른 시나리오 테스트 ---")
    test_metrics_2 = {
        'face_aspect_ratio': 1.3,
        'forehead_ratio': 0.28,
        'eye_spacing_ratio': 0.8,
        'nose_prominence': 0.01,
        'nose_width_ratio': 0.20,
        'lip_thickness_ratio': 0.3,
        'mouth_corner_angle': -2.0
    }
    gwansang_keys_2 = analyze_gwansang_rules(test_metrics_2)
    print("관상 분석 결과 2 (해석 키):")
    print(gwansang_keys_2)
