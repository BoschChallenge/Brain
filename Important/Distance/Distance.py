import imutils
import cv2

image = cv2.imread('Source.jpg')
KNOWN_DISTANCE = 21.0

class SignDistance:
	def __init__(self):
		self.KNOWN_WIDTH = 6.0
		marker = self.find_marker(image)
		self.focalLength = (marker[1][0] * KNOWN_DISTANCE) / self.KNOWN_WIDTH

	def find_marker(self,image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)
		edged = cv2.Canny(gray, 35, 125)
		cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key = cv2.contourArea)
		return cv2.minAreaRect(c)

	def distance_to_camera(self,knownWidth, focalLength, perWidth):
		return (knownWidth * focalLength) / perWidth

	def calculate_distance(self,width):
		distance = self.distance_to_camera(self.KNOWN_WIDTH, self.focalLength, width)
		return distance