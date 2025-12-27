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
        [{"text": "📝 ثبت‌نام", "url": "https://t.me/hooshman_support"}],
        [{"text": "🎓 دریافت گواهینامه", "callback_data": "cert"}],
        [{"text": "🪪 کارت آزمون", "callback_data": "card"}],
        [{"text": "📊 تعرفه آزمون", "callback_data": "fees"}],
        [{"text": "📈 دهک من چند است؟", "callback_data": "decile"}],
        [{"text": "📖 نمونه سوالات", "callback_data": "samples"}],
        [{"text": "📞 پشتیبانی", "url": "https://t.me/hooshman_support"}],
        [{"text": "🌐 وبسایت", "url": "https://hooshmaniran.ir"}]
    ]
}

def edit(chat_id, msg_id, text, kb):
    requests.post(f"{API}/editMessageText", json={
        "chat_id": chat_id,
        "message_id": msg_id,
        "text": text,
        "reply_markup": kb,
        "parse_mode": "Markdown"
    })

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

        # ===== دریافت گواهینامه =====
        if cb == "cert":
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
                "می‌توانید *۱ تا ۳ روز قبل از آزمون* با مراجعه به سامانه زیر و "
                "وارد کردن مشخصات، کارت آزمون خود را دانلود نمایید.",
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
                "برای بررسی وضعیت دهک خانوار:\n\n"
                "🔹 سامانه حمایت وزارت رفاه\n"
                "🔹 کد دستوری: `#43857*4*`\n"
                "🔹 اپلیکیشن‌های رفاه ایرانیان و شادمان",
                {"inline_keyboard":[[{"text":"🔙 بازگشت","callback_data":"back"}]]}
            )

        elif cb == "back":
            edit(cid, mid, "📋 منوی اصلی:", main_kb)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
