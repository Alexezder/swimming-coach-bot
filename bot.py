import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден!")

# ==================== КЛАВИАТУРЫ ====================

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("👤 Обо мне и подходе", callback_data="about_me")],
        [InlineKeyboardButton("🏊 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton("📍 Где занимаемся", callback_data="location")],
        [InlineKeyboardButton("❓ Частые вопросы", callback_data="faq_menu")],
        [InlineKeyboardButton("📅 Как записаться на пробное", callback_data="booking")],
        [InlineKeyboardButton("📞 Контакты и соцсети", callback_data="contacts")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_faq_menu():
    keyboard = [
        [InlineKeyboardButton("С какого возраста можно начинать?", callback_data="faq_age")],
        [InlineKeyboardButton("Есть ли пробное занятие?", callback_data="faq_trial")],
        [InlineKeyboardButton("Что нужно взять с собой?", callback_data="faq_what_to_bring")],
        [InlineKeyboardButton("Сколько стоит занятие?", callback_data="faq_price")],
        [InlineKeyboardButton("Индивидуально или в группе?", callback_data="faq_format")],
        [InlineKeyboardButton("Можно ли, если боюсь воды?", callback_data="faq_fear")],
        [InlineKeyboardButton("⬅️ Назад в главное меню", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад в главное меню", callback_data="back_to_main")]])


# ==================== ОБРАБОТЧИКИ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "👋 Привет! Выбери нужный раздел ниже 👇"
    await update.message.reply_text(text, reply_markup=get_main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_main":
        await query.edit_message_text("Выбери нужный раздел 👇", reply_markup=get_main_menu())
    elif data == "about_me":
        await query.edit_message_text("👤 Здесь текст про тренера", reply_markup=get_back_button(), parse_mode="HTML")
    elif data == "services":
        await query.edit_message_text("🏊 Здесь услуги и цены", reply_markup=get_back_button(), parse_mode="HTML")
    elif data == "location":
        await query.edit_message_text("📍 Здесь адрес бассейна", reply_markup=get_back_button(), parse_mode="HTML")
    elif data == "faq_menu":
        await query.edit_message_text("❓ Выбери вопрос:", reply_markup=get_faq_menu())
    elif data == "booking":
        await query.edit_message_text("📅 Напиши мне для записи на пробное", reply_markup=get_back_button(), parse_mode="HTML")
    elif data == "contacts":
        await query.edit_message_text("📞 Контакты здесь", reply_markup=get_back_button(), parse_mode="HTML")
    elif data == "faq_age":
        await query.edit_message_text("👶 С 4 лет", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_trial":
        await query.edit_message_text("🎁 Пробное стоит [ЦЕНА]", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_what_to_bring":
        await query.edit_message_text("🩱 Купальник, шапочка, очки", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_price":
        await query.edit_message_text("💰 Смотри раздел Услуги", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_format":
        await query.edit_message_text("👥 Индивидуально и в группе", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_fear":
        await query.edit_message_text("😰 Работаю со страхом воды", reply_markup=get_faq_menu(), parse_mode="HTML")


async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот запущен на Webhooks!")

    # === Webhook настройки для Render ===
    PORT = int(os.environ.get("PORT", 8443))
    RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

    if RENDER_HOST:
        webhook_url = f"https://{RENDER_HOST}/webhook"
        print(f"Webhook URL: {webhook_url}")

        await application.initialize()
        await application.start()
        await application.updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="webhook",
            webhook_url=webhook_url,
        )
        await asyncio.Event().wait()
    else:
        # Локальный запуск (для теста)
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())