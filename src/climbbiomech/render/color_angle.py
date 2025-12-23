import math
import colorsys

def get_color(angle):
	t = max(0.0, min(1.0, angle / math.pi))
	hue = (1.0 - t) * 0.0 + t * (240.0 / 360.0)

	r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
	color = [int(255 * r), int(255 * g), int(255 * b)]

	return color