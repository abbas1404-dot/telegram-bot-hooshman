import os
from flask import Flask, request
import requests

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# 🎛 منوی اصلی — دقیقاً مطابق درخواست شما
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

# 🎛 ساخت منوی دوره‌ها — 2 دکمه در هر سطر
def make_double_column(buttons):
    k = []
    for i in range(0, len(buttons), 2):
        k.append(buttons[i:i+2])
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

courses_kb = make_double_column(course_buttons)

# 📡 پیام خوش‌آمدگویی
WELCOME = (
    "سلام و درود 🌸\n"
    "به **آکادمی تخصصی هوشمان** خوش آمدید —\n"
    "جایی که *یادگیری* با *هوشمندی* همراه می‌شود! 🧠✨\n\n"
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
        if not data:
            return "No data", 400

        # ✅ /start
        if "message" in data and data["message"].get("text") == "/start":
            chat_id = data["message"]["chat"]["id"]
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": WELCOME,
                    "reply_markup": main_keyboard,
                    "parse_mode": "Markdown"
                }
            )
            return "OK", 200

        # ✅ رسیدگی به کلیک‌ها
        if "callback_query" in data:
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            callback_data = query["data"]

            # تأیید فوری کلیک
            requests.post(
                f"{TELEGRAM_API}/answerCallbackQuery",
                json={"callback_query_id": query["id"]}
            )

            # ▶️ دوره‌های فعال → منوی 2 ستونی
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

            # ▶️ دوره‌های فرعی
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
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"در حال آماده‌سازی اطلاعات {name}...\n✅ به زودی جزئیات کامل اضافه می‌شود.",
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

            # ▶️ سایر گزینه‌ها
            responses = {
                "cert": "🎓 *دریافت گواهینامه*\nپس از قبولی در آزمون، گواهینامه معتبر *وزارت کار* به صورت الکترونیکی صادر می‌شود و قابل استعلام در سامانه رسمی است.",
                "card": "🪪 *دریافت کارت آزمون*\nکارت ورود به جلسه ۲۴ ساعت قبل از آزمون به صورت خودکار در همین ربات برای شما ارسال می‌شود.",
                "fee": "📊 *تعرفه آزمون*\n• آزمون اصلی: رایگان (برای دانشجویان ثبت‌نام‌شده)\n• آزمون آزمایشی: ۲۵۰,۰۰۰ تومان",
                "decile": "📈 *دهک من چند است؟*\nدهک شما بر اساس رتبه‌ی شما در میان کل شرکت‌کنندگان محاسبه می‌شود و پس از اعلام نتایج در گواهینامه و پنل کاربری قابل مشاهده است.",
                "samples": "📖 *نمونه سوالات*\nدر [وبسایت ما](https://hooshmaniran.ir/samples) می‌توانید نمونه سوالات رایگان آزمون‌های فنی و حرفه‌ای را دانلود کنید."
            }

            text = responses.get(callback_data, "⚠️ محتوای این بخش به زودی بروزرسانی می‌شود.")
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
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
