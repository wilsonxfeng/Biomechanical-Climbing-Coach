import typer
import cv2


def load_video(video_path: str, display: bool = False):
	"""
	Loads a video for you to enjoy!
	"""

	cap = cv2.VideoCapture(video_path)

	if not cap.isOpened():
		raise RuntimeError("Failed to open video")

	if display:
		fps = cap.get(cv2.CAP_PROP_FPS)
		delay = 1 if fps <= 0 else max(1, int(1000 / fps) - 5)
		while True:
			ok, frame = cap.read()

			if not ok:
				break
			cv2.imshow("Video", frame)
			if cv2.waitKey(delay) & 0xFF == ord("q"):
				break

		cap.release()
		cv2.destroyAllWindows()
	else:
		return cap



if __name__ == "__main__":
	typer.run(load_video)
