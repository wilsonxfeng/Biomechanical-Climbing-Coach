from pathlib import Path
import cv2
import typer
import numpy
from climbbiomech.pose.landmark_enumeration import PoseLandmarks, ImportantLandmarks, BoneLandmarks
from climbbiomech.kinematics.elbow_angle import calculate_elbow
from climbbiomech.render.color_angle import get_color


def draw_joints(frame, result):

	if not result.pose_landmarks:
		return frame

	pose = result.pose_landmarks[0]
	H, W = frame.shape[0], frame.shape[1]
	color = [255, 255, 255]

	for joint in ImportantLandmarks:

		if PoseLandmarks[joint] == 14: # Right elbow
			wrist = pose[PoseLandmarks["RIGHT_WRIST"]]
			elbow = pose[PoseLandmarks["RIGHT_ELBOW"]]
			shoulder = pose[PoseLandmarks["RIGHT_SHOULDER"]]
			angle = calculate_elbow(wrist, elbow, shoulder)
			color = get_color(angle)

			if elbow.presence >= 0.5 and elbow.visibility >= 0.4:

				coords = [int(elbow.x * W), int(elbow.y * H)]

				cv2.circle(frame, coords, 10, color, 5)


		elif PoseLandmarks[joint] == 13: # Left Elbow
			wrist = pose[PoseLandmarks["LEFT_WRIST"]]
			elbow = pose[PoseLandmarks["LEFT_ELBOW"]]
			shoulder = pose[PoseLandmarks["LEFT_SHOULDER"]]
			angle = calculate_elbow(wrist, elbow, shoulder)

			color = get_color(angle)

			if elbow.presence >= 0.5 and elbow.visibility >= 0.4:

				coords = [int(elbow.x * W), int(elbow.y * H)]

				cv2.circle(frame, coords, 10, color, 5)

		elif PoseLandmarks[joint] == 26: # Right Knee
			hip = pose[PoseLandmarks["RIGHT_HIP"]]
			knee = pose[PoseLandmarks["RIGHT_KNEE"]]
			ankle = pose[PoseLandmarks["RIGHT_ANKLE"]]
			angle = calculate_elbow(hip, knee, ankle)

			color = get_color(angle)

			if knee.presence >= 0.5 and knee.visibility >= 0.4:

				coords = [int(knee.x * W), int(knee.y * H)]

				cv2.circle(frame, coords, 10, color, 5)

		elif PoseLandmarks[joint] == 25: # Left Knee
			hip = pose[PoseLandmarks["LEFT_HIP"]]
			knee = pose[PoseLandmarks["LEFT_KNEE"]]
			ankle = pose[PoseLandmarks["LEFT_ANKLE"]]
			angle = calculate_elbow(hip, knee, ankle)

			color = get_color(angle)

			if knee.presence >= 0.5 and knee.visibility >= 0.4:

				coords = [int(knee.x * W), int(knee.y * H)]

				cv2.circle(frame, coords, 10, color, 5)


		else:
			joint_info = pose[PoseLandmarks[joint]]
			x_px = int(joint_info.x * W)
			y_px = int(joint_info.y * H)

			if joint_info.presence >= 0.5:

				coords = [x_px, y_px]

				cv2.circle(frame, coords, 10, color, 5)

		color = [255, 255, 255]


	for bone in BoneLandmarks:

		start = pose[PoseLandmarks[bone[0]]]
		end = pose[PoseLandmarks[bone[1]]]

		if start.presence >= 0.5 and end.presence >= 0.5 and start.visibility >= 0.4 and end.visibility >= 0.4:

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

