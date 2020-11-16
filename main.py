import cv2
import numpy as np
import random


# todo: add oriantation chacking for the square
# todo: check if both sides are +- equal

threshEmpty = 0.03


def extract_digit(cell):
    thresh = cv2.adaptiveThreshold(cell, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return None

    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    h, w = thresh.shape
    percent_filled = cv2.countNonZero(mask) / float(w * h)

    if percent_filled < threshEmpty:
        return None

    digit = cv2.bitwise_and(thresh, thresh, mask=mask)

    return digit


# def pre_process(img):
#     imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
#     imgCanny = cv2.Canny(imgBlur, 200, 200)
#     kernel = np.ones((5, 5))
#     imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
#     imgThres = cv2.erode(imgDial, kernel, iterations=1)
#     return imgThres


cam = cv2.VideoCapture(0)
cam.set(3, 1920)
cam.set(4, 1080)

imgOutput = 0
imgCropped = 0

numbers = np.zeros((9, 9))

frame_tres = 10

while True:
    _, img = cam.read()

    imgContour = img.copy()

    blank = np.zeros_like(img)

    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)

    #########################################################################################################

    contures, hiearchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contures:
        area = cv2.contourArea(cnt)
        if area > 50000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            perimiter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimiter, True)
            width, height = 450, 450
            if len(approx) == 4:
                pts1 = np.float32([approx[0], approx[3], approx[1], approx[2]])
                pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                imgOutput = cv2.warpPerspective(imgBlur, matrix, (width, height))

                for i in range(9):
                    for j in range(9):
                        imgCropped = imgOutput[j*50+frame_tres:j*50+50-frame_tres, i*50+frame_tres:i*50+50-frame_tres]
                        dgt = extract_digit(imgCropped)
                        if dgt is None:
                            numbers[j][i] = 0
                        else:
                            numbers[j][i] = 1

                        if random.randint(1, 100) > 80:
                            cv2.imshow("test", imgCropped)
    #############################################################################################################

    cv2.imshow("Original", img)
    # cv2.imshow("Canny", imgCanny)
    cv2.imshow("Output", imgOutput)
    cv2.imshow("Cropped", imgCropped)
    # cv2.imshow("blank", blank)
    cv2.imshow("Countours", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(numbers)
        break
