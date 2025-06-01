import threading
import time
import requests
from telegram import Bot

# ✅ Dein Telegram Bot Token
bot = Bot(token='7956426656:AAH5o_reU2KNE-rCUQXPLCh-qt-YeC-yLoU')

# 🟢 SuiVision API-Endpunkt (kein Key nötig!)
API_URL_TEMPLATE = "https://api.suivision.io/v1/account/{address}/txs"

tracked_wallets = {}

def start_tracking(address, chat_id):
    if address not in tracked_wallets:
        tracked_wallets[address] = {
            'chat_id': chat_id,
            'last_tx': None
        }
        thread = threading.Thread(target=watch_wallet, args=(address,))
        thread.daemon = True
        thread.start()
        print(f"[INFO] Tracking gestartet für {address}")

def watch_wallet(address):
    while True:
        activities = get_wallet_activities(address)
        if not activities:
            print(f"[DEBUG] Keine neuen Aktivitäten für {address}")
            time.sleep(10)
            continue

        for tx in activities:
            tx_hash = tx.get("txDigest")
            if not tx_hash:
                continue

            # Testmodus: immer senden
            print(f"[INFO] Neue Aktivität erkannt: {tx_hash}")
            if is_swap(tx):
                info = extract_info(tx)
                bot.send_message(chat_id=tracked_wallets[address]['chat_id'], text=format_info(info))
            else:
                print(f"[DEBUG] Keine Swap-Transaktion: {tx_hash}")

        time.sleep(10)

def get_wallet_activities(address):
    try:
        url = API_URL_TEMPLATE.format(address=address)
        response = requests.get(url)
        print(f"[DEBUG] API Response: {response.status_code}")
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print(f"[ERROR] SuiVision API Fehler: {response.text}")
    except Exception as e:
        print(f"[ERROR] Netzwerkfehler: {e}")
    return []

def is_swap(tx):
    try:
        kinds = tx.get("transaction", {}).get("kind", "")
        lower = str(kinds).lower()
        return any(kw in lower for kw in ["swap", "cetus", "deepbook", "turbos", "kriya", "flowx", "aftermath"])
    except:
        return False

def extract_info(tx):
    return {
        "digest": tx.get("txDigest", "unbekannt"),
        "timestamp": tx.get("timestampMs", "unbekannt"),
        "sender": tx.get("sender", "unbekannt"),
        "status": tx.get("effects", {}).get("status", {}).get("status", "unbekannt")
    }

def format_info(info):
    return (
        f"🔍 *Swap erkannt!*\n\n"
        f"🔗 TX Hash: `{info['digest']}`\n"
        f"📤 Sender: `{info['sender']}`\n"
        f"🕒 Timestamp: {info['timestamp']}\n"
        f"✅ Status: {info['status']}"
    )
