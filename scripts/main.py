import audioRec
import Fingerprint
import gamepadControl
import time
import os
import keyboard
import visual
import numpy as np


def netChecker():
    time.sleep(0.8)
    audioRec.stream()# Scale recording duration with the distance from the net
    make1 = Fingerprint.fingerprint('make1.wav')
    make2 = Fingerprint.fingerprint('make2.wav')
    test = Fingerprint.fingerprint('temp.wav')
    
    compare1 = Fingerprint.compare(make1, test)
    compare2 = Fingerprint.compare(make2, test)
    
    os.remove("temp.wav")
    return compare1 > 90 or  compare2 > 90 or compare1 + compare2 > 120

def moveTo(desiredPOS, gamepad, range = 5 ):
    currentPOS, zero, centerEstimate = visual.estimatePOS([0,0], [0,0])
    distanceX = desiredPOS[0] - currentPOS[0] 
    distanceY = desiredPOS[1] - currentPOS[1] 
    while np.abs(distanceX) > range or np.abs(distanceY) > range:
        print(distanceX, distanceY)
        if distanceX > 2*range:
            x_value = 0.5
        elif distanceX > range:
            x_value = 0.1
        elif distanceX < -2*range:
            x_value = -0.5
        elif distanceX < -range:
            x_value = -0.1
        else:
            x_value = 0.0
        if distanceY > 2*range:
            y_value = -0.5
        elif distanceY > range:
            y_value = -0.1
        elif distanceY < -2*range:
            y_value = 0.5
        elif distanceY < -range:
            y_value = 0.1
        else:
            y_value = 0.0
        
        gamepad.left_joystick_float(x_value,y_value)
        gamepad.update()
        currentPOS,zero,centerEstimate = visual.estimatePOS(zero, centerEstimate)
        distanceX = desiredPOS[0] - currentPOS[0]
        distanceY = desiredPOS[1] - currentPOS[1] 
    gamepad.left_joystick_float( 0.0, 0.0)
    gamepad.update()
    return


def main():
    
    gamepad = gamepadControl.gamepadInit()
    print('Press Enter to Start')
    keyboard.wait('enter')
    #gamepadControl.shoot(gamepad, 1)
    #print(netChecker())
    moveTo([112, 60], gamepad)

if __name__ == "__main__":
    main()
