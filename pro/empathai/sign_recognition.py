"""
sign_recognition.py

Uses Mediapipe and OpenCV to detect simple hand gestures and map them to a small set of sample signs.
Supported sample gestures: 'hello' (open hand), 'yes' (thumbs up), 'no' (fist), 'thank you' (hand to chin - approximate).

The detection is heuristic-based for demo purposes.
"""
import cv2
import numpy as np

try:
    import mediapipe as mp
except Exception:
    mp = None


mp_hands = mp.solutions.hands if mp is not None else None


def _draw_landmarks(image, hand_landmarks, handedness=None):
    if mp is None:
        return image
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing.draw_landmarks(
        image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
    return image


def fingers_up(hand_landmarks) -> list:
    """Return a list of 5 booleans indicating if each finger is up (thumb->pinky).

    Uses a simple heuristic comparing tip and pip y coordinates for fingers and x for thumb.
    """
    if mp is None or hand_landmarks is None:
        return [False] * 5

    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    lm = hand_landmarks.landmark
    # Thumb: compare x of tip and ip (depends on hand orientation)
    thumb_is_open = lm[tips_ids[0]].x < lm[tips_ids[0] - 1].x
    fingers.append(thumb_is_open)

    # Other fingers: tip y < pip y => finger up (in mediapipe coords top is smaller y)
    for id in tips_ids[1:]:
        fingers.append(lm[id].y < lm[id - 2].y)

    return fingers


def detect_sign_from_frame(frame):
    """Detects a simple sign from a BGR frame.

    Returns (label, annotated_frame).
    """
    label = ""
    annotated = frame.copy()

    if mp is None:
        return "mediapipe-not-installed", annotated

    with mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                         min_detection_confidence=0.5,
                         min_tracking_confidence=0.5) as hands:
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        if not results.multi_hand_landmarks:
            return "no-hand", annotated

        hand_landmarks = results.multi_hand_landmarks[0]
        _draw_landmarks(annotated, hand_landmarks)

        # Heuristic gesture detection
        fup = fingers_up(hand_landmarks)

        # open palm (hello): many fingers up
        if sum(fup[1:]) >= 4:
            label = "hello"
        # fist (no): no fingers up
        elif sum(fup) == 0:
            label = "no"
        # thumbs up (yes): thumb up, others down
        elif fup[0] and sum(fup[1:]) == 0:
            label = "yes"
        else:
            # try detect hand near chin for 'thank you' (approximate)
            # use landmark for wrist and index finger tip
            lm = hand_landmarks.landmark
            wrist = lm[0]
            index_tip = lm[8]
            # If hand is near upper area of image (low y value) and index near wrist x-wise
            h, w, _ = frame.shape
            if index_tip.y * h < h * 0.35:
                label = "thank you"
            else:
                label = "unknown"

        # annotate label
        cv2.putText(annotated, f"Detected: {label}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return label, annotated


if __name__ == "__main__":
    # Quick local test loop (runs if module executed directly)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            label, ann = detect_sign_from_frame(frame)
            cv2.imshow("EmpathAI Sign Demo", ann)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
