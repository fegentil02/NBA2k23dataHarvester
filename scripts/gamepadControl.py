import vgamepad as vg
import time

def gamepadInit():
    gamepad = vg.VX360Gamepad()
    gamepad.reset()
    return gamepad

def shoot(gamepad, delay):#Presses x, holds for x amount of time, releases
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(delay)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    
def ballReset(gamepad):#Presses and releases the A button, makes teamates give you a new ball
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(1)
    

def main():
    print("Testing joystick")
    gamepad = vg.VX360Gamepad()
    gamepad.reset()
    while(True):
        ballReset(gamepad)
    
    
    
if __name__ == "__main__":
    main()