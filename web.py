from flask import Flask, jsonify
import threading, store

app = Flask(__name__)

@app.get('/status')
def status():
    summary = store.create_summary()
    print(summary)
    return jsonify(summary)

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