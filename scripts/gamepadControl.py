import vgamepad as vg
import time


class controller():
    def __init__(self) -> None:
        
        self.gamepad = vg.VX360Gamepad()
        self.gamepad.reset()

    def shoot(self, delay):#Presses x, holds for x amount of time, releases
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
        time.sleep(delay)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
    
    def ballReset(self):#Presses and releases the A button, makes teamates give you a new ball
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(1)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(1)
    

def main():
    print("Testing joystick")
    gamepad = controller()
    controller.gamepad.reset()
    while(True):
        controller.ballReset()
    
    
    
if __name__ == "__main__":
    main()