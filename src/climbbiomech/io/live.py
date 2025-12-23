import cv2
from pathlib import Path
import typer
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from climbbiomech.io.video import load_video
from climbbiomech.render.draw_joints import draw_joints



model_path = Path(__file__).resolve().parents[2]/"landmark models"/"pose_landmarker_full.task"
output_path = Path(__file__).resolve().parents[3]/"outputs"/"annotated.mp4"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(model_path)),
    running_mode=VisionRunningMode.VIDEO)



def main():
    cap = cv2.VideoCapture(0)  # 0 = default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    with PoseLandmarker.create_from_options(options) as landmarker:

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                    data=frame_rgb)
            timestamp = int((frame_idx / 30) * 1000)
            pose_landmarker_result = landmarker.detect_for_video(mp_image,
                    timestamp)

            frame = draw_joints(frame, pose_landmarker_result)

            cv2.imshow("Webcam Feed", frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_idx += 1


        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
