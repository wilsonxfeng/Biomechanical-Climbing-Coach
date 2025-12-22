from pathlib import Path
import cv2
import typer
import numpy
from climbbiomech.pose.landmark_enumeration import PoseLandmarks, ImportantLandmarks, BoneLandmarks


def draw_joints(frame, result):

	if not result.pose_landmarks:
		return frame

	pose = result.pose_landmarks[0]
	H, W = frame.shape[0], frame.shape[1]
	color = [255, 255, 255]

	for joint in ImportantLandmarks:

		joint_info = pose[PoseLandmarks[joint]]
		x_px = int(joint_info.x * W)
		y_px = int(joint_info.y * H)

		if joint_info.visibility >= 0.4 and joint_info.presence >= 0.4 and x_px < W and y_px < H:

			coords = [x_px, y_px]

			cv2.circle(frame, coords, 10, color, 5)

	for bone in BoneLandmarks:
		start = pose[PoseLandmarks[bone[0]]]
		end = pose[PoseLandmarks[bone[1]]]

		x1_px = int(start.x * W)
		x2_px = int(end.x * W)
		y1_px = int(start.y * H)
		y2_px = int(end.y * H)

		startcoords = [x1_px, y1_px]
		endcoords = [x2_px, y2_px]

		cv2.line(frame, startcoords, endcoords, color, 3)



	return frame


if __name__ == "__main__":
	typer.run(draw_joints)

