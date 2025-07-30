# geometry_calculator.py

import numpy as np
from typing import List, Dict, Any

# MediaPipe 랜드마크 인덱스 (주요 포인트)
# 이 인덱스들은 MediaPipe 공식 문서를 참조하여 정의되었습니다.
# https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png

# 이마 (상단)
FOREHEAD_TOP = 10

# 턱 (하단, 좌측, 우측)
JAW_BOTTOM = 152
JAW_LEFT = 234
JAW_RIGHT = 454

# 눈 (좌측 눈의 좌우 끝, 우측 눈의 좌우 끝)
LEFT_EYE_LEFT_CORNER = 33
LEFT_EYE_RIGHT_CORNER = 133
RIGHT_EYE_LEFT_CORNER = 362
RIGHT_EYE_RIGHT_CORNER = 263

# 코 (코끝, 콧대 상단, 콧방울 좌우)
NOSE_TIP = 1
NOSE_LEFT_WING = 213 
NOSE_RIGHT_WING = 433

# 입술 (윗입술 상단, 아랫입술 하단, 입꼬리 좌우)
LIP_UPPER = 13
LIP_LOWER = 14
LIP_LEFT_CORNER = 61
LIP_RIGHT_CORNER = 291

# 눈썹 중앙 (이마 높이 계산용)
LEFT_EYEBROW_CENTER = 69
RIGHT_EYEBROW_CENTER = 299


def calculate_geometric_metrics(landmarks: List[Any], img_height: int, img_width: int) -> Dict[str, float]:
    """
    랜드마크 리스트를 받아 주요 기하학적 특징들을 계산합니다.
    랜드마크 좌표는 정규화되어 있으므로, 실제 픽셀 좌표로 변환하여 비율을 계산합니다.

    Args:
        landmarks (List[Any]): MediaPipe에서 추출된 랜드마크 객체 리스트.
        img_height (int): 원본 이미지의 높이.
        img_width (int): 원본 이미지의 너비.

    Returns:
        Dict[str, float]: 계산된 기하학적 특징들의 딕셔너리.
    """
    if not landmarks or len(landmarks) < 478: # 478개의 랜드마크가 모두 있는지 확인
        return {}
    
    # 랜드마크를 numpy 배열로 변환 (x, y 좌표만 사용)
    lm_coords = np.array([[lm.x * img_width, lm.y * img_height] for lm in landmarks])

    metrics = {}

    # 1. 얼굴 전체의 높이와 너비
    face_height = np.linalg.norm(lm_coords[FOREHEAD_TOP] - lm_coords[JAW_BOTTOM])
    face_width = np.linalg.norm(lm_coords[JAW_LEFT] - lm_coords[JAW_RIGHT])
    metrics['face_aspect_ratio'] = face_height / face_width if face_width > 0 else 0

    # 2. 이마 비율 (얼굴 높이 대비 이마 높이)
    # 이마 높이를 눈썹 중앙선과 이마 상단점(헤어라인 근처) 사이의 거리로 계산
    eyebrow_mid_y = (lm_coords[LEFT_EYEBROW_CENTER][1] + lm_coords[RIGHT_EYEBROW_CENTER][1]) / 2
    forehead_height = eyebrow_mid_y - lm_coords[FOREHEAD_TOP][1]
    metrics['forehead_ratio'] = forehead_height / face_height if face_height > 0 else 0
    
    # 3. 눈 사이 거리 (미간 너비) / 눈의 너비
    inter_eye_distance = np.linalg.norm(lm_coords[RIGHT_EYE_LEFT_CORNER] - lm_coords[LEFT_EYE_RIGHT_CORNER])
    left_eye_width = np.linalg.norm(lm_coords[LEFT_EYE_RIGHT_CORNER] - lm_coords[LEFT_EYE_LEFT_CORNER])
    metrics['eye_spacing_ratio'] = inter_eye_distance / left_eye_width if left_eye_width > 0 else 0

    # 4. 코의 너비 / 얼굴 너비
    nose_width = np.linalg.norm(lm_coords[NOSE_RIGHT_WING] - lm_coords[NOSE_LEFT_WING])
    metrics['nose_width_ratio'] = nose_width / face_width if face_width > 0 else 0
    
    # 5. 코의 돌출 정도 (z좌표를 이용한 상대적 높이)
    # z좌표는 카메라로부터의 거리를 나타내므로, 값이 작을수록 돌출됨을 의미.
    # 코끝과 콧방울의 z값 차이로 높이를 추정.
    nose_tip_z = landmarks[NOSE_TIP].z
    nose_wing_z_avg = (landmarks[NOSE_LEFT_WING].z + landmarks[NOSE_RIGHT_WING].z) / 2
    metrics['nose_prominence'] = nose_wing_z_avg - nose_tip_z # 양수일수록 코가 돌출됨

    # 6. 입술 두께 (입술 상하 거리) / 입 너비
    lip_height = np.linalg.norm(lm_coords[LIP_LOWER] - lm_coords[LIP_UPPER])
    lip_width = np.linalg.norm(lm_coords[LIP_RIGHT_CORNER] - lm_coords[LIP_LEFT_CORNER])
    metrics['lip_thickness_ratio'] = lip_height / lip_width if lip_width > 0 else 0

    # 7. 입꼬리 방향 (입꼬리와 입술 중앙의 y좌표 비교)
    lip_center_y = (lm_coords[LIP_UPPER][1] + lm_coords[LIP_LOWER][1]) / 2
    lip_corners_y_avg = (lm_coords[LIP_LEFT_CORNER][1] + lm_coords[LIP_RIGHT_CORNER][1]) / 2
    metrics['mouth_corner_angle'] = lip_center_y - lip_corners_y_avg # 양수일수록 입꼬리가 올라감

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
