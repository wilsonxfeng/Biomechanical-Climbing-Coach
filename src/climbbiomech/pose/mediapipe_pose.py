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


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(model_path)),
    running_mode=VisionRunningMode.VIDEO)

def getss(video_path: str, full: bool = True, seconds: int = 0):

	video = load_video(video_path)
	fps = video.get(cv2.CAP_PROP_FPS)
	delay = 1 if fps <= 0 else max(1, int(1000 / fps) - 5)

	video.set(cv2.CAP_PROP_POS_MSEC, int(seconds * 1000))
	ok, frame = video.read()
	if ok:
		cv2.imwrite("frame.png", frame)

	frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
			data=frame_rgb)
	pose_landmarker_result = landmarker.detect_for_video(mp_image,
			int(seconds * 1000))

	video.release()

	return frame, pose_landmarker_result

def main(video_path: str):

	video = load_video(video_path)
	fps = video.get(cv2.CAP_PROP_FPS)
	delay = 1 if fps <= 0 else max(1, int(1000 / fps) - 5)

	with PoseLandmarker.create_from_options(options) as landmarker:
		frame_idx = 0
		while True:
			ok, frame = video.read()

			if not ok:
				break

			frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
					data=frame_rgb)
			timestamp = int((frame_idx / fps) * 1000)
			pose_landmarker_result = landmarker.detect_for_video(mp_image,
					timestamp)

			frame = draw_joints(frame, pose_landmarker_result)

			cv2.imshow("Video", frame)
			if cv2.waitKey(delay) & 0xFF == ord("q"):
				break

			frame_idx += 1

		video.release()
		cv2.destroyAllWindows()



if __name__ == "__main__":
	typer.run(main)
	# print("Hello World!")
