import numpy as np
import cv2 as cv

def detect_shape(c):
    # Compute perimeter of contour and perform contour approximation
    shape = ""
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 6:
        shape = "hexagon"
    return shape

img = cv.imread('./4canny.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

kernel = np.ones((2,2), np.uint8)
opening_img = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel) 
blurred = cv.GaussianBlur(opening_img, (5, 5), 0)
thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

# canny = cv.Canny(blurred, 45, 120)
# canny = cv.Canny(thresh, 100, 200)
canny = cv.Canny(blurred, 10, 30)
# canny = cv.Canny(blurred, 30, 45)

# Find contours and detect shape
cnts = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    # Identify shape
    shape = detect_shape(c)

    # Find centroid and label shape name
    M = cv.moments(c)
    if (M["m00"] !=0):
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv.putText(img, shape, (cX - 20, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (36,0,255), 2)
        print(cX,cY)

cv.imshow('original', img)
cv.imshow('canny', canny)
cv.waitKey(0)