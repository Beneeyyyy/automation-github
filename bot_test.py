import os
import telebot

# Ambil token dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise SystemExit("❌ BOT_TOKEN belum diisi")

# Masukkan Telegram User ID kamu di sini
# Contoh: ADMIN_IDS = [123456789]
ADMIN_IDS = []

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 Bot aktif!\n\n"
        "Perintah yang tersedia:\n"
        "/ping - cek koneksi bot\n"
        "/id - melihat Telegram User ID kamu"
    )


@bot.message_handler(commands=["ping"])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Bot berjalan dengan baik.")


@bot.message_handler(commands=["id"])
def get_id(message):
    user = message.from_user

    bot.reply_to(
        message,
        f"Telegram User ID kamu: {user.id}\n"
        f"Username: @{user.username if user.username else '-'}"
    )


print("🤖 Bot test sedang berjalan...")
print("Tekan CTRL+C untuk menghentikan.")

bot.infinity_polling()

