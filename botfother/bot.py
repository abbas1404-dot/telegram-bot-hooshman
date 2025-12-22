from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8228546920:AAED-uM-Srx8MA0y0-Mc-6dx1sczQQjysNA"

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📝 توضیحات آزمون", callback_data="exam")],
    [InlineKeyboardButton("🎓 مدارک و گواهینامه‌ها", callback_data="cert")],
    [InlineKeyboardButton("💰 شهریه", callback_data="price")],
    [InlineKeyboardButton("🪪 کارت ورود به جلسه", callback_data="card")]
])

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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "exam":
        await query.message.reply_text("📝 توضیحات کامل آزمون‌ها در این بخش قرار می‌گیرد.")

    elif query.data == "cert":
        await query.message.reply_text("🎓 پس از پایان دوره، گواهینامه معتبر ارائه می‌شود.")

    elif query.data == "price":
        await query.message.reply_text("💰 شهریه دوره‌ها به‌صورت نقد و اقساط قابل پرداخت است.")

    elif query.data == "card":
        await query.message.reply_text("🪪 کارت ورود به جلسه ۲۴ ساعت قبل از آزمون صادر می‌شود.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
