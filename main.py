import cv2
import mediapipe as mp
from chord_wheel import ChordWheel

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
UI_FONT = cv2.FONT_HERSHEY_DUPLEX

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

wheel = ChordWheel()


def landmark_to_pixel(landmark, width, height):
    return int(landmark.x * width), int(landmark.y * height)


def right_hand_gesture(hand_landmarks):
    fingers_up = 0
    finger_pairs = [(8, 6), (12, 10), (16, 14), (20, 18)]

    for tip_id, pip_id in finger_pairs:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[pip_id].y:
            fingers_up += 1

    if fingers_up >= 4:
        return "PLAY"
    if fingers_up == 0:
        return "MUTE"
    if fingers_up == 1:
        return "STRUM"
    return "HOLD"


# Webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert BGR -> RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    left_index_point = None
    right_control = "IDLE"

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness
        ):
            hand_label = handedness.classification[0].label
            index_tip = hand_landmarks.landmark[8]

            if hand_label == "Left":
                left_index_point = landmark_to_pixel(index_tip, w, h)
            elif hand_label == "Right":
                right_control = right_hand_gesture(hand_landmarks)

    active_chord = wheel.draw(frame, left_index_point)

    # Draw landmarks
    if results.multi_hand_landmarks and results.multi_handedness:

        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness
        ):

            # Draw hand skeleton
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Hand label
            hand_label = handedness.classification[0].label

            index_tip = hand_landmarks.landmark[8]
            x, y = landmark_to_pixel(index_tip, w, h)

            cv2.circle(frame, (x, y), 12, (0, 0, 255), -1)

    if active_chord:
        cv2.putText(
            frame,
            f"Chord: {active_chord}",
            (24, h - 56),
            UI_FONT,
            0.8,
            (255, 255, 255),
            2
        )

    cv2.putText(
        frame,
        f"Right: {right_control}",
        (24, h - 24),
        UI_FONT,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("AirChord", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
