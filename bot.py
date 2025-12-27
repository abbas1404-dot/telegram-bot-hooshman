import os
from flask import Flask, request
import requests

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# ================= MAIN MENU =================
main_kb = {
    "inline_keyboard": [
        [{"text": "📚 دوره‌های فعال", "callback_data": "courses"}],
        [{"text": "📝 ثبت‌نام", "url": "https://hooshmaniran.ir"}],  # ارجاع مستقیم به وبسایت
        [{"text": "🎓 دریافت گواهینامه", "callback_data": "cert"}],
        [{"text": "🪪 کارت آزمون", "callback_data": "card"}],
        [{"text": "📊 تعرفه آزمون", "callback_data": "fees"}],
        [{"text": "📈 دهک من چند است؟", "callback_data": "decile"}],
        [{"text": "📖 نمونه سوالات", "callback_data": "samples"}],
        [{"text": "📞 پشتیبانی", "url": "https://t.me/HOOSHMAN_IR"}],  # ارجاع مستقیم به تلگرام
        [{"text": "🌐 وبسایت", "url": "https://hooshmaniran.ir"}]
    ]
}

def edit(chat_id, msg_id, text, kb=None):
    payload = {
        "chat_id": chat_id,
        "message_id": msg_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if kb:
        payload["reply_markup"] = kb
    requests.post(f"{API}/editMessageText", json=payload)

# ================= COURSES =================
COURSES = {
    "💻 مهارت‌های کامپیوتر": ["ICDL", "EXCEL"],
    "🎨 گرافیک دیزاین": ["Photoshop", "Illustrator", "Corel Draw", "Premiere", "After Effect", "Create Content"],
    "🧠 مهندس هوش مصنوعی": ["Python", "Data Science", "Machine Learning", "Deep Learning", "Computer Vision"],
    "🧑 کاربر هوش مصنوعی": ["AI Automation", "AI Powered Learning"],
    "🌐 طراحی سایت": ["Frontend", "PHP", "WordPress", "SEO"],
    "🔒 شبکه و امنیت": ["Network+", "Linux", "Cisco", "Microsoft"],
    "📐 معماری مهندسی": ["AutoCAD", "3Ds Max", "Revit", "SolidWorks"]
}

# ================= PRICE =================
PRICE = {
    "ICDL": {6:"920.000",7:"989.000",8:"1.058.000",9:"1.127.000",10:"1.196.000"},
    "EXCEL": {6:"-",7:"-",8:"-",9:"-",10:"-"},
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

# ================= WEBHOOK =================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "OK"

    if "message" in data and data["message"].get("text") == "/start":
        cid = data["message"]["chat"]["id"]
        requests.post(f"{API}/sendMessage", json={
            "chat_id": cid,
            "text": "🌸 به *آکادمی تخصصی هوشمان* خوش آمدید",
            "reply_markup": main_kb,
            "parse_mode": "Markdown"
        })
        return "OK"

    if "callback_query" in data:
        q = data["callback_query"]
        cid = q["message"]["chat"]["id"]
        mid = q["message"]["message_id"]
        cb = q["data"]

        # ===== دوره‌ها =====
        if cb == "courses" or cb == "fees" or cb == "samples":  # samples مانند دوره‌ها
            kb = []
            row = []
            for i, key in enumerate(COURSES.keys()):
                row.append({"text": key, "callback_data": f"{cb}_course_{key}"})
                if (i+1) % 2 == 0:
                    kb.append(row)
                    row = []
            if row:
                kb.append(row)
            kb.append([{"text": "🔙 بازگشت", "callback_data": "back"}])
            edit(cid, mid, "📚 لطفاً یک دوره را انتخاب کنید:", {"inline_keyboard": kb})

        # ===== زیرمنو دوره =====
        elif cb.startswith("courses_course_") or cb.startswith("fees_course_") or cb.startswith("samples_course_"):
            prefix = "courses_course_" if cb.startswith("courses_course_") else "fees_course_" if cb.startswith("fees_course_") else "samples_course_"
            course_name = cb.replace(prefix, "")
            items = COURSES.get(course_name, [])
            kb = []
            for item in items:
                if cb.startswith("fees_course_"):
                    kb.append([{"text": item, "callback_data": f"fees_price_{item}"}])
                elif cb.startswith("samples_course_"):
                    kb.append([{"text": item, "callback_data": f"samples_file_{item}"}])
                else:
                    kb.append([{"text": item, "callback_data": f"courses_detail_{item}"}])
            kb.append([{"text": "🔙 بازگشت", "callback_data": cb[:4]}])
            edit(cid, mid, f"💡 {course_name} شامل موارد زیر است:", {"inline_keyboard": kb})

        # ===== نمایش قیمت بر اساس دهک =====
        elif cb.startswith("fees_price_"):
            item = cb.replace("fees_price_", "")
            prices = PRICE.get(item, {})
            text = f"💰 تعرفه {item} بر اساس دهک:\n"
            for d, p in prices.items():
                text += f"دهک {d}: {p} تومان\n"
            edit(cid, mid, text, {"inline_keyboard":[[{"text":"🔙 بازگشت","callback_data":"fees"}]]})

        # ===== دریافت گواهینامه =====
        elif cb == "cert":
            edit(
                cid,
                mid,
                "🎓 *دریافت گواهینامه*\n\n"
                "🔹 اگر از آزمون عملی شما *بیش از ۴۰ روز گذشته است*، "
                "می‌توانید با پرداخت هزینه گواهینامه، سپس فایل آن را دریافت کنید.\n\n"
                "🔹 اگر *قبلاً پرداخت انجام داده‌اید*، "
                "مستقیماً به لینک دریافت فایل مراجعه نمایید.",
                {
                    "inline_keyboard": [
                        [{"text": "💳 پرداخت هزینه گواهینامه", "url": "https://pay.portaltvto.com/pay/licence2"}],
                        [{"text": "📄 دریافت فایل گواهینامه", "url": "https://azmoon.portaltvto.com/estelam/estelam"}],
                        [{"text": "🔙 بازگشت", "callback_data": "back"}]
                    ]
                }
            )

        # ===== کارت آزمون =====
        elif cb == "card":
            edit(
                cid,
                mid,
                "🪪 *دریافت کارت آزمون*\n\n"
                "در صورتی که نام شما برای یک تاریخ مشخص ثبت آزمون شده باشد، "
                "می‌توانید *۱ تا ۳ روز قبل از آزمون* کارت خود را دانلود کنید.",
                {
                    "inline_keyboard": [
                        [{"text": "🪪 دریافت کارت آزمون", "url": "https://azmoon.portaltvto.com/card/card/index/1/80"}],
                        [{"text": "🔙 بازگشت", "callback_data": "back"}]
                    ]
                }
            )

        # ===== دهک =====
        elif cb == "decile":
            edit(
                cid,
                mid,
                "📈 *دهک من چند است؟*\n\n"
                "برای بررسی وضعیت دهک خانوار:\n"
                "🔹 سامانه حمایت وزارت رفاه\n"
                "🔹 کد دستوری: `#43857*4*`\n"
                "🔹 اپلیکیشن‌های رفاه ایرانیان و شادمان",
                {"inline_keyboard":[[{"text":"🔙 بازگشت","callback_data":"back"}]]}
            )

        # ===== نمونه سوالات =====
        elif cb.startswith("samples_file_"):
            # فعلاً فقط نمایش نام دوره، لینک فایل بعداً اضافه می‌شود
            item = cb.replace("samples_file_", "")
            edit(cid, mid, f"📄 نمونه سوالات {item} در دسترس است (لینک بعداً اضافه می‌شود).",
                 {"inline_keyboard":[[{"text":"🔙 بازگشت","callback_data":"samples"}]]})

        # ===== بازگشت به منوی اصلی =====
        elif cb == "back":
            edit(cid, mid, "📋 منوی اصلی:", main_kb)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
