# rule_engine.py

from typing import Dict, List

def analyze_gwansang_rules(metrics: Dict[str, float]) -> List[str]:
    """
    기하학적 특징 딕셔너리를 입력받아, 정의된 규칙에 따라
    관상학적 해석 키 리스트를 반환합니다.
    """
    interpretations = []

    # --- 얼굴형 (Face Shape) ---
    if 'face_aspect_ratio' in metrics:
        if metrics['face_aspect_ratio'] < 0.95: # 너비가 높이보다 큼
            interpretations.append('FACE_SHAPE_ROUND')
        elif metrics['face_aspect_ratio'] > 1.1:
            interpretations.append('FACE_SHAPE_LONG')
        elif metrics.get('jaw_to_cheek_width_ratio', 1.0) > 0.95:
            interpretations.append('FACE_SHAPE_SQUARE')
        elif metrics.get('jaw_to_cheek_width_ratio', 1.0) < 0.8:
            interpretations.append('FACE_SHAPE_INVERTED_TRIANGLE')
        else:
            interpretations.append('FACE_SHAPE_EGG')

    # --- 이마 (Forehead) ---
    if 'forehead_height_ratio' in metrics:
        if metrics['forehead_height_ratio'] > 0.35:
            interpretations.append('FOREHEAD_WIDE_HIGH')
        elif metrics['forehead_height_ratio'] < 0.30:
            interpretations.append('FOREHEAD_NARROW')
    if 'forehead_m_shape_curve' in metrics and metrics['forehead_m_shape_curve'] > 0.02:
        interpretations.append('FOREHEAD_M_SHAPE')

    # --- 눈 (Eyes) ---
    if 'eye_size_ratio' in metrics:
        if metrics['eye_size_ratio'] > 0.015:
            interpretations.append('EYES_LARGE')
        else:
            interpretations.append('EYES_SMALL')
    if 'left_eye_slant' in metrics and 'right_eye_slant' in metrics:
        avg_slant = (metrics['left_eye_slant'] + metrics['right_eye_slant']) / 2
        if avg_slant > 5:
            interpretations.append('EYES_UPWARD_SLANTING')
        elif avg_slant < -5:
            interpretations.append('EYES_DOWNWARD_SLANTING')
    if 'eye_spacing_ratio' in metrics:
        if metrics['eye_spacing_ratio'] > 1.1:
            interpretations.append('EYES_SPACED_WIDE')
        elif metrics['eye_spacing_ratio'] < 0.9:
            interpretations.append('EYES_SPACED_NARROW')

    # --- 눈썹 (Eyebrows) ---
    if 'eyebrow_length_ratio' in metrics:
        if metrics['eyebrow_length_ratio'] > 1.1:
            interpretations.append('EYEBROWS_LONG')
        elif metrics['eyebrow_length_ratio'] < 0.9:
            interpretations.append('EYEBROWS_SHORT')
    if 'eyebrow_thickness' in metrics and metrics['eyebrow_thickness'] > 0.01:
        interpretations.append('EYEBROWS_THICK')
    else:
        interpretations.append('EYEBROWS_THIN')
    if 'eyebrow_arch' in metrics:
        if abs(metrics['eyebrow_arch']) < 5:
            interpretations.append('EYEBROWS_STRAIGHT')
        else:
            interpretations.append('EYEBROWS_CRESCENT')
    if 'eyebrow_slant' in metrics:
        if metrics['eyebrow_slant'] > 5:
            interpretations.append('EYEBROWS_UPWARD')
        elif metrics['eyebrow_slant'] < -5:
            interpretations.append('EYEBROWS_DOWNWARD')

    # --- 코 (Nose) ---
    if 'nose_height_ratio' in metrics and 'nose_width_ratio' in metrics:
        if metrics['nose_height_ratio'] > 0.3 and metrics['nose_width_ratio'] < 0.2:
            interpretations.append('NOSE_LARGE') # 높고 좁은 코
        elif metrics['nose_height_ratio'] < 0.25:
            interpretations.append('NOSE_SMALL')
    if 'nose_width_ratio' in metrics and metrics['nose_width_ratio'] > 0.25:
        interpretations.append('NOSE_WIDE_WINGS')
    if 'nose_tip_sharpness' in metrics:
        if metrics['nose_tip_sharpness'] > 0.02:
            interpretations.append('NOSE_POINTED_TIP')
        else:
            interpretations.append('NOSE_ROUNDED_TIP')
    if 'nose_upturned_angle' in metrics and metrics['nose_upturned_angle'] < -5:
        interpretations.append('NOSE_UPTURNED')

    # --- 광대뼈 (Cheekbones) ---
    if 'cheekbone_prominence' in metrics:
        if metrics['cheekbone_prominence'] > 0.05:
            interpretations.append('CHEEKBONES_PROMINENT')
        else:
            interpretations.append('CHEEKBONES_BALANCED')

    # --- 입술 및 입 (Lips & Mouth) ---
    if 'lip_thickness_ratio' in metrics:
        if metrics['lip_thickness_ratio'] > 0.5:
            interpretations.append('LIPS_THICK')
        else:
            interpretations.append('LIPS_THIN')
    if 'mouth_size_ratio' in metrics:
        if metrics['mouth_size_ratio'] > 0.4:
            interpretations.append('MOUTH_LARGE')
        else:
            interpretations.append('MOUTH_SMALL')
    if 'mouth_corner_angle' in metrics:
        if metrics['mouth_corner_angle'] > 2:
            interpretations.append('MOUTH_CORNERS_UP')
        elif metrics['mouth_corner_angle'] < -2:
            interpretations.append('MOUTH_CORNERS_DOWN')
    if 'lip_upper_to_lower_ratio' in metrics:
        if metrics['lip_upper_to_lower_ratio'] > 1.2:
            interpretations.append('LIPS_UPPER_THICKER')
        elif metrics['lip_upper_to_lower_ratio'] < 0.8:
            interpretations.append('LIPS_LOWER_THICKER')

    # --- 턱 (Chin/Jaw) ---
    if 'jaw_width_ratio' in metrics:
        if metrics['jaw_width_ratio'] > 0.8:
            interpretations.append('JAW_SQUARE')
        else:
            interpretations.append('JAW_POINTED_VLINE')
    if 'chin_prominence' in metrics:
        if metrics['chin_prominence'] < -0.1:
            interpretations.append('JAW_PROTRUDING')
        elif metrics['chin_prominence'] > 0.1:
            interpretations.append('JAW_RECEDING')

    # --- 인중 (Philtrum) ---
    if 'philtrum_height_ratio' in metrics:
        if metrics['philtrum_height_ratio'] > 0.2:
            interpretations.append('PHILTRUM_LONG')
        else:
            interpretations.append('PHILTRUM_SHORT')

    # --- 법령 (Nasolabial Folds) ---
    if 'nasolabial_depth' in metrics and metrics['nasolabial_depth'] > 0.01:
        interpretations.append('NASOLABIAL_CLEAR_LONG')
    else:
        interpretations.append('NASOLABIAL_FAINT_SHORT')

    return list(set(interpretations)) # 중복 제거 후 반환


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
