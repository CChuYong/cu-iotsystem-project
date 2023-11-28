import RPi.GPIO as GPIO
import time
import temp, database, web, store, lcd
from common import RelayState, PowerState

# SENSOR PINS
TEMP_SENSOR_PIN_ID, IR_SENSOR_PIN_ID = 4, 18

# LED/BUZZER PINS
RED_LED_PIN_ID, BUZZER_PIN_ID = 24, 23

# LCD
LCD_SDA_PIN_ID, LCD_SCL_PIN_ID = 2, 3

# MAIN RELAY PINS
V220_RELAY_PIN_ID = 17


# SETUP PINS
GPIO.setmode(GPIO.BCM)
GPIO.setup(V220_RELAY_PIN_ID, GPIO.OUT)


system_active = True

print("Initializing Modules...")
database.initialize()
temp.initialize(TEMP_SENSOR_PIN_ID)
web.initialize()
lcd.initialize()


def evaluate_next_state():
    temp_state = temp.evaluate_state()
    return temp_state

def gracefully_shutdown():
    global system_active
    system_active = False
    print("Gracefully Shutting Down System...")
    database.shutdown()
    temp.shutdown()
    web.shutdown()
    lcd.shutdown()
    print("Releasing Relay...")
    GPIO.output(V220_RELAY_PIN_ID, False)
    time.sleep(1)
    print("Clean up GPIO...")
    GPIO.cleanup()
    time.sleep(1)

print("Initializing Modules Completed!")

try:
    while system_active:
        if store.current_power_state == PowerState.ON:
            GPIO.output(V220_RELAY_PIN_ID, store.current_relay_state.value)
            current_relay_state = evaluate_next_state()
        else:
            GPIO.output(V220_RELAY_PIN_ID, False)
        
        print("relay=%s, power=%s, temp=%f, desired_temp=%f"%(store.current_relay_state, store.current_power_state, store.current_temperature, store.desired_temp))
        time.sleep(0.5) #Loop Ticker
except KeyboardInterrupt:
    gracefully_shutdown()
