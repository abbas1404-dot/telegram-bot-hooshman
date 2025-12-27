import os
from flask import Flask, request
import requests

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# ================== MAIN KEYBOARD ==================
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

# ================== HELPERS ==================
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
    "d_graph": ["Photoshop", "Illustrator", "Premiere", "After Effect", "Create Content"],
    "d_ai_eng": ["Python", "Deep Learning"],
    "d_ai_user": ["AI Automation", "AI Powered Learning"],
    "d_web": ["WordPress", "SEO"],
    "d_net": ["Network+"],
    "d_arch": ["AutoCAD", "3Ds Max"]
}

# ================== PRICE TABLE ==================
PRICE_TABLE = {
    "ICDL": {6:"920.000",7:"989.000",8:"1.058.000",9:"1.127.000",10:"1.196.000"},
    "AutoCAD": {6:"912.000",7:"981.000",8:"1.049.000",9:"1.117.000",10:"1.186.000"},
    "3Ds Max": {6:"1.347.000",7:"1.448.000",8:"1.549.000",9:"1.650.000",10:"1.751.000"},
    "Network+": {6:"320.000",7:"344.000",8:"368.000",9:"392.000",10:"416.000"},
    "Photoshop": {6:"720.000",7:"774.000",8:"828.000",9:"882.000",10:"936.000"},
    "Illustrator": {6:"720.000",7:"774.000",8:"828.000",9:"882.000",10:"936.000"},
    "Premiere": {6:"384.000",7:"413.000",8:"441.000",9:"471.000",10:"499.000"},
    "After Effect": {6:"1.160.000",7:"1.247.000",8:"1.334.000",9:"1.421.000",10:"1.508.000"},
    "Python": {6:"840.000",7:"903.000",8:"966.000",9:"1.029.000",10:"1.092.000"},
    "WordPress": {6:"1.448.000",7:"1.556.600",8:"1.665.200",9:"1.773.800",10:"1.882.400"},
    "Deep Learning": {6:"962.500",7:"1.034.680",8:"1.106.870",9:"1.179.060",10:"1.251.250"},
    "Create Content": {6:"448.000",7:"481.600",8:"515.200",9:"548.800",10:"582.400"},
    "SEO": {6:"1.240.000",7:"1.333.000",8:"1.426.000",9:"1.519.000",10:"1.612.000"}
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
                row = [{"text": skills[i], "callback_data": f"price_{skills[i]}"}]
                if i + 1 < len(skills):
                    row.append({"text": skills[i + 1], "callback_data": f"price_{skills[i + 1]}"} )
                kb["inline_keyboard"].append(row)
            kb["inline_keyboard"].append([{"text": "🔙 بازگشت", "callback_data": "decile"}])
            edit_message(chat_id, message_id, "📊 مهارت‌ها را انتخاب کنید:", kb)
            return "OK", 200

        if cb.startswith("price_"):
            course = cb.replace("price_", "")
            prices = PRICE_TABLE.get(course)
            if not prices:
                edit_message(chat_id, message_id, "❌ قیمت یافت نشد", decile_main_kb)
                return "OK", 200

            text = f"💰 *هزینه دوره {course}*\n\n"
            for d in range(6, 11):
                text += f"دهک {d}: `{prices[d]} تومان`\n"

            edit_message(
                chat_id,
                message_id,
                text,
                {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "decile"}]]}
            )
            return "OK", 200

    return "OK", 200

# ================== RUN ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
