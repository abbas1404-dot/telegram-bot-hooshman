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
        [{"text": "📖 نمونه سوالات", "callback_data": "samples"}],
        [{"text": "📞 پشتیبانی", "url": "https://t.me/hooshman_support"}],
        [{"text": "🌐 وبسایت", "url": "https://hooshmaniran.ir"}]
    ]
}

def edit(chat, msg, text, kb):
    requests.post(f"{API}/editMessageText", json={
        "chat_id": chat,
        "message_id": msg,
        "text": text,
        "reply_markup": kb,
        "parse_mode": "Markdown"
    })

# ================= COURSES =================
COURSES = {
    "c_comp": ["ICDL", "EXCEL"],
    "c_graph": ["Photoshop", "Illustrator", "Corel Draw", "Premiere", "After Effect", "Create Content"],
    "c_ai_eng": ["Python", "Data Science", "Machine Learning", "Deep Learning", "Computer Vision"],
    "c_ai_user": ["AI Automation", "AI Powered Learning"],
    "c_web": ["Frontend", "PHP", "WordPress", "SEO"],
    "c_net": ["Network+", "Linux", "Cisco", "Microsoft"],
    "c_arch": ["AutoCAD", "3Ds Max", "Revit", "SolidWorks"]
}

courses_kb = {
    "inline_keyboard": [
        [{"text": "💻 مهارت‌های کامپیوتر", "callback_data": "c_comp"},
         {"text": "🎨 گرافیک دیزاین", "callback_data": "c_graph"}],

        [{"text": "🧠 مهندس هوش مصنوعی", "callback_data": "c_ai_eng"},
         {"text": "🧑 کاربر هوش مصنوعی", "callback_data": "c_ai_user"}],

        [{"text": "🌐 طراحی سایت", "callback_data": "c_web"},
         {"text": "🔒 شبکه و امنیت", "callback_data": "c_net"}],

        [{"text": "📐 معماری مهندسی", "callback_data": "c_arch"}],
        [{"text": "🔙 بازگشت", "callback_data": "back"}]
    ]
}

# ================= FEES (DECILE) =================
PRICE = {
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

# ================= ROUTE =================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    d = request.get_json()
    if not d:
        return "OK"

    if "message" in d and d["message"].get("text") == "/start":
        cid = d["message"]["chat"]["id"]
        requests.post(f"{API}/sendMessage", json={
            "chat_id": cid,
            "text": "به آکادمی تخصصی هوشمان خوش آمدید 🌸",
            "reply_markup": main_kb,
            "parse_mode": "Markdown"
        })
        return "OK"

    if "callback_query" in d:
        q = d["callback_query"]
        cid = q["message"]["chat"]["id"]
        mid = q["message"]["message_id"]
        cb = q["data"]

        if cb == "courses":
            edit(cid, mid, "📚 دوره‌های فعال:", courses_kb)

        elif cb in COURSES:
            kb = {"inline_keyboard": []}
            for i in range(0, len(COURSES[cb]), 2):
                row = [{"text": COURSES[cb][i], "callback_data": f"course_{COURSES[cb][i]}"}]
                if i+1 < len(COURSES[cb]):
                    row.append({"text": COURSES[cb][i+1], "callback_data": f"course_{COURSES[cb][i+1]}"})
                kb["inline_keyboard"].append(row)
            kb["inline_keyboard"].append([{"text": "🔙 بازگشت", "callback_data": "courses"}])
            edit(cid, mid, "📌 دوره موردنظر را انتخاب کنید:", kb)

        elif cb.startswith("course_"):
            name = cb.replace("course_", "")
            edit(cid, mid, f"📘 *{name}*\n\nبرای ثبت‌نام با پشتیبانی در ارتباط باشید.",
                 {"inline_keyboard":[[{"text":"📝 ثبت‌نام","url":"https://t.me/hooshman_support"}],
                                     [{"text":"🔙 بازگشت","callback_data":"courses"}]]})

        elif cb == "fees":
            edit(cid, mid, "📊 تعرفه آزمون – ابتدا دوره را انتخاب کنید:", courses_kb)

        elif cb.startswith("course_") and cb.replace("course_","") in PRICE:
            c = cb.replace("course_","")
            txt = f"💰 *تعرفه {c}*\n\n"
            for d in range(6,11):
                txt += f"دهک {d}: `{PRICE[c][d]} تومان`\n"
            edit(cid, mid, txt, {"inline_keyboard":[[{"text":"🔙 بازگشت","callback_data":"fees"}]]})

        elif cb == "back":
            edit(cid, mid, "منوی اصلی:", main_kb)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
