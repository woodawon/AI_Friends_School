import cv2  # OpenCV 라이브러리 import
import sys  # sys 모듈 import
import mediapipe as mp  # MediaPipe 패키지 import하고 mp라는 별칭으로 사용하겠다는 뜻.


# !!!!! - mediapipe 내용 추가된 부분
# MediaPipe 패키지에서 사용할 기능들.
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = (
    mp.solutions.hands
)  # 손 인식을 위한 객체 - mediapipe.python.solutions의 hands 모듈 불러온다는 뜻.
# !!!!!


cap = cv2.VideoCapture(0)  # 비디오 캡처 객체 생성(OpenCV 라이브러리 : cv2)

if not cap.isOpened():  # 연결 확인
    print("Camera is not opened")
    sys.exit(1)  # 프로그램 종료

hands = mp_hands.Hands()  # 손 인식 객체 생성 - mp.solutions.hands 내부의 Hands() 클래스를 의미함.

while True:  # 무한 반복
    res, frame = cap.read()  # 카메라 데이터 읽기(T&F, frame data)

    if not res:  # 프레임 읽었는지 확인(True, False)
        print("Camera error")
        break  # 반복문 종료

    # !!!!! - mediapipe 22.

    frame = cv2.flip(frame, 1)  # 셀프 카메라처럼 좌우 반전(= 대칭 변환)

    image = cv2.cvtColor(
        frame, cv2.COLOR_BGR2RGB
    )  # 미디어파이프에서 인식 가능한 색공간으로 변경 -> (frame)BGR을 RGB인식으로 바꿔준다는 뜻.
    # cvtColor() 함수 : 이미지와 색 공간 정보를 받아 변경해줌.
    # OpenCV는 이미지를 BGR 순서로 읽음 But Mediapipe는 RGB 순서로 이미지를 읽을 수 있어서 알맞게 변경해주는 거임.

    # hands.process(image) -> MediaPipe의 hands 모듈을 이용해서 손동작을 인식한다. 이 한줄로서 손동작 인식 AI모델이 작동되고 결과 값이 result로 저장된다.
    results = hands.process(image)  # 이미지에서 손을 찾고 결과를 반환

    if results.multi_hand_landmarks:  # 손이 인식되었는지 확인
        # mulit_hand_landmarks => mp_hands의 Hand() 클래스 안의 super()__init__() 안의 outputs[] 안에 들어있는 요소.
        for (
            hand_landmarks
        ) in results.multi_hand_landmarks:  # !!! 반복문을 활용해 인식된 손의 주요 부분을 그림으로 그려 표현 !!!
            mp_drawing.draw_landmarks(
                frame,  # image
                hand_landmarks,  # landmark_list
                mp_hands.HAND_CONNECTIONS,  # connections
                mp_drawing_styles.get_default_hand_landmarks_style(),  # landmark_drawing_spec
                mp_drawing_styles.get_default_hand_connections_style(),  # connection_drawing_spec
            )

    # !!!!!

    cv2.imshow("MediaPipe Hands", frame)  # 영상을 화면에 출력.

    key = cv2.waitKey(5) & 0xFF  # 키보드 입력받기
    if key == 27:  # ESC를 눌렀을 경우
        break  # 반복문 종료

cv2.destroyAllWindows()  # 영상 창 닫기
cap.release()  # 비디오 캡처 객체 해제
