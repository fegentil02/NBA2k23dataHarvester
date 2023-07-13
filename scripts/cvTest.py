from PIL import ImageGrab
import cv2 as cv
import numpy as np



while True:
    screen = np.array(ImageGrab.grab(bbox=(0,0,800,600)))
    screen = cv.cvtColor(screen, cv.COLOR_RGB2HSV)#Color detection with HSV values
    screen = cv.dilate(screen,np.ones((5, 5), np.uint8))
    lower_red = np.array([160,100,20])
    upper_red = np.array([179,255,255])
    mask = cv.inRange(screen, lower_red, upper_red)
    result = cv.bitwise_and(screen, screen, mask = mask)
    canny = cv.Canny(result, 50, 150)
    contours, hierarchy= cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    aproxContours = []
    for i in contours:
        aproxContours.append(cv.approxPolyDP(i, 10, False))
    cv.drawContours(result, aproxContours, -1, (0, 255, 0), 3)
    cv.imshow('Python Window',result)

    if cv.waitKey(25) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break

