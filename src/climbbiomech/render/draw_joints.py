from pathlib import Path
import cv2
import typer
import numpy
from climbbiomech.pose.landmark_enumeration import PoseLandmark


def draw_joints(frame, result):

	if not result.pose_landmarks:
		return frame

	pose = result.pose_landmarks[0]
	H, W = frame.shape[0], frame.shape[1]

	for joint in range(len(pose)):

		joint_info = pose[joint]
		x_px = int(joint_info.x * W)
		y_px = int(joint_info.y * H)

		if joint_info.visibility >= 0.4 and joint_info.presence >= 0.4 and x_px < W and y_px < H:

			coords = [x_px, y_px]
			color = [255, 255, 255]

			cv2.circle(frame, coords, 10, color, 1)

	return frame


if __name__ == "__main__":
	typer.run(draw_joints)

