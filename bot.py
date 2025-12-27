import os
from flask import Flask, request
import requests

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

def back_btn(target="back_to_main"):
    return {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": target}]]}

def edit_message(chat_id, message_id, text, reply_markup):
    requests.post(
        f"{TELEGRAM_API}/editMessageText",
        json={
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "reply_markup": reply_markup,
            "parse_mode": "Markdown"
        }
    )

# ================== DECILE MENUS ==================
decile_main_kb = {
    "inline_keyboard": [
        [{"text": "💻 مهارت‌های کامپیوتر", "callback_data": "d_comp"},
         {"text": "🎨 گرافیک دیزاین", "callback_data": "d_graph"}],

        [{"text": "🧠 مهندس هوش مصنوعی", "callback_data": "d_ai_eng"},
         {"text": "🧑 کاربر هوش مصنوعی", "callback_data": "d_ai_user"}],

        [{"text": "🌐 طراحی سایت", "callback_data": "d_web"},
         {"text": "🔒 شبکه و امنیت", "callback_data": "d_net"}],

        [{"text": "📐 معماری مهندسی", "callback_data": "d_arch"}],

        [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
    ]
}

DECILE_SKILLS = {
    "d_comp": ["ICDL", "EXCEL"],
    "d_graph": ["Photoshop", "Illustrator", "Corel Draw", "Premiere", "After Effect", "Create Content"],
    "d_ai_eng": ["Python", "Data Science", "Machine Learning", "Deep Learning", "Computer Vision"],
    "d_ai_user": ["AI Automation", "AI Powered Learning"],
    "d_web": ["Frontend", "PHP", "WordPress", "SEO"],
    "d_net": ["Network+", "Linux", "Cisco", "Microsoft"],
    "d_arch": ["AutoCAD", "3Ds Max", "Revit", "SolidWorks"]
}

# ================== ROUTES ==================
@app.route("/")
def home():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "OK", 200

    # /start
    if "message" in data and data["message"].get("text") == "/start":
        chat_id = data["message"]["chat"]["id"]
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "سلام و درود 🌸\nبه **آکادمی تخصصی هوشمان** خوش آمدید!",
                "reply_markup": main_keyboard,
                "parse_mode": "Markdown"
            }
        )
        return "OK", 200

    # CALLBACKS
    if "callback_query" in data:
        q = data["callback_query"]
        chat_id = q["message"]["chat"]["id"]
        message_id = q["message"]["message_id"]
        cb = q["data"]

        requests.post(
            f"{TELEGRAM_API}/answerCallbackQuery",
            json={"callback_query_id": q["id"]}
        )

        if cb == "back_to_main":
            edit_message(chat_id, message_id, "📋 منوی اصلی:", main_keyboard)
            return "OK", 200

        if cb == "decile":
            edit_message(chat_id, message_id, "📈 رشته مورد نظر را انتخاب کنید:", decile_main_kb)
            return "OK", 200

        if cb in DECILE_SKILLS:
            skills = DECILE_SKILLS[cb]
            kb = {"inline_keyboard": []}

            for i in range(0, len(skills), 2):
                row = [{"text": skills[i], "callback_data": "noop"}]
                if i + 1 < len(skills):
                    row.append({"text": skills[i + 1], "callback_data": "noop"})
                kb["inline_keyboard"].append(row)

            kb["inline_keyboard"].append([{"text": "🔙 بازگشت", "callback_data": "decile"}])

            edit_message(chat_id, message_id, "📊 مهارت‌های این رشته:", kb)
            return "OK", 200

    return "OK", 200

# ================== RUN ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

