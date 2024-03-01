# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2

def find_marker(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	return cv2.minAreaRect(c)

KNOWN_DISTANCE = 21.0
KNOWN_WIDTH = 6.0

image = cv2.imread("Source.jpg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

def distance_to_camera(knownWidth, focalLength, perWidth):
	return (knownWidth * focalLength) / perWidth

def calculate_distance(width):
    distance = distance_to_camera(KNOWN_WIDTH, focalLength, width)
    return distance
