import RPi.GPIO as GPIO
from common import RelayState, PowerState, FanCoilMode
import adafruit_dht as dht
import time
import threading
import database, store

temperature_pin_id = 0

#TODO: SAVE STATE with Database

# fancoil_mode = FanCoilMode.HEATER
# desired_temperature = 20.0
# last_read_temperature = 0.0

break_flag = False

def _handle_temp():
    while True:
        time.sleep(2.5)
        current_temp = _read_current_temperature()
        if current_temp > 0.0:
            store.current_temperature = current_temp
        global break_flag
        if break_flag:
            break


def initialize(pin):
    print("Initializing temp module...")
    global temperature_pin_id
    temperature_pin_id = pin

    global temp_sensor
    temp_sensor = dht.DHT11(temperature_pin_id)

    #Read Temperature Once
    _read_current_temperature()

    # Restore Temperature State
    store.desired_temp = database.read_desired_temp()

    # Start Temp Thread Loop
    global temp_thread
    temp_thread = threading.Thread(target=_handle_temp)
    temp_thread.start()

def shutdown():
    global break_flag
    break_flag = True

def _read_current_temperature():
    try:
        t = temp_sensor.temperature
        if t is None or t <= 0.0:
            print("Cannot read tempreature")
            return 0.0
        return t
    except:
        return 0.0

def set_desired_temp(temp):
    if temp >= 0.0 and temp <= 50.0:
        store.desired_temperature = temp

def evaluate_state():
    if store.fancoil_mode == FanCoilMode.HEATER:
        if store.current_temperature >= store.desired_temp:
            return RelayState.DISABLED
        else:
            return RelayState.ENABLED
    else:
        if store.current_temperature <= store.desired_temp:
            return RelayState.DISABLED
        else:
            return RelayState.ENABLED
    