import RPi.GPIO as GPIO
import time
import temp, database
from common import RelayState, PowerState

# SENSOR PINS
TEMP_SENSOR_PIN_ID, IR_SENSOR_PIN_ID = 2, 3

# LED/BUZZER PINS
RED_LED_PIN_ID, BUZZER_PIN_ID = 4, 5

# LCD
LCD_SDA_PIN_ID, LCD_SCL_PIN_ID = 6, 7

# MAIN RELAY PINS
V220_RELAY_PIN_ID = 10


# SETUP PINS
GPIO.setmode(GPIO.BCM)
GPIO.setup(V220_RELAY_PIN_ID, GPIO.OUT)

current_relay_state = RelayState.DISABLED
current_power_state = PowerState.OFF
system_active = True

print("Initializing Modules...")
database.initialize()
temp.initialize(TEMP_SENSOR_PIN_ID)

def evaluate_next_state():
    temp_state = temp.evaluate_next_state()
    return temp_state

def gracefully_shutdown():
    global system_active
    system_active = False
    print("Gracefully Shutting Down System...")
    database.shutdown()
    temp.shutdown()
    print("Releasing Relay Output...")
    GPIO.output(V220_RELAY_PIN_ID, False)
    time.sleep(1)
    print("Clean up GPIO...")
    GPIO.cleanup()
    time.sleep(1)

print("Initializing Modules Completed!")

try:
    while system_active:
        if current_power_state == PowerState.ON:
            GPIO.output(V220_RELAY_PIN_ID, current_relay_state)
            current_relay_state = evaluate_next_state()
        else:
            GPIO.output(V220_RELAY_PIN_ID, False)
        
        print("relay=%s, power=%s, temp=%f, desired_temp=%f"%(current_relay_state, current_power_state, temp.get_current_temperature(), temp.get_desired_temp()))
        time.sleep(0.5) #Loop Ticker
except KeyboardInterrupt:
    gracefully_shutdown()