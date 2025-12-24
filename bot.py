import os
from flask import Flask, request
import requests

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# 🎛 منوی اصلی
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

# 🎛 منوی "نمایش لیست" (برای بازگشت)
list_button_kb = {"inline_keyboard": [[{"text": "📊 نمایش لیست", "callback_data": "show_list"}]]}

WELCOME_TEXT = "سلام و درود 🌸\nبه **آکادمی تخصصی هوشمان** خوش آمدید —\nجایی که *یادگیری* با *هوشمندی* همراه می‌شود! 🧠✨"

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

# 🎯 تابع ویرایش پیام (برای رفتار درخواستی شما)
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

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if data is None:
            return "OK", 200

        # ✅ /start
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

        # ✅ کلیک‌ها
        if "callback_query" in data:
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            message_id = query["message"]["message_id"]
            callback_data = query["data"]

            requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": query["id"]})

            # 🔙 بازگشت به منوی اصلی
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

            # 📚 دوره‌های فعال → منوی یک‌ستونی
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
                        [{"text": "🔧 تاسیسات", "callback_data": "c_inst"}],
                        [{"text": "🔙 بازگشت", "callback_data": "back_to_main"}]
                    ]
                }
                edit_message(
                    chat_id,
                    message_id,
                    "📚 لطفاً یکی از دوره‌های زیر را انتخاب کنید:",
                    courses_kb
                )
                return "OK", 200

            # 🔙 بازگشت از منوی دوره‌ها
            if callback_data == "back_to_main":
                edit_message(
                    chat_id,
                    message_id,
                    "📋 منوی اصلی:",
                    main_keyboard
                )
                return "OK", 200

            # ▶️ انتخاب یک دوره — ویرایش پیام قبلی
            if callback_data.startswith("c_"):
                descriptions = {
                    "c_comp": "💻 *مهارت‌های کامپیوتر*\n• آموزش مبانی کامپیوتر، ویندوز، آفیس\n• سطح: مقدماتی تا متوسط\n• مدت: ۴۰ ساعت",
                    "c_graph": "🎨 *گرافیک دیزاین*\n• فتوشاپ، ایلاستریتور، کورل‌درآو\n• پروژه‌های عملی: بنر، لوگو، پوستر\n• مدت: ۶۰ ساعت",
                    "c_ai_eng": "🧠 *مهندس هوش مصنوعی*\n• یادگیری ماشین، شبکه‌های عصبی، پایتون\n• پیش‌نیاز: دانش برنامه‌نویسی\n• مدت: ۱۲۰ ساعت",
                    "c_ai_user": "🧑 *کاربر هوش مصنوعی*\n• کاربرد AI در رشته‌های مختلف\n• بدون نیاز به دانش برنامه‌نویسی\n• مدت: ۳۰ ساعت",
                    "c_web": "🌐 *طراحی سایت*\n• HTML, CSS, JavaScript, React\n• ساخت سایت شخصی و فروشگاهی\n• مدت: ۸۰ ساعت",
                    "c_net": "🔒 *شبکه و امنیت*\n• CCNA, امنیت سایبری، تست نفوذ\n• آزمایشگاه مجازی شبکه\n• مدت: ۱۰۰ ساعت",
                    "c_eng": "📐 *معماری مهندسی*\n• AutoCAD, Revit, 3D Max\n• طراحی ساختمان و محیط‌زیست\n• مدت: ۷۰ ساعت",
                    "c_art": "🎨 *هنرهای تجسمی*\n• نقاشی دیجیتال، انیمیشن، سه‌بعدی\n• نرم‌افزارهای تخصصی صنعت\n• مدت: ۵۰ ساعت",
                    "c_inst": "🔧 *تاسیسات*\n• برق، لوازم خانگی، سیستم‌های هوشمند\n• آموزش عملی در کارگاه\n• مدت: ۴۵ ساعت"
                }
                text = descriptions.get(callback_data, "⚠️ اطلاعات این دوره به زودی بروزرسانی می‌شود.")
                edit_message(
                    chat_id,
                    message_id,
                    text + "\n\n👇 برای بازگشت، روی «نمایش لیست» کلیک کنید.",
                    list_button_kb
                )
                return "OK", 200

            # ▶️ سایر گزینه‌ها
            responses = {
                "cert": "🎓 *دریافت گواهینامه*\nگواهینامه معتبر *وزارت کار* پس از قبولی صادر می‌شود.",
                "card": "🪪 *دریافت کارت آزمون*\nکارت ورود ۲۴ ساعت قبل از آزمون ارسال می‌شود.",
                "fee": "📊 *تعرفه آزمون*\n• آزمون اصلی: رایگان\n• آزمون آزمایشی: ۲۵۰,۰۰۰ تومان",
                "decile": "📈 *دهک من چند است؟*\nبر اساس رتبهٔ شما در میان کل شرکت‌کنندگان محاسبه می‌شود.",
                "samples": "📖 *نمونه سوالات*\nدر [وبسایت ما](https://hooshmaniran.ir/samples) قابل دانلود است."
            }

            if callback_data in responses:
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": responses[callback_data] + "\n\n👇 برای بازگشت، روی «نمایش لیست» کلیک کنید.",
                        "reply_markup": list_button_kb,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

        return "OK", 200

    except Exception as e:
        print("❌ Error:", str(e))
        return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
