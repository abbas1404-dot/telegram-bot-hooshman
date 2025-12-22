import os
from flask import Flask, request
import telegram
import json

# 🔑 توکن
TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# 🎛 کیبورد
keyboard = telegram.InlineKeyboardMarkup([
    [telegram.InlineKeyboardButton("📝 توضیحات آزمون", callback_data="exam")],
    [telegram.InlineKeyboardButton("🎓 مدارک و گواهینامه‌ها", callback_data="cert")],
    [telegram.InlineKeyboardButton("💰 شهریه", callback_data="price")],
    [telegram.InlineKeyboardButton("🪪 کارت ورود به جلسه", callback_data="card")]
])

# 📡 پیام شروع
START_TEXT = (
    "سلام و عرض ادب 🌸\n\n"
    "به *آکادمی تخصصی هوشمان* خوش آمدید 👋\n"
    "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
)

# 🖥 health check
@app.route("/")
def home():
    return "OK", 200

# 🔗 webhook endpoint — دقیقاً با توکن
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:  # ✅ اصلاح شده
            return "No data", 400

        # اگر پیام متنی بود (مثل /start)
        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"]["text"].strip()

            if text == "/start":
                bot.send_message(
                    chat_id=chat_id,
                    text=START_TEXT,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
                return "OK", 200

        # اگر کلیک روی دکمه بود
        if "callback_query" in data:  # ✅ اصلاح شده
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            callback_data = query["data"]

            # ✅ "exam" → ارسال دوباره پیام اصلی
            if callback_data == "exam":
                bot.send_message(
                    chat_id=chat_id,
                    text=START_TEXT,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            elif callback_data == "cert":
                bot.send_message(chat_id=chat_id, text="🎓 پس از پایان دوره، گواهینامه معتبر ارائه می‌شود.")
            elif callback_data == "price":
                bot.send_message(chat_id=chat_id, text="💰 شهریه دوره‌ها به‌صورت نقد و اقساط قابل پرداخت است.")
            elif callback_data == "card":
                bot.send_message(chat_id=chat_id, text="🪪 کارت ورود به جلسه ۲۴ ساعت قبل از آزمون صادر می‌شود.")
            else:
                bot.send_message(chat_id=chat_id, text="⚠️ گزینه نامعتبر است.")

            # تأیید کلیک (برای حذف loading در تلگرام)
            bot.answer_callback_query(callback_query_id=query["id"])

            return "OK", 200

        return "Ignored", 200

    except Exception as e:
        print("❌ Error:", str(e))
        return "Error", 500

# 🚀 راه‌اندازی
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
