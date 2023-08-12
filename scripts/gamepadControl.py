import vgamepad as vg
import time
import keyboard

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
    def pumpfake(self):#Taps the x button, makes the player do a pumpfake
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
        time.sleep(0.11)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
        time.sleep(0.2) 

def main():
    print("Testing joystick")
    gamepad = controller()
    keyboard.wait('enter')
    gamepad.pumpfake()
    while True:
        time.sleep(1)
    
    
if __name__ == "__main__":
    main()