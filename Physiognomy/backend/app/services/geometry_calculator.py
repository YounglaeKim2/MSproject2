# geometry_calculator.py

import numpy as np
from typing import List, Dict, Any

# MediaPipe 랜드마크 인덱스 (주요 포인트)
# 이 인덱스들은 MediaPipe 공식 문서를 참조하여 정의되었습니다.
# https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png

# 얼굴 윤곽 (Face Contour)
FOREHEAD_TOP = 10
JAW_BOTTOM = 152
JAW_LEFT = 234
JAW_RIGHT = 454
CHEEK_LEFT = 117 # 왼쪽 광대
CHEEK_RIGHT = 346 # 오른쪽 광대

# 눈 (Eyes)
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_EYE_LEFT_CORNER = 33
LEFT_EYE_RIGHT_CORNER = 133
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
RIGHT_EYE_LEFT_CORNER = 362
RIGHT_EYE_RIGHT_CORNER = 263

# 눈썹 (Eyebrows)
LEFT_EYEBROW_OUTER_END = 52
LEFT_EYEBROW_INNER_END = 55
RIGHT_EYEBROW_OUTER_END = 282
RIGHT_EYEBROW_INNER_END = 285
LEFT_EYEBROW_CENTER_TOP = 105
RIGHT_EYEBROW_CENTER_TOP = 334

# 코 (Nose)
NOSE_TIP = 1
NOSE_BRIDGE_TOP = 6
NOSE_BRIDGE_BOTTOM = 168
NOSE_LEFT_WING = 213
NOSE_RIGHT_WING = 433

# 입술 (Lips)
LIP_UPPER_TOP = 13
LIP_LOWER_BOTTOM = 14
LIP_LEFT_CORNER = 61
LIP_RIGHT_CORNER = 291
UPPER_LIP_CENTER_BOTTOM = 0
LOWER_LIP_CENTER_TOP = 17

# 턱 (Chin)
CHIN_CENTER = 152 # JAW_BOTTOM과 동일
CHIN_LEFT = 326
CHIN_RIGHT = 97

# 귀 (Ears) - MediaPipe는 귀 랜드마크를 제공하지 않음. 다른 방법 필요.
# 인중 (Philtrum)
PHILTRUM_TOP = 164
PHILTRUM_BOTTOM = 0 # UPPER_LIP_CENTER_BOTTOM과 동일

# 법령 (Nasolabial Folds) - 특정 랜드마크가 없으므로 주변 랜드마크로 추정
NASOLABIAL_LEFT_UPPER = 205
NASOLABIAL_RIGHT_UPPER = 425


