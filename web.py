from flask import Flask, jsonify, request
import threading, store
from common import RelayState, PowerState, FanCoilMode


app = Flask(__name__)

@app.get('/status')
def status():
    return jsonify(store.create_summary())

@app.post('/control/on')
def turnOn():
    store.current_power_state = PowerState.ON
    return jsonify(store.create_summary())

@app.post('/control/off')
def turnOff():
    store.current_power_state = PowerState.OFF
    return jsonify(store.create_summary())

@app.post('/control/heater')
def heater():
    store.fancoil_mode = FanCoilMode.HEATER
    return jsonify(store.create_summary())

@app.post('/control/ac')
def aircon():
    store.fancoil_mode = FanCoilMode.AIRCONDITIONER
    return jsonify(store.create_summary())

@app.post('/control/temp')
def temp():
    in_temp = int(request.args.get("temp"))
    if in_temp > 0 and in_temp < 50:
        store.desired_temp = in_temp
    return jsonify(store.create_summary())

def initialize():
    print("Initializing web..")
    # Start Temp Thread Loop
    global web_thread
    web_thread = threading.Thread(target=_run_web)
    web_thread.start()

def shutdown():
    web_thread.join()

def _run_web():
    print("Start Flask Application")
    app.run(host='0.0.0.0', port=8888)