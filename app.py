from flask import Flask, jsonify
import random, time, threading
from datetime import datetime

app = Flask(__name__)

last_signal = {"pair": "Starting...", "action": "ANALYZING", "time": datetime.now().strftime("%H:%M:%S")}

def get_best_signal():
    trend = random.choice(["UP", "DOWN"])
    if trend == "UP":
        return "BUY"
    else:
        return "SELL"

def generate_signals():
    global last_signal
    while True:
        action = get_best_signal()
        pair = random.choice(["EUR/USD OTC", "USD/INR OTC", "GBP/USD OTC"])
        last_signal = {
            "pair": pair,
            "action": action,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        print(f"NEW SIGNAL {last_signal}")
        time.sleep(90)

@app.route('/')
def home():
    return f"Bot Running - {last_signal}"

@app.route('/last-signal')
def get_signal():
    return jsonify(last_signal)

threading.Thread(target=generate_signals, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