def calculate_geometric_metrics(landmarks: List[Any], img_height: int, img_width: int) -> Dict[str, float]:
    """
    랜드마크 리스트를 받아 주요 기하학적 특징들을 계산합니다.
    랜드마크 좌표는 정규화되어 있으므로, 실제 픽셀 좌표로 변환하여 비율을 계산합니다.
    """
    if not landmarks or len(landmarks) < 478:
        return {}

    lm_coords = np.array([[lm.x * img_width, lm.y * img_height] for lm in landmarks])
    lm_coords_z = np.array([lm.z for lm in landmarks])

    metrics = {}

    # --- 얼굴 전체 및 기본 비율 ---
    face_height = np.linalg.norm(lm_coords[FOREHEAD_TOP] - lm_coords[JAW_BOTTOM])
    face_width = np.linalg.norm(lm_coords[JAW_LEFT] - lm_coords[JAW_RIGHT])
    metrics['face_height'] = face_height
    metrics['face_width'] = face_width
    metrics['face_aspect_ratio'] = face_height / face_width if face_width > 0 else 0

    # --- 얼굴형 (Face Shape) ---
    # 광대뼈 너비
    cheek_width = np.linalg.norm(lm_coords[CHEEK_LEFT] - lm_coords[CHEEK_RIGHT])
    # 턱 너비 (입꼬리 아래)
    jaw_width = np.linalg.norm(lm_coords[326] - lm_coords[97])
    metrics['cheek_to_face_width_ratio'] = cheek_width / face_width
    metrics['jaw_to_cheek_width_ratio'] = jaw_width / cheek_width if cheek_width > 0 else 0

    # --- 이마 (Forehead) ---
    eyebrow_mid_y = (lm_coords[LEFT_EYEBROW_INNER_END][1] + lm_coords[RIGHT_EYEBROW_INNER_END][1]) / 2
    forehead_height = eyebrow_mid_y - lm_coords[FOREHEAD_TOP][1]
    metrics['forehead_height_ratio'] = forehead_height / face_height if face_height > 0 else 0
    # M자 이마 (헤어라인 굴곡)
    forehead_center_x = lm_coords[FOREHEAD_TOP][0]
    forehead_left_x = lm_coords[104][0] # 왼쪽 이마 상단
    forehead_right_x = lm_coords[333][0] # 오른쪽 이마 상단
    metrics['forehead_m_shape_curve'] = (forehead_center_x - (forehead_left_x + forehead_right_x) / 2) / face_width

    # --- 눈 (Eyes) ---
    left_eye_height = np.linalg.norm(lm_coords[LEFT_EYE_TOP] - lm_coords[LEFT_EYE_BOTTOM])
    left_eye_width = np.linalg.norm(lm_coords[LEFT_EYE_RIGHT_CORNER] - lm_coords[LEFT_EYE_LEFT_CORNER])
    metrics['left_eye_aspect_ratio'] = left_eye_height / left_eye_width if left_eye_width > 0 else 0
    metrics['eye_size_ratio'] = (left_eye_height * left_eye_width) / (face_height * face_width) if face_height * face_width > 0 else 0
    # 눈꼬리 각도
    metrics['left_eye_slant'] = lm_coords[LEFT_EYE_LEFT_CORNER][1] - lm_coords[LEFT_EYE_RIGHT_CORNER][1]
    metrics['right_eye_slant'] = lm_coords[RIGHT_EYE_RIGHT_CORNER][1] - lm_coords[RIGHT_EYE_LEFT_CORNER][1]
    # 눈 사이 거리
    inter_eye_distance = np.linalg.norm(lm_coords[RIGHT_EYE_LEFT_CORNER] - lm_coords[LEFT_EYE_RIGHT_CORNER])
    metrics['eye_spacing_ratio'] = inter_eye_distance / left_eye_width if left_eye_width > 0 else 0

    # --- 눈썹 (Eyebrows) ---
    left_eyebrow_length = np.linalg.norm(lm_coords[LEFT_EYEBROW_OUTER_END] - lm_coords[LEFT_EYEBROW_INNER_END])
    metrics['eyebrow_length_ratio'] = left_eyebrow_length / left_eye_width if left_eye_width > 0 else 0
    # 눈썹 두께 (z값으로 추정)
    metrics['eyebrow_thickness'] = abs(lm_coords_z[LEFT_EYEBROW_CENTER_TOP] - lm_coords_z[107]) # 눈썹 위쪽과 아래쪽 z값 차이
    # 눈썹 모양 (직선/아치)
    eyebrow_center_y = lm_coords[LEFT_EYEBROW_CENTER_TOP][1]
    eyebrow_ends_y_avg = (lm_coords[LEFT_EYEBROW_INNER_END][1] + lm_coords[LEFT_EYEBROW_OUTER_END][1]) / 2
    metrics['eyebrow_arch'] = eyebrow_ends_y_avg - eyebrow_center_y
    # 눈썹 각도
    metrics['eyebrow_slant'] = lm_coords[LEFT_EYEBROW_INNER_END][1] - lm_coords[LEFT_EYEBROW_OUTER_END][1]

    # --- 코 (Nose) ---
    nose_height = np.linalg.norm(lm_coords[NOSE_BRIDGE_BOTTOM] - lm_coords[NOSE_BRIDGE_TOP])
    nose_width = np.linalg.norm(lm_coords[NOSE_RIGHT_WING] - lm_coords[NOSE_LEFT_WING])
    metrics['nose_height_ratio'] = nose_height / face_height if face_height > 0 else 0
    metrics['nose_width_ratio'] = nose_width / face_width if face_width > 0 else 0
    # 코끝 모양 (z값으로 뾰족함 측정)
    nose_tip_z = lm_coords_z[NOSE_TIP]
    nose_bridge_z = lm_coords_z[NOSE_BRIDGE_BOTTOM]
    metrics['nose_tip_sharpness'] = nose_bridge_z - nose_tip_z # 값이 클수록 뾰족
    # 들창코 (코끝과 콧대 바닥의 y좌표 비교)
    metrics['nose_upturned_angle'] = lm_coords[NOSE_TIP][1] - lm_coords[NOSE_BRIDGE_BOTTOM][1]

    # --- 광대뼈 (Cheekbones) ---
    cheek_prominence_left = lm_coords_z[JAW_LEFT] - lm_coords_z[CHEEK_LEFT]
    cheek_prominence_right = lm_coords_z[JAW_RIGHT] - lm_coords_z[CHEEK_RIGHT]
    metrics['cheekbone_prominence'] = (cheek_prominence_left + cheek_prominence_right) / 2

    # --- 입술 및 입 (Lips & Mouth) ---
    lip_height = np.linalg.norm(lm_coords[LIP_LOWER_BOTTOM] - lm_coords[LIP_UPPER_TOP])
    lip_width = np.linalg.norm(lm_coords[LIP_RIGHT_CORNER] - lm_coords[LIP_LEFT_CORNER])
    metrics['lip_thickness_ratio'] = lip_height / lip_width if lip_width > 0 else 0
    metrics['mouth_size_ratio'] = lip_width / face_width if face_width > 0 else 0
    # 입꼬리 각도
    lip_center_y = (lm_coords[LIP_UPPER_TOP][1] + lm_coords[LIP_LOWER_BOTTOM][1]) / 2
    lip_corners_y_avg = (lm_coords[LIP_LEFT_CORNER][1] + lm_coords[LIP_RIGHT_CORNER][1]) / 2
    metrics['mouth_corner_angle'] = lip_center_y - lip_corners_y_avg
    # 윗입술/아랫입술 두께 비교
    upper_lip_thickness = np.linalg.norm(lm_coords[LIP_UPPER_TOP] - lm_coords[UPPER_LIP_CENTER_BOTTOM])
    lower_lip_thickness = np.linalg.norm(lm_coords[LOWER_LIP_CENTER_TOP] - lm_coords[LIP_LOWER_BOTTOM])
    metrics['lip_upper_to_lower_ratio'] = upper_lip_thickness / lower_lip_thickness if lower_lip_thickness > 0 else 0

    # --- 턱 (Chin/Jaw) ---
    metrics['jaw_width_ratio'] = jaw_width / face_width if face_width > 0 else 0
    # 주걱턱/무턱 (z값으로 판단)
    metrics['chin_prominence'] = lm_coords_z[FOREHEAD_TOP] - lm_coords_z[CHIN_CENTER]

    # --- 인중 (Philtrum) ---
    philtrum_height = np.linalg.norm(lm_coords[PHILTRUM_TOP] - lm_coords[PHILTRUM_BOTTOM])
    metrics['philtrum_height_ratio'] = philtrum_height / nose_height if nose_height > 0 else 0

    # --- 법령 (Nasolabial Folds) ---
    # 법령의 깊이는 z값의 차이로 추정
    metrics['nasolabial_depth'] = (lm_coords_z[NASOLABIAL_LEFT_UPPER] + lm_coords_z[NASOLABIAL_RIGHT_UPPER]) / 2 - lm_coords_z[NOSE_LEFT_WING]

    return metrics


