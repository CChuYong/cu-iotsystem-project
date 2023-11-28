import RPi_I2C_driver
from time import *
import threading, store

break_flag = False
def initialize():
    print("Initializing lcd..")
    # Start Temp Thread Loop
    global lcd_thread
    lcd_thread = threading.Thread(target=_run_lcd)
    lcd_thread.start()
    
    # Initialize lcd
    global lcd
    lcd = RPi_I2C_driver.lcd(0x27)
    lcd.cursor()


def shutdown():
    break_flag = True
    lcd_thread.join()

def _run_lcd():
    while True:
        time.sleep(2.5)
        lcd.print("Hello")
        global break_flag
        if break_flag:
            break


    