import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== НАСТРОЙКИ ====================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Создай файл .env")

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
    text = (
        "👋 Привет! Я бот-помощник тренера по плаванию.\n\n"
        "Выбери нужный раздел ниже 👇"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_main":
        await query.edit_message_text("Выбери нужный раздел 👇", reply_markup=get_main_menu())

    elif data == "about_me":
        text = "👤 <b>Обо мне и подходе</b>\n\n[Здесь текст про тренера]"
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "services":
        text = "🏊 <b>Услуги и цены</b>\n\n[Здесь цены]"
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "location":
        text = "📍 <b>Где занимаемся</b>\n\n[Адрес бассейна]"
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "faq_menu":
        await query.edit_message_text("❓ Выбери вопрос:", reply_markup=get_faq_menu())

    elif data == "booking":
        text = "📅 Напиши мне в личные сообщения для записи на пробное занятие."
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "contacts":
        text = "📞 Telegram: @твой_ник\nТелефон: +7 (XXX) XXX-XX-XX"
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    # FAQ
    elif data == "faq_age":
        await query.edit_message_text("👶 Я беру детей с 4 лет.", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_trial":
        await query.edit_message_text("🎁 Пробное занятие стоит [ЦЕНА] ₽.", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_what_to_bring":
        await query.edit_message_text("🩱 Купальник, шапочка, очки, полотенце.", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_price":
        await query.edit_message_text("💰 Цены смотри в разделе «Услуги и цены».", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_format":
        await query.edit_message_text("👥 Можно индивидуально и в мини-группе.", reply_markup=get_faq_menu(), parse_mode="HTML")
    elif data == "faq_fear":
        await query.edit_message_text("😰 Да, я работаю со страхом воды.", reply_markup=get_faq_menu(), parse_mode="HTML")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот успешно запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()