# --- 테스트용 코드 ---
if __name__ == '__main__':
    # face_landmarker.py의 get_face_landmarks 함수를 임포트해야 합니다.
    # 이 스크립트를 단독으로 실행하려면 아래 줄의 주석을 해제하고,
    # face_landmarker.py가 동일한 디렉토리에 있거나 PYTHONPATH에 포함되어야 합니다.
    # from face_landmarker import get_face_landmarks 
    
    # get_face_landmarks 함수가 없으므로, 테스트를 위한 임시 함수 및 데이터 생성
    def get_face_landmarks_for_test(image_path: str):
        """테스트를 위한 더미 랜드마크 생성 함수"""
        print(f"'{image_path}'에 대한 랜드마크 추출을 시뮬레이션합니다. 실제 모듈이 필요합니다.")
        
        class DummyLandmark:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        # 478개의 랜덤 랜드마크 생성
        dummy_landmarks = [DummyLandmark(np.random.rand(), np.random.rand(), np.random.rand()) for _ in range(478)]
        return dummy_landmarks, 800, 600

    test_image_path = 'input_image.jpg'
    # 실제 사용 시에는 face_landmarker.get_face_landmarks(test_image_path)를 호출해야 합니다.
    landmarks, height, width = get_face_landmarks_for_test(test_image_path)
    
    if landmarks:
        geometric_metrics = calculate_geometric_metrics(landmarks, height, width)
        print("\n계산된 기하학적 특징:")
        for key, value in geometric_metrics.items():
            print(f"- {key}: {value:.4f}")
