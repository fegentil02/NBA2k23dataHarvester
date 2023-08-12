from PIL import ImageGrab
import cv2 as cv
import numpy as np


lower_purple = np.array([135,150,0])
upper_purple = np.array([165,255,255])



def main():
    test = visual(courtColor= 'Green')
    while True:
        currentPOS, zero, centerEstimate = test.estimatePOS([0,0], [0,0])
        print(currentPOS)

class visual():
    def __init__(self, screenSize = [1920, 1800], courtColor = 'Blue', lower_court = np.array([100,150,0]), upper_court = np.array([140,255,255]) ) -> None:
        self.screenSize = screenSize
        self.lower_court = lower_court
        self.upper_court = upper_court
        match courtColor:
            case 'Blue':
                self.lower_court = np.array([100,150,0])
                self.upper_court = np.array([140,255,255])
            case 'Black':
                self.lower_court = np.array([0,0,0])
                self.upper_court = np.array([180, 255, 35])
            case 'Yellow':
                self.lower_court = np.array([20, 100, 100])
                self.upper_court = np.array([30, 255, 255])
            case 'Red':
                self.lower_court = np.array([0, 70, 50])
                self.upper_court = np.array([10, 255, 255])
            case 'Green':
                self.lower_court = np.array([36, 25, 25])
                self.upper_court = np.array([86, 255, 255])
          

    def estimatePOS(self, zero, centerEstimate):
        playerPos = [0,0]
        screen = np.array(ImageGrab.grab(bbox=(0,0,self.screenSize[0],self.screenSize[1])))
        hsv = cv.cvtColor(screen, cv.COLOR_RGB2HSV)#Color detection with HSV values
        
        
        result0, newZero = self.zeroFinder(hsv)
        result1, newCenterEstimate = self.playerFinder(hsv)
        if result0 and result1:
            zero = [self.posFilter(zero[0], newZero[0]), self.posFilter(zero[1], newZero[1])]
            centerEstimate = [self.posFilter(centerEstimate[0], newCenterEstimate[0]), self.posFilter(centerEstimate[1], newCenterEstimate[1])]
            playerPos = [(centerEstimate[0]- zero[0])*256/self.screenSize[0], (centerEstimate[1] - zero[1])*256/self.screenSize[1]]
            
        return playerPos, zero, centerEstimate

    def posFilter(self, oldPos, newPos): # Stabilizes pos results
        return 0.7*newPos + 0.4*oldPos   

    def playerFinder(self, hsv): # Estimates player position
        erode = cv.erode(hsv,np.ones((3, 3), np.uint8 ))
        mask = cv.inRange(erode, lower_purple, upper_purple)
        result = cv.bitwise_and(hsv, hsv, mask = mask)
 
    
        canny = cv.Canny(result, 50, 150)
        contours, hierarchy= cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        aproxContours = []
        avgX = 0
        avgY = 0
        avgCounter = 0
        for i in contours:     
                aprox = cv.approxPolyDP(i, 3, False)
                if len(aprox) >= 3:
                    aproxContours.append(aprox)
                    for j in aprox:
                        avgX += j[0][0]
                        avgY += j[0][1]
                        avgCounter += 1
        if avgCounter > 0:
            centerEstimate = [avgX//avgCounter, avgY//avgCounter]    
            return True, centerEstimate
        else:
            return False, [0,0]
    

    def zeroFinder(self, hsv):#Finds court corner, will be used to locate player with x,y coords
        hsv = cv.dilate(hsv,np.ones((5, 5), np.uint8))
        mask = cv.inRange(hsv, self.lower_court, self.upper_court)
        result = cv.bitwise_and(hsv, hsv, mask = mask)
        canny = cv.Canny(result, 50, 150)
        contours, hierarchy= cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
        aproxContours = []
        for i in contours:     
                aprox = cv.approxPolyDP(i, 10, False)
                if len(aprox) > 4 and aprox[0][0][1] < self.screenSize[1]//7.2 :
                    aproxContours.append(aprox)
        if len(aproxContours) > 0:
            minIndexix = 0
            minIndexjx = 0
            minIndexiy = 0
            minIndexjy = 0
            for i in range(len(aproxContours)):
                for j in range(len(aproxContours[i])):
                    if aproxContours[minIndexix][minIndexjx][0][0] >= aproxContours[i][j][0][0]:
                        minIndexix = i
                        minIndexjx = j
                    if aproxContours[minIndexiy][minIndexjy][0][1] >= aproxContours[i][j][0][1]:
                        minIndexiy = i
                        minIndexjy = j
    
            return True, [aproxContours[minIndexix][minIndexjx][0][0], aproxContours[minIndexiy][minIndexjy][0][1]]
        else: 
            return False, [0,0]
    
if __name__ == "__main__":
    main()
