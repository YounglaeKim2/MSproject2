import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 솔루션 초기화
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def get_face_landmarks(image_path: str, visualize: bool = False):
    """
    이미지 경로를 입력받아 얼굴 랜드마크를 추출하고, 선택적으로 시각화합니다.

    Args:
        image_path (str): 분석할 이미지 파일의 경로.
        visualize (bool): 랜드마크를 시각화하여 보여줄지 여부.

    Returns:
        tuple: 성공 시 (랜드마크 리스트, 이미지 높이, 이미지 너비), 실패 시 (None, None, None).
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"오류: 이미지를 로드할 수 없습니다. 경로: {image_path}")
            return None, None, None
        
        image_height, image_width, _ = image.shape
        
        # FaceMesh 모델 실행
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7) as face_mesh:
            
            # BGR 이미지를 RGB로 변환
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.multi_face_landmarks:
                print("경고: 이미지에서 얼굴을 감지하지 못했습니다.")
                return None, None, None

            # 첫 번째 감지된 얼굴의 랜드마크만 사용
            face_landmarks = results.multi_face_landmarks[0]
            
            # 시각화 옵션이 켜져 있을 경우
            if visualize:
                annotated_image = image.copy()
                # 얼굴 메쉬 그리기
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                # 얼굴 윤곽선, 눈, 코, 입 등 그리기
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                # 눈동자 그리기
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
                
                # 결과 이미지 보여주기
                cv2.imshow('Face Landmarks', annotated_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return face_landmarks.landmark, image_height, image_width

    except Exception as e:
        print(f"랜드마크 추출 중 오류 발생: {e}")
        return None, None, None

# --- 테스트용 코드 ---
if __name__ == '__main__':
    # 테스트할 이미지 경로를 지정하세요.
    test_image_path = 'input_image.jpg' 
    landmarks, height, width = get_face_landmarks(test_image_path, visualize=True)
    
    if landmarks:
        print(f"성공: {len(landmarks)}개의 랜드마크를 추출했습니다.")
        # 첫 번째 랜드마크의 정규화된 좌표 출력
        print(f"랜드마크 0: (x={landmarks[0].x}, y={landmarks[0].y}, z={landmarks[0].z})")