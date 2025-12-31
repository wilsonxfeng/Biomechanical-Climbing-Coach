import cv2
import typer
import mediapipe as mp
from src.sidetracked_days.draw_landmarks import draw
from pathlib import Path
from src.sidetracked_days.rel import generate_rels
from src.sidetracked_days.rel import niche_baby_dists
from src.sidetracked_days.rel import curious_monkey_dists
from src.sidetracked_days.rel import six_seven_dists
from src.sidetracked_days.check import cmpr
import time



model_path = Path(__file__).resolve().parents[1]/"landmark models"/"pose_landmarker_full.task"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(model_path)),
    running_mode=VisionRunningMode.VIDEO)


def main(option: int = 0):
    
    if option == 0:
        img0 = cv2.imread("nicheNormal.png")
        img1 = cv2.imread("niche.png")
    elif option == 1:
        img0 = cv2.imread("monkeyNormal.png")
        img1 = cv2.imread("monkeyCurious.png")
    elif option == 2:
        img0 = cv2.imread("ssNormal.png")
        img1 = cv2.imread("ss.png")



    state = 0
    cap = cv2.VideoCapture(0)    

    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    if not cap.isOpened():
        print("error: could not open camera")
        return

    with PoseLandmarker.create_from_options(options) as Landmarker:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not grab frame")
                break

            frame = cv2.flip(frame, 1)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                    data=frame_rgb)
            timestamp = int((frame_idx / 30) * 1000)
            pose_landmarker_result = Landmarker.detect_for_video(mp_image,
                    timestamp)

            # frame = draw(frame, pose_landmarker_result)
             

            cv2.imshow("Investing", frame)

            if option == 0:
                res = cmpr(niche_baby_dists, generate_rels(pose_landmarker_result))
            elif option == 1:
                res = cmpr(curious_monkey_dists, generate_rels(pose_landmarker_result))
            elif option == 2:
                res = cmpr(six_seven_dists, generate_rels(pose_landmarker_result, 1))

            if res:
                print("MAX WINNNNNN !!!!!!!!!!!1")
                state = 1
            else:
                print("no....")
                state = 0

            if state == 1:
                cv2.imshow("Output", img1)
            elif state == 0:
                cv2.imshow("Output", img0)

            if cv2.waitKey(1) & 0xFF == ord('q'):

                with open("six_seven.txt", "w") as f:
                    f.write(str(generate_rels(pose_landmarker_result, 1)))
                break



            frame_idx += 1
        
        cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    typer.run(main)
