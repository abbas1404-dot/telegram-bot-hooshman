import os
from flask import Flask, request
import requests

# ================== CONFIG ==================
TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# ================== KEYBOARDS ==================
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

list_button_kb = {
    "inline_keyboard": [
        [{"text": "📊 نمایش لیست", "callback_data": "show_list"}]
    ]
}

def make_two_column(buttons):
    kb = []
    for i in range(0, len(buttons), 2):
        kb.append(buttons[i:i + 2])
    kb.append([{"text": "📊 نمایش لیست", "callback_data": "show_list"}])
    return {"inline_keyboard": kb}

# ================== COURSES ==================
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

courses_kb = make_two_column(course_buttons)

COURSE_NAMES = {
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

# ================== DECILE ==================
decile_buttons = [
    {"text": "💻 مهارت‌های کامپیوتر", "callback_data": "d_comp"},
    {"text": "🎨 گرافیک دیزاین", "callback_data": "d_graph"},
    {"text": "🧩 برنامه‌نویسی", "callback_data": "d_prog"},
    {"text": "🤖 هوش مصنوعی", "callback_data": "d_ai"},
    {"text": "🌐 طراحی سایت", "callback_data": "d_web"},
    {"text": "🔒 شبکه و امنیت", "callback_data": "d_net"},
    {"text": "📐 معماری مهندسی", "callback_data": "d_eng"}
]

decile_kb = make_two_column(decile_buttons)

DECILE_NAMES = {
    "d_comp": "مهارت‌های کامپیوتر",
    "d_graph": "گرافیک دیزاین",
    "d_prog": "برنامه‌نویسی",
    "d_ai": "هوش مصنوعی",
    "d_web": "طراحی سایت",
    "d_net": "شبکه و امنیت",
    "d_eng": "معماری مهندسی"
}

# ================== TEXTS ==================
WELCOME_TEXT = (
    "سلام و درود 🌸\n"
    "به **آکادمی تخصصی هوشمان** خوش آمدید —\n"
    "جایی که *یادگیری* با *هوشمندی* همراه می‌شود! 🧠✨"
)

RESPONSES = {
    "cert": "🎓 *دریافت گواهینامه*\nگواهینامه معتبر وزارت کار صادر می‌شود.",
    "card": "🪪 *دریافت کارت آزمون*\n۲۴ ساعت قبل از آزمون ارسال می‌شود.",
    "fee": "📊 *تعرفه آزمون*\n• آزمون اصلی: رایگان\n• آزمون آزمایشی: ۲۵۰,۰۰۰ تومان",
    "samples": "📖 *نمونه سوالات*\nدر سایت hooshmaniran.ir قابل دانلود است."
}

# ================== ROUTES ==================
@app.route("/")
def home():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "No data", 400

    # /start
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

    # CALLBACKS
    if "callback_query" in data:
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
                    "text": "📋 منوی اصلی:",
                    "reply_markup": main_keyboard
                }
            )
            return "OK", 200

        if callback_data == "courses":
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "📚 یکی از دوره‌ها را انتخاب کنید:",
                    "reply_markup": courses_kb
                }
            )
            return "OK", 200

        if callback_data.startswith("c_"):
            name = COURSE_NAMES.get(callback_data, "این دوره")
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"ℹ️ اطلاعات {name} در حال آماده‌سازی است.",
                    "reply_markup": list_button_kb
                }
            )
            return "OK", 200

        if callback_data == "decile":
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "📈 رشته مورد نظر را انتخاب کنید:",
                    "reply_markup": decile_kb
                }
            )
            return "OK", 200

        if callback_data.startswith("d_"):
            field = DECILE_NAMES.get(callback_data, "این رشته")
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"📊 دهک شما در رشته «{field}» در حال بررسی است.",
                    "reply_markup": list_button_kb
                }
            )
            return "OK", 200

        if callback_data in RESPONSES:
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": RESPONSES[callback_data],
                    "reply_markup": list_button_kb,
                    "parse_mode": "Markdown"
                }
            )
            return "OK", 200

    return "OK", 200

# ================== RUN ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

