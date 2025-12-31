import cv2
from src.climbbiomech.pose.landmark_enumeration import PoseLandmarks
import numpy
from src.sidetracked_days.rel import generate_rels

def draw(frame, landmarks):

    if not landmarks.pose_landmarks:
        return frame
    
    pose = landmarks.pose_landmarks[0]
    H, W = frame.shape[0], frame.shape[1]
    color = [255, 255, 255]

    for landmark in range(33):
        joint_info = pose[landmark]
        x_px = int(joint_info.x * W)
        y_px = int(joint_info.y * H)

#       if joint_info.presence >= 0.5:
        coords = [x_px, y_px]
        # cv2.circle(frame, coords, 10, color, 5)
        cv2.putText(
                frame,
                f"{landmark}",
                (coords[0], coords[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
                cv2.LINE_AA
                )


    return frame


