import RPi.GPIO as GPIO
from common import RelayState, PowerState, FanCoilMode
import adafruit_dht as dht
import time
import threading
import database

temperature_pin_id = 0

#TODO: SAVE STATE with Database
fancoil_mode = FanCoilMode.HEATER
desired_temperature = 20.0

last_read_temperature = 0.0
break_flag = False

def _handle_temp():
    while True:
        time.sleep(2.5)
        current_temp = _read_current_temperature()
        if current_temp > 0.0:
            global last_read_temperature
            last_read_temperature = current_temp
        global break_flag
        if break_flag:
            break


def initialize(pin):
    global temperature_pin_id
    temperature_pin_id = pin

    global temp_sensor
    temp_sensor = dht.DHT11(temperature_pin_id)

    #Read Temperature Once
    _read_current_temperature()

    # Restore Temperature State
    global desired_temperature
    desired_temperature = database.read_desired_temp()

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
        global desired_temperature
        desired_temperature = temp

def get_desired_temp():
    global desired_temperature
    return desired_temperature

def get_current_temperature():
    global last_read_temperature
    return last_read_temperature 

def evaluate_state():
    if fancoil_mode == FanCoilMode.HEATER:
        if last_read_temperature >= desired_temperature:
            return RelayState.DISABLED
        else:
            return RelayState.ENABLED
    else:
        if last_read_temperature <= desired_temperature:
            return RelayState.DISABLED
        else:
            return RelayState.ENABLED
    