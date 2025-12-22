import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیمات
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 8080))

# کیبورد
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 توضیحات آزمون", callback_data="exam")],
    [InlineKeyboardButton("🎓 مدارک و گواهینامه‌ها", callback_data="cert")],
    [InlineKeyboardButton("💰 شهریه", callback_data="price")],
    [InlineKeyboardButton("🪪 کارت ورود به جلسه", callback_data="card")]
])

# هندلرها
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

# ساخت ربات (بدون اجرای خودکار)
bot_app = Application.builder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))

# راه‌اندازی async loop — فقط یک بار
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot_app.updater = None  # جلوگیری از polling
bot_app.bot_data  # برای اطمینان از init

# Flask
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        json_data = request.get_json()
        if json_data:
            update = Update.de_json(json_data, bot_app.bot)
            loop.run_until_complete(bot_app.process_update(update))
            return "OK", 200
    return "Bad Request", 400

if __name__ == "__main__":
    print(f"✅ Server starting on port {PORT}")
    print(f"📡 Webhook URL should be: https://f71671be-f173-4d32-8178-ed8a8fe1e1e5.up.railway.app/{TOKEN}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
