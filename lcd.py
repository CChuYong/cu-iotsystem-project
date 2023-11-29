import RPi_I2C_driver
import time
import threading, store

break_flag = False
def initialize():
    print("Initializing lcd..")
    
    # Initialize lcd
    global lcd
    lcd = RPi_I2C_driver.lcd(0x27)
    #lcd.cursor()

    # Start Temp Thread Loop
    global lcd_thread
    lcd_thread = threading.Thread(target=_run_lcd)
    lcd_thread.start()


def shutdown():
    break_flag = True
    lcd_thread.join()

def _run_lcd():
    while True:
        lcd.home()
        curr_tmp_str = str(int(store.current_temperature))
        curr_dtr_str = str(int(store.desired_temp))
        lcd.print("Current Temp: " + curr_tmp_str)
        lcd.setCursor(0, 1)
        lcd.print("Desired Temp: " + curr_dtr_str)
        global break_flag
        if break_flag:
            break
        time.sleep(2.5)


    