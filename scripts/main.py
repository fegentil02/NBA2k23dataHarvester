import audioRec
import Fingerprint
import gamepadControl
import time
import os
import keyboard
import visual
import numpy as np
import csv
import ast


make1 = Fingerprint.fingerprint('audio\make1.wav')
make2 = Fingerprint.fingerprint('audio\make2.wav')

def netChecker():
    time.sleep(0.8)
    audioRec.stream()# Scale recording duration with the distance from the net
    
    test = Fingerprint.fingerprint('temp.wav')
    
    compare1 = Fingerprint.compare(make1, test)
    compare2 = Fingerprint.compare(make2, test)
    
    os.remove("temp.wav")
    return compare1 > 90 or  compare2 > 90 or compare1 + compare2 > 120

def moveTo(desiredPOS, gamepad, visual, range = 2):
    currentPOS, zero, centerEstimate = visual.estimatePOS([0,0], [0,0])
    distanceX = desiredPOS[0] - currentPOS[0] 
    distanceY = desiredPOS[1] - currentPOS[1] 
    correctCounter = 0
    while correctCounter <= 5:
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
        gamepad.gamepad.left_joystick_float(x_value,y_value)
        gamepad.gamepad.update()
        currentPOS,zero,centerEstimate = visual.estimatePOS(zero, centerEstimate)
        distanceX = desiredPOS[0] - currentPOS[0]
        distanceY = desiredPOS[1] - currentPOS[1] 
        if np.abs(distanceX) < range and np.abs(distanceY) < range:
            correctCounter += 1
    gamepad.gamepad.left_joystick_float( 0.0, 0.0)
    gamepad.gamepad.update()
    return

def attempt(gamepad, visual, PLAYERNAME,  desiredPOS, shootDelay):
    moveTo(desiredPOS, gamepad, visual)
    gamepad.shoot(shootDelay)
    success = netChecker()
    gamepad.ballReset()
    time.sleep(0.2)
    gamepad.ballReset()
    return {'Player Name': PLAYERNAME , 'Position': desiredPOS, 'Delay': shootDelay, 'Success': success}

def collectData(gamepad, visual, pos, PLAYERNAME, nAttempts, timing):# pos = List of Desired positions, nAttempts = max attempts integer, timing = [start delay, end delay, delay step]
    atCounter = 0
    currentDelay = timing[0]
    data = []
    for i in pos:
        while currentDelay <= timing[1]:
            while atCounter <= nAttempts:
                data.append(attempt(gamepad,visual, PLAYERNAME, i, currentDelay))
                if keyboard.is_pressed('Enter'):
                    return data
                atCounter += 1
            atCounter = 0
            currentDelay += timing[2]
        currentDelay = timing[0]
    return data

def main():
    #Grabs configs from CONFIG.txt
    config = open("CONFIG.txt", 'r')
    PLAYERNAME = (config.readline()).split("=")[1][:-1]
    SCREENSIZE = (config.readline()).split("=")[1][:-1]
    SCREENSIZE = ast.literal_eval(SCREENSIZE)
    DESIREDPOS = (config.readline()).split("=")[1][:-1]
    DESIREDPOS = ast.literal_eval(DESIREDPOS)
    INITIALDELAY = (config.readline()).split("=")[1][:-1]
    INITIALDELAY = ast.literal_eval(INITIALDELAY)
    FINALDELAY = (config.readline()).split("=")[1][:-1]
    FINALDELAY = ast.literal_eval(FINALDELAY)
    DELAYSTEP = (config.readline()).split("=")[1][:-1]
    DELAYSTEP = ast.literal_eval(DELAYSTEP)
    ATTEMPTNUM = (config.readline()).split("=")[1]
    ATTEMPTNUM = ast.literal_eval(ATTEMPTNUM)
    config.close()
    
    
    #Initializes controller and screengrabber
    gamepad = gamepadControl.controller()
    vis = visual.visual(SCREENSIZE)
    print('Press Enter to Start')
    keyboard.wait('enter')

    data = collectData(gamepad,vis,DESIREDPOS ,PLAYERNAME,  ATTEMPTNUM , [INITIALDELAY, FINALDELAY, DELAYSTEP])
    if os.path.isfile("data.csv") == False:
        with open('data.csv', 'a' ,newline='') as csvfile:
            fieldnames = ['Player Name' ,'Position' ,'Delay', 'Success']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for j in data:
                writer.writerow(j)
    else:
        with open('data.csv', 'a' ,newline='') as csvfile:
            fieldnames = ['Player Name' ,'Position' ,'Delay', 'Success']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for j in data:
                writer.writerow(j)
    

if __name__ == "__main__":
    main()
