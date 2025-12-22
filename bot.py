import os
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from aiohttp import web

# 🔑 دریافت توکن (اجباری)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN missing in environment.")

PORT = int(os.getenv("PORT", 8000))
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "").strip()

# 🎛 کیبورد
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 توضیحات آزمون", callback_data="exam")],
    [InlineKeyboardButton("🎓 مدارک و گواهینامه‌ها", callback_data="cert")],
    [InlineKeyboardButton("💰 شهریه", callback_data="price")],
    [InlineKeyboardButton("🪪 کارت ورود به جلسه", callback_data="card")]
])

# 📡 هندلرها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام و عرض ادب 🌸\nبه *آکادمی تخصصی هوشمان* خوش آمدید 👋\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    replies = {
        "exam": "📝 توضیحات کامل آزمون‌ها در این بخش قرار می‌گیرد.",
        "cert": "🎓 پس از پایان دوره، گواهینامه معتبر ارائه می‌شود.",
        "price": "💰 شهریه دوره‌ها به‌صورت نقد و اقساط قابل پرداخت است.",
        "card": "🪪 کارت ورود به جلسه ۲۴ ساعت قبل از آزمون صادر می‌شود."
    }
    await query.message.reply_text(replies.get(query.data, "⚠️ گزینه نامعتبر."))

# 🖥 سرویس health check (حیاتی برای Railway)
async def health_check(request):
    return web.Response(text="OK", status=200)

# 🌀 راه‌اندازی ربات
async def start_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    if WEBHOOK_HOST:
        webhook_path = f"/{TOKEN}"
        webhook_url = f"{WEBHOOK_HOST}{webhook_path}"
        print(f"📡 Setting webhook: {webhook_url}")
        await app.bot.set_webhook(url=webhook_url)
        await app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
            drop_pending_updates=True
        )
    else:
        print("🔄 Using polling (no WEBHOOK_HOST set)")
        await app.run_polling(drop_pending_updates=True)

# 🚀 نقطه ورود اصلی
if __name__ == "__main__":
    # ساخت سرور HTTP
    app_http = web.Application()
    app_http.router.add_get("/", health_check)

    async def main():
        # راه‌اندازی سرور HTTP
        runner = web.AppRunner(app_http)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"✅ HTTP server running on port {PORT} (for Railway)")

        # راه‌اندازی ربات در background
        bot_task = asyncio.create_task(start_bot())
        print("🤖 Bot is starting...")

        # منتظر بمان تا متوقف شود
        await bot_task

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹ Bot stopped.")
