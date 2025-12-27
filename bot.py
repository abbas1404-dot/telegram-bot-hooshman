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

def edit_message(chat_id, message_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{TELEGRAM_API}/editMessageText", json=payload)

def add_back_button(reply_markup, back_data="back_to_main"):
    keyboard = reply_markup["inline_keyboard"]
    if keyboard and len(keyboard[-1]) == 1 and keyboard[-1][0].get("callback_data") == "back_to_main":
        keyboard.pop()
    keyboard.append([{"text": "🔙 بازگشت", "callback_data": back_data}])
    return {"inline_keyboard": keyboard}

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if data is None:
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

        if "callback_query" in 
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            message_id = query["message"]["message_id"]
            callback_data = query["data"]

            requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": query["id"]})

            if callback_data == "back_to_main":
                edit_message(chat_id, message_id, "📋 منوی اصلی:", main_keyboard)
                return "OK", 200

            if callback_data == "courses":
                courses_kb = {
                    "inline_keyboard": [
                        [{"text": "💻 مهارت‌های کامپیوتر", "callback_data": "c_comp"}],
                        [{"text": "🎨 گرافیک دیزاین", "callback_data": "c_graph"}],
                        [{"text": "🧠 مهندس هوش مصنوعی", "callback_data": "c_ai_eng"}],
                        [{"text": "🧑 کاربر هوش مصنوعی", "callback_data": "c_ai_user"}],
                        [{"text": "🌐 طراحی سایت", "callback_data": "c_web"}],
                        [{"text": "🔒 شبکه و امنیت", "callback_data": "c_net"}],
                        [{"text": "📐 معماری مهندسی", "callback_data": "c_eng"}],
                        [{"text": "🎨 هنرهای تجسمی", "callback_data": "c_art"}],
                        [{"text": "🔧 تاسیسات", "callback_data": "c_inst"}]
                    ]
                }
                courses_kb = add_back_button(courses_kb)
                edit_message(chat_id, message_id, "📚 یک دوره را انتخاب کنید:", courses_kb)
                return "OK", 200

            if callback_data.startswith("c_"):
                descriptions = {
                    "c_comp": "💻 *مهارت‌های کامپیوتر*\n• آموزش ویندوز، آفیس\n• سطح: مقدماتی\n• مدت: ۴۰ ساعت",
                    "c_graph": "🎨 *گرافیک دیزاین*\n• فتوشاپ، ایلاستریتور\n• پروژه: لوگو، بنر\n• مدت: ۶۰ ساعت",
                    "c_ai_eng": "🧠 *مهندس هوش مصنوعی*\n• پایتون، یادگیری ماشین\n• پیش‌نیاز: برنامه‌نویسی\n• مدت: ۱۲۰ ساعت",
                    "c_ai_user": "🧑 *کاربر هوش مصنوعی*\n• کاربرد عملی AI\n• بدون برنامه‌نویسی\n• مدت: ۳۰ ساعت",
                    "c_web": "🌐 *طراحی سایت*\n• HTML, CSS, React\n• ساخت فروشگاه\n• مدت: ۸۰ ساعت",
                    "c_net": "🔒 *شبکه و امنیت*\n• CCNA، تست نفوذ\n• آزمایشگاه مجازی\n• مدت: ۱۰۰ ساعت",
                    "c_eng": "📐 *معماری مهندسی*\n• AutoCAD, Revit\n• طراحی ساختمان\n• مدت: ۷۰ ساعت",
                    "c_art": "🎨 *هنرهای تجسمی*\n• نقاشی دیجیتال\n• نرم‌افزارهای تخصصی\n• مدت: ۵۰ ساعت",
                    "c_inst": "🔧 *تاسیسات*\n• برق، لوازم خانگی\n• کارگاه عملی\n• مدت: ۴۵ ساعت"
                }
                text = descriptions.get(callback_data, "ℹ️ اطلاعات در حال آماده‌سازی است.")
                edit_message(chat_id, message_id, text, {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]]})
                return "OK", 200

            responses = {
                "cert": "🎓 *دریافت گواهینامه*\nگواهینامه معتبر *وزارت کار* پس از قبولی صادر می‌شود.",
                "card": "🪪 *دریافت کارت آزمون*\nکارت ورود ۲۴ ساعت قبل از آزمون ارسال می‌شود.",
                "fee": "📊 *تعرفه آزمون*\n• آزمون اصلی: رایگان\n• آزمون آزمایشی: ۲۵۰,۰۰۰ تومان",
                "decile": "📈 *دهک من چند است؟*\nبر اساس رتبه در میان کل شرکت‌کنندگان.",
                "samples": "📖 *نمونه سوالات*\nدر [وبسایت ما](https://hooshmaniran.ir/samples) قابل دانلود است."
            }

            if callback_data in responses:
                text = responses[callback_data] + "\n\n🔙 برای بازگشت، روی دکمه کلیک کنید."
                edit_message(chat_id, message_id, text, {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]]})
                return "OK", 200

        return "OK", 200

    except Exception as e:
        print("❌ Error:", str(e))
        return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
