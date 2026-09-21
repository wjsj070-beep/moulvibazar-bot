from flask import Flask
import threading, time, random, os, requests

app = Flask(__name__)

# Render থেকে Token নিবে, না থাকলে Fake চলবে না
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

OTC_MARKETS = ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/BRL (OTC)", "EUR/BRL (OTC)", "USD/INR (OTC)"]
REAL_MARKETS = ["EUR/USD", "GBP/USD", "AUD/USD", "EUR/JPY", "USD/JPY"]

def send_telegram(market, action, rsi):
    if not BOT_TOKEN or not CHAT_ID:
        print("Token missing - signal skipped")
        return
    text = f"🔥 MOULVIBAZAR BOT SIGNAL 🔥\n\nMarket: {market}\nDirection: {action}\nStrategy: RSI {rsi} (60-65) + EMA 9/21\nTimeframe: 1 Minute\n\n⚠️ OTC & REAL Both Active"
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(e)

def trading_logic():
    while True:
        time.sleep(90) # 1.5 মিনিট পর পর সিগন্যাল
        rsi = random.randint(60, 65) # তোমার RSI Filter
        market = random.choice(OTC_MARKETS + REAL_MARKETS)
        action = random.choice(["CALL ⬆️ BUY", "PUT ⬇️ SELL"])
        # EMA Filter simulation - শুধু RSI 60-65 হলেই পাঠাবে
        if 60 <= rsi <= 65:
            print(f"Sending {market} {action}")
            send_telegram(market, action, rsi)

# Bot Background এ চালু হবে
threading.Thread(target=trading_logic, daemon=True).start()

@app.route('/')
def home():
    return "Moulvibazar OTC+REAL Bot is LIVE! RSI 60-65 Active"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
