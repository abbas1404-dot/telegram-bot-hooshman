import os
from flask import Flask, request
import requests

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

main_keyboard = {
    "inline_keyboard": [
        [{"text": "📚 دوره‌های فعال", "callback_data": "courses"}],
        [{"text": "📝 میخواهم ثبت نام کنم", "url": "https://t.me/hooshman_support"}],
        [{"text": "🎓 دریافت گواهینامه", "callback_data": "cert"}],
        [{"text": "🪪 دریافت کارت آزمون", "callback_data": "card"}],
        [{"text": "📊 تعرفه آزمون", "callback_data": "fee"}],
        [{"text": "📈 دهک من چند است؟", "callback_data": "decile"}],
        [{"text": "📖 نمونه سوالات", "callback_data": "samples"}],
        [{"text": "📞 پشتیبانی و مشاوره", "url": "https://t.me/hooshman_support"}],
        [{"text": "🌐 وبسایت آموزشگاه", "url": "https://hooshmaniran.ir/"}]
    ]
}

list_button_kb = {"inline_keyboard": [[{"text": "📊 نمایش لیست", "callback_data": "show_list"}]]}

def make_double_column_with_list(buttons):
    k = []
    for i in range(0, len(buttons), 2):
        k.append(buttons[i:i+2])
    k.append([{"text": "📊 نمایش لیست", "callback_data": "show_list"}])
    return {"inline_keyboard": k}

course_buttons = [
    {"text": "💻 مهارت‌های کامپیوتر", "callback_data": "c_comp"},
    {"text": "🎨 گرافیک دیزاین", "callback_data": "c_graph"},
    {"text": "🧩 برنامه‌نویسی", "callback_data": "c_prog"},
    {"text": "🤖 هوش مصنوعی", "callback_data": "c_ai"},
    {"text": "📢 تولید محتوا", "callback_data": "c_cont"},
    {"text": "🌐 طراحی سایت", "callback_data": "c_web"},
    {"text": "🔒 شبکه و امنیت", "callback_data": "c_net"},
    {"text": "📐 معماری و مهندسی", "callback_data": "c_eng"},
    {"text": "🎨 هنرهای تجسمی", "callback_data": "c_art"}
]

courses_kb = make_double_column_with_list(course_buttons)

WELCOME_TEXT = "سلام و درود 🌸\nبه **آکادمی تخصصی هوشمان** خوش آمدید —\nجایی که *یادگیری* با *هوشمندی* همراه می‌شود! 🧠✨"

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if data is None:
            return "No data", 400

        if "message" in data and data["message"].get("text") == "/start":
            chat_id = data["message"]["chat"]["id"]
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": WELCOME_TEXT,
                    "reply_markup": main_keyboard,
                    "parse_mode": "Markdown"
                }
            )
            return "OK", 200

        if "message" in data and "text" in data["message"]:
            text = data["message"]["text"].strip().lower()
            chat_id = data["message"]["chat"]["id"]
            if "لیست" in text or "menu" in text or "منو" in text:
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "📋 منوی خدمات:",
                        "reply_markup": main_keyboard,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

        if "callback_query" in 
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            callback_data = query["data"]

            requests.post(
                f"{TELEGRAM_API}/answerCallbackQuery",
                json={"callback_query_id": query["id"]}
            )

            if callback_data == "show_list":
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "📋 لیست خدمات آکادمی هوشمان:",
                        "reply_markup": main_keyboard,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

            if callback_data == "courses":
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "📚 لطفاً یکی از دوره‌های زیر را انتخاب کنید:",
                        "reply_markup": courses_kb,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

            elif callback_data.startswith("c_"):
                names = {
                    "c_comp": "مهارت‌های کامپیوتر",
                    "c_graph": "گرافیک دیزاین",
                    "c_prog": "برنامه‌نویسی",
                    "c_ai": "هوش مصنوعی",
                    "c_cont": "تولید محتوا",
                    "c_web": "طراحی سایت",
                    "c_net": "شبکه و امنیت",
                    "c_eng": "معماری و مهندسی",
                    "c_art": "هنرهای تجسمی"
                }
                name = names.get(callback_data, "این دوره")
                text = f"✅ اطلاعات {name}:\nدر حال آماده‌سازی جزئیات.\n\n👇 برای بازگشت، روی \"نمایش لیست\" کلیک کنید."
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "reply_markup": list_button_kb,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

            responses = {
                "cert": "🎓 *دریافت گواهینامه*\nگواهینامه معتبر *وزارت کار* صادر می‌شود.\n\n👇 برای بازگشت، روی \"نمایش لیست\" کلیک کنید.",
                "card": "🪪 *دریافت کارت آزمون*\nارسال ۲۴ ساعت قبل از آزمون.\n\n👇 برای بازگشت، روی \"نمایش لیست\" کلیک کنید.",
                "fee": "📊 *تعرفه آزمون*\n• آزمون اصلی: رایگان\n• آزمون آزمایشی: ۲۵۰,۰۰۰ تومان\n\n👇 برای بازگشت، روی \"نمایش لیست\" کلیک کنید.",
                "decile": "📈 *دهک من چند است؟*\nبر اساس رتبهٔ شما محاسبه می‌شود.\n\n👇 برای بازگشت، روی \"نمایش لیست\" کلیک کنید.",
                "samples": "📖 *نمونه سوالات*\nدر [وبسایت ما](https://hooshmaniran.ir/samples) قابل دانلود است.\n\n👇 برای بازگشت، روی \"نمایش لیست\" کلیک کنید."
            }

            text = responses.get(callback_data)
            if text:
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "reply_markup": list_button_kb,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

        return "Ignored", 200

    except Exception as e:
        print("❌ Error:", str(e))
        return "Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
