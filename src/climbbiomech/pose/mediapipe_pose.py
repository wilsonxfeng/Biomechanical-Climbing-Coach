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


def main(video_path: str, output_path: str = output_path):

	video = load_video(video_path)
	frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = video.get(cv2.CAP_PROP_FPS)

	fourcc = cv2.VideoWriter_fourcc(*"mp4v")
	out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

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

			out.write(frame)

			cv2.imshow("Video", frame)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break

			frame_idx += 1

		video.release()
		cv2.destroyAllWindows()



if __name__ == "__main__":
	typer.run(main)
	# print("Hello World!")
