print("[BOOT] Bot.py wird gestartet...")

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from wallet_tracker import start_tracking

# 🔐 Deinen echten Telegram-Bot-Token hier einfügen
TOKEN = '7038474937:AAGfnFd_N1jv8VVBsq_Xd97bULn34mfiu0U'

# 📩 Begrüßung bei /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Willkommen bei SuiTracker!\n\n"
        "Sende mir einfach eine gültige Sui-Wallet-Adresse (z. B. beginnend mit 0x),\n"
        "und ich werde sie für dich überwachen.\n"
        "Du bekommst automatisch eine Nachricht, sobald dort ein Kauf erkannt wird."
    )

# 🧾 Wallet-Adressen empfangen und verarbeiten
async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()

    if address.startswith("0x") and len(address) == 66:
        await update.message.reply_text(f"✅ Wallet {address} wird jetzt überwacht.")
        print(f"[INFO] Neue Wallet registriert: {address} für Chat-ID {update.message.chat_id}")
        start_tracking(address, update.message.chat_id)
    else:
        await update.message.reply_text("❌ Ungültige Adresse. Sie muss mit '0x' beginnen und 66 Zeichen lang sein.")

# 🚀 Hauptfunktion
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_wallet))

    print("[INFO] Bot gestartet. Warte auf Nachrichten...")
    app.run_polling()

# 🔁 Startpunkt
if __name__ == '__main__':
    main()
