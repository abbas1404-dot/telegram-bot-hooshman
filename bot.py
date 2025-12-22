import os
from flask import Flask, request
import requests
import json

# 🔑 توکن
TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# 🎛 کیبورد (به صورت دیکشنری ساده)
keyboard = {
    "inline_keyboard": [
        [{"text": "📝 توضیحات آزمون", "callback_data": "exam"}],
        [{"text": "🎓 مدارک و گواهینامه‌ها", "callback_data": "cert"}],
        [{"text": "💰 شهریه", "callback_data": "price"}],
        [{"text": "🪪 کارت ورود به جلسه", "callback_data": "card"}]
    ]
}

# 📡 پیام شروع
START_TEXT = (
    "سلام و عرض ادب 🌸\n\n"
    "به *آکادمی تخصصی هوشمان* خوش آمدید 👋\n"
    "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
)

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not 
            return "No data", 400

        # ✅ /start
        if "message" in data and data["message"].get("text") == "/start":
            chat_id = data["message"]["chat"]["id"]
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": START_TEXT,
                    "reply_markup": keyboard,
                    "parse_mode": "Markdown"
                }
            )
            return "OK", 200

        # ✅ کلیک دکمه
        if "callback_query" in 
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            callback_data = query["data"]

            # تأیید فوری کلیک (حذف loading)
            requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": query["id"]})

            if callback_data == "exam":
                # ارسال دوباره پیام اصلی
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": START_TEXT,
                        "reply_markup": keyboard,
                        "parse_mode": "Markdown"
                    }
                )
            elif callback_data == "cert":
                requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": "🎓 پس از پایان دوره، گواهینامه معتبر ارائه می‌شود."})
            elif callback_data == "price":
                requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": "💰 شهریه دوره‌ها به‌صورت نقد و اقساط قابل پرداخت است."})
            elif callback_data == "card":
                requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": "🪪 کارت ورود به جلسه ۲۴ ساعت قبل از آزمون صادر می‌شود."})
            else:
                requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": "⚠️ گزینه نامعتبر است."})

            return "OK", 200

        return "Ignored", 200

    except Exception as e:
        print("❌ Error:", str(e))
        return "Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
