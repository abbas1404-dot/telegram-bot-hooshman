import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask

# 🔑 امنیت اول
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN is missing.")

# 🌐 ضروری برای webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # مثلاً: https://your-id.up.railway.app
if not WEBHOOK_URL:
    raise RuntimeError("❌ WEBHOOK_URL is missing (get it from Railway → Domains).")

PORT = int(os.getenv("PORT", 8000))

# 🎛 کیبورد
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 توضیحات آزمون", callback_data="exam")],
    [InlineKeyboardButton("🎓 مدارک و گواهینامه‌ها", callback_data="cert")],
    [InlineKeyboardButton("💰 شهریه", callback_data="price")],
    [InlineKeyboardButton("🪪 کارت ورود به جلسه", callback_data="card")]
])

# 📡 هندلرها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام و عرض ادب 🌸\nبه *آکادمی تخصصی هوشمان* خوش آمدید 👋\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    replies = {
        "exam": "📝 توضیحات کامل آزمون‌ها در این بخش قرار می‌گیرد.",
        "cert": "🎓 پس از پایان دوره، گواهینامه معتبر ارائه می‌شود.",
        "price": "💰 شهریه دوره‌ها به‌صورت نقد و اقساط قابل پرداخت است.",
        "card": "🪪 کارت ورود به جلسه ۲۴ ساعت قبل از آزمون صادر می‌شود."
    }
    await query.message.reply_text(replies.get(query.data, "⚠️ گزینه نامعتبر."))

# 🖥 Flask برای Railway (سبک‌تر و پایدارتر از aiohttp در این مورد)
app_flask = Flask(__name__)

@app_flask.route("/")
def health():
    return "OK", 200

# 🚀 راه‌اندازی ربات (همزمان با Flask)
def run_bot():
    print("🤖 Initializing bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # تنظیم webhook — فقط یک بار، قبل از شروع flask
    webhook_path = f"/webhook/{TOKEN}"
    full_url = WEBHOOK_URL + webhook_path
    print(f"📡 Setting webhook to: {full_url}")
    app.bot.set_webhook(url=full_url).wait()  # sync برای اطمینان
    
    print(f"✅ Starting webhook on port {PORT} (path: {webhook_path})")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"webhook/{TOKEN}",
        secret_token=None
    )

if __name__ == "__main__":
    # راه‌اندازی ربات در thread جداگانه
    from threading import Thread
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # راه‌اندازی Flask برای Railway
    print(f"✅ Flask health server starting on port {PORT} (/ → 'OK')")
    app_flask.run(host="0.0.0.0", port=PORT, threaded=True)
