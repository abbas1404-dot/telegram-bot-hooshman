import os
from flask import Flask, request
import requests

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# 🎛 کیبورد اصلی
main_keyboard = {
    "inline_keyboard": [
        [{"text": "📚 دوره‌های فعال", "callback_data": "courses"}],
        [{"text": "📝 میخواهم ثبت نام کنم", "url": "https://t.me/hooshman_support"}]
        [{"text": "🎓 دریافت گواهینامه", "callback_data": "cert"}],
        [{"text": "🪪  دریافت کارت آزمون", "callback_data": "card"}],
        [{"text": "📊 تعرفه آزمون", "callback_data": "fee"}],
        [{"text": "📈 دهک من چند است؟", "callback_data": "decile"}],
        [{"text": "📖 نمونه سوالات", "callback_data": "samples"}]
        [{"text": "📞  پشتیبانی و مشاوره", "url": "https://t.me/hooshman_support"}],
        [{"text": "🌐 وبسایت آموزشگاه", "url": "https://hooshmaniran.ir/"}],
    ]
}

# 🎛 کیبورد فرعی: دوره‌های فعال (2 دکمه در هر سطر)
courses_keyboard = {
    "inline_keyboard": [
        [{"text": "💻 مهارت‌های کامپیوتر", "callback_data": "course_computer"}],
        [{"text": "🎨 گرافیک دیزاین", "callback_data": "course_graphics"}],
        [{"text": "🧩 برنامه‌نویسی", "callback_data": "course_programming"}],
        [{"text": "🤖 هوش مصنوعی", "callback_data": "course_ai"}],
        [{"text": "📢 تولید محتوا", "callback_data": "course_content"}],
        [{"text": "🌐 طراحی سایت", "callback_data": "course_web"}],
        [{"text": "🔒 شبکه و امنیت", "callback_data": "course_network"}],
        [{"text": "📐 معماری و مهندسی", "callback_data": "course_engineering"}],
        [{"text": "🎨 هنرهای تجسمی", "callback_data": "course_art"}]
    ]
}

# 🔁 برای نمایش 2 دکمه در هر سطر، لیست را به جفت‌ها تقسیم می‌کنیم
def make_double_column_keyboard(buttons):
    keyboard = []
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        keyboard.append(row)
    return {"inline_keyboard": keyboard}

# ساخت کیبورد دو ستونی برای دوره‌ها
course_buttons = [
    {"text": "💻 مهارت‌های کامپیوتر", "callback_data": "course_computer"},
    {"text": "🎨 گرافیک دیزاین", "callback_data": "course_graphics"},
    {"text": "🧩 برنامه‌نویسی", "callback_data": "course_programming"},
    {"text": "🤖 هوش مصنوعی", "callback_data": "course_ai"},
    {"text": "📢 تولید محتوا", "callback_data": "course_content"},
    {"text": "🌐 طراحی سایت", "callback_data": "course_web"},
    {"text": "🔒 شبکه و امنیت", "callback_data": "course_network"},
    {"text": "📐 معماری و مهندسی", "callback_data": "course_engineering"},
    {"text": "🎨 هنرهای تجسمی", "callback_data": "course_art"}
]

courses_keyboard_2col = make_double_column_keyboard(course_buttons)

WELCOME_TEXT = (
    "سلام و درود 🌸\n"
    "به **آکادمی تخصصی هوشمان** خوش آمدید —\n"
    "جایی که *یادگیری* با *هوشمندی* همراه می‌شود! 🧠✨\n\n"
    "برای دریافت اطلاعات، لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
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
                    "text": WELCOME_TEXT,
                    "reply_markup": main_keyboard,
                    "parse_mode": "Markdown"
                }
            )
            return "OK", 200

        # ✅ رسیدگی به کلیک‌ها
        if "callback_query" in 
            query = data["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            callback_data = query["data"]

            requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={"callback_query_id": query["id"]})

            # پاسخ به گزینه‌های اصلی
            if callback_data == "courses":
                # نمایش منوی دوره‌ها — 2 دکمه در هر سطر
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "📚 لطفاً یکی از دوره‌های زیر را انتخاب کنید:",
                        "reply_markup": courses_keyboard_2col,
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

            elif callback_data.startswith("course_"):
                # پاسخ موقت برای دوره‌های فرعی (قابل توسعه)
                course_names = {
                    "course_computer": "مهارت‌های کامپیوتر",
                    "course_graphics": "گرافیک دیزاین",
                    "course_programming": "برنامه‌نویسی",
                    "course_ai": "هوش مصنوعی",
                    "course_content": "تولید محتوا",
                    "course_web": "طراحی سایت",
                    "course_network": "شبکه و امنیت",
                    "course_engineering": "معماری و مهندسی",
                    "course_art": "هنرهای تجسمی"
                }
                name = course_names.get(callback_data, "این دوره")
                requests.post(
                    f"{TELEGRAM_API}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"در حال آماده‌سازی اطلاعات {name}...\n📌 به زودی جزئیات کامل (محتوا، مدرس، هزینه) اضافه می‌شود.",
                        "parse_mode": "Markdown"
                    }
                )
                return "OK", 200

            # سایر گزینه‌ها
            responses = {
                "price": "💰 شهریه دوره‌ها:\n• آزمون فنی: ۲,۵۰۰,۰۰۰ تومان\n• دوره‌های تخصصی: ۳,۲۰۰,۰۰۰ تومان\n• بسته‌های ویژه دانشجویی موجود است.\n\n📌 امکان پرداخت اقساطی فراهم است.",
                "cert": "🎓 گواهینامه فنی و حرفه‌ای:\nپس از اتمام دوره و قبولی در آزمون، گواهینامه معتبر *وزارت کار* صادر می‌شود و قابل استعلام در سامانه رسمی است.",
                "card": "🪪 کارت ورود به آزمون:\nکارت ورود ۲۴ ساعت قبل از آزمون به صورت خودکار به پیام‌رسان شما ارسال می‌شود. لطفاً از فعال بودن اینترنت و دسترسی به پیام‌ها اطمینان حاصل کنید.",
                "exam": "ℹ️ توضیحات آزمون:\nآزمون شامل ۱۰۰ سؤال چندگزینه‌ای، در ۹۰ دقیقه است. مباحث: فنی عمومی، تخصصی، و قوانین حرفه‌ای.",
                "fee": "📊 تعرفه آزمون‌ها:\n• آزمون اصلی: رایگان (برای دانشجویان ثبت‌نام‌شده)\n• آزمون آزمایشی: ۲۵۰,۰۰۰ تومان\n• آزمون بازگشتی: رایگان",
                "decile": "📈 دهک شما چگونه محاسبه می‌شود؟\nدهک بر اساس رتبهٔ شما در میان کل شرکت‌کنندگان آزمون تعیین می‌شود. پس از اعلام نتایج، در گواهینامه و پنل کاربری شما قابل مشاهده است.",
                "samples": "📖 نمونه سوالات آزمون فنی و حرفه‌ای:\nدر [این لینک](https://hooshmaniran.ir/samples) می‌توانید نمونه سوالات رایگان را دانلود کنید.\nهمچنین، بسته‌های ویژهٔ تمرین با پاسخنامهٔ تشریحی در فروشگاه ما موجود است."
            }

            text = responses.get(callback_data, "⚠️ محتوای این بخش به زودی بروزرسانی می‌شود.")
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": False
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
