import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from aiohttp import web
import asyncio

# 🔑 دریافت توکن از متغیر محیطی (استاندارد: TELEGRAM_BOT_TOKEN)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ خطای امنیتی: متغیر محیطی TELEGRAM_BOT_TOKEN تنظیم نشده است.")

# 🌐 آدرس عمومی Railway (برای webhook)
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")  # مثلاً: https://your-app.up.railway.app
PORT = int(os.getenv("PORT", 8000))  # Railway این را ست می‌کند

# 🎛 ساخت کیبورد
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 توضیحات آزمون", callback_data="exam")],
    [InlineKeyboardButton("🎓 مدارک و گواهینامه‌ها", callback_data="cert")],
    [InlineKeyboardButton("💰 شهریه", callback_data="price")],
    [InlineKeyboardButton("🪪 کارت ورود به جلسه", callback_data="card")]
])

# 📡 دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "سلام و عرض ادب 🌸\n\n"
        "به *آکادمی تخصصی هوشمان* خوش آمدید 👋\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
    )
    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# 🖱 مدیریت کلیک دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    responses = {
        "exam": "📝 توضیحات کامل آزمون‌ها در این بخش قرار می‌گیرد.",
        "cert": "🎓 پس از پایان دوره، گواهینامه معتبر ارائه می‌شود.",
        "price": "💰 شهریه دوره‌ها به‌صورت نقد و اقساط قابل پرداخت است.",
        "card": "🪪 کارت ورود به جلسه ۲۴ ساعت قبل از آزمون صادر می‌شود."
    }
    await query.message.reply_text(responses.get(query.data, "⚠️ گزینه نامعتبر است."))

# 🚀 راه‌اندازی
async def main():
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # اگر WEBHOOK_HOST وجود داشت → وب‌هوک
    if WEBHOOK_HOST:
        webhook_path = f"/{TOKEN}"
        webhook_url = f"{WEBHOOK_HOST}{webhook_path}"
        print(f"📡 تنظیم وب‌هوک: {webhook_url}")
        await app.bot.set_webhook(url=webhook_url)
        await app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
            secret_token=None  # اختیاری؛ برای امنیت بیشتر می‌توانید اضافه کنید
        )
    else:
        # حالت توسعه لوکال (polling)
        print("🔄 حالت توسعه: در حال استفاده از polling...")
        await app.run_polling()

# 🖥 سرویس health check (برای Railway — جلوگیری از خوابیدن)
async def health_check(request):
    return web.Response(text="OK", content_type="text/plain")

if __name__ == "__main__":
    # راه‌اندازی سرور HTTP ساده برای Railway
    app_http = web.Application()
    app_http.router.add_get("/", health_check)

    # راه‌اندازی ربات و سرور همزمان
    async def start_services():
        # راه‌اندازی ربات در background
        bot_task = asyncio.create_task(main())
        
        # راه‌اندازی سرور HTTP روی همان پورت
        runner = web.AppRunner(app_http)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        
        print(f"✅ ربات و سرویس health check روی پورت {PORT} فعال شد.")
        print("🌐 Railway می‌تواند این سرویس را بررسی کند: GET / → 'OK'")

        # منتظر بمان تا interrupt شود
        await bot_task

    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("\n⏹ ربات متوقف شد.")
