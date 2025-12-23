import math

# I want to input the coordinates of the elbow, wrist, and shoulder
# Outputs the angle of those coordinates.

def distance(x1, y1, x2, y2):
	return ((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 1/2)

def calculate_elbow(wrist, elbow, shoulder):
	x_wrist = wrist.x
	y_wrist = wrist.y
	x_elbow = elbow.x
	y_elbow = elbow.y
	x_shoulder = shoulder.x
	y_shoulder = shoulder.y

	a = distance(x_shoulder, y_shoulder, x_elbow, y_elbow)
	b = distance(x_elbow, y_elbow, x_wrist, y_wrist)
	c = distance(x_shoulder, y_shoulder, x_wrist, y_wrist)

	cosC = (a**2 + b**2 - c**2) / (2 * a * b)
	angle = math.acos(max(-1.0, min(1.0, cosC)))

	return angle





