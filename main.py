import cv2
import numpy as np
import random

#todo: add oriantation chacking for the square
#todo: check if both sides are +- equal

def empty(x):
    pass



def pre_process(img):
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres

cam = cv2.VideoCapture(0)
cam.set(3, 1920)
cam.set(4, 1080)


imgOutput = 0
imgCropped = 0

numbers = np.zeros((9, 9))

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
                imgOutput = cv2.warpPerspective(img, matrix, (width, height))

                for i in range(9):
                    for j in range(9):
                        imgCropped = imgOutput[j*50:j*50+50, i*50:i*50+50]
                        numbers[i][j] = 1
                        if random.randint(1, 100) > 80:
                            cv2.imshow("test", imgCropped)
    #############################################################################################################


    cv2.imshow("Original", img)
    #cv2.imshow("Canny", imgCanny)
    cv2.imshow("Output", imgOutput)
    cv2.imshow("Cropped", imgCropped)
    #cv2.imshow("blank", blank)
    cv2.imshow("Countours", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
