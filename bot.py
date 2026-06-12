import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== НАСТРОЙКИ ====================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Создай файл .env и добавь строку BOT_TOKEN=твой_токен")
# ===================================================


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
    keyboard = [[InlineKeyboardButton("⬅️ Назад в главное меню", callback_data="back_to_main")]]
    return InlineKeyboardMarkup(keyboard)


# ==================== ОБРАБОТЧИКИ ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Привет! Я бот-помощник тренера по плаванию.\n\n"
        "Здесь ты можешь узнать обо мне, услугах, ценах и записаться на пробное занятие.\n\n"
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
        text = (
            "👤 <b>Обо мне и подходе</b>\n\n"
            "Привет! Меня зовут <b>[ИМЯ ТРЕНЕРА]</b>.\n\n"
            "Стаж: <b>[X] лет</b>\n"
            "Специализация: дети от 4 лет и взрослые.\n\n"
            "Мой подход: индивидуальный, с акцентом на технику и преодоление страха воды."
        )
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "services":
        text = (
            "🏊 <b>Услуги и цены</b>\n\n"
            "• Индивидуальное 45 мин — [ЦЕНА] ₽\n"
            "• Индивидуальное 60 мин — [ЦЕНА] ₽\n"
            "• Мини-группа (2-4 чел) — [ЦЕНА] ₽ с человека\n\n"
            "Абонементы выгоднее!"
        )
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "location":
        text = "📍 <b>Где занимаемся</b>\n\n[Полный адрес бассейна + как добраться]"
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "faq_menu":
        await query.edit_message_text("❓ Выбери вопрос:", reply_markup=get_faq_menu())

    elif data == "booking":
        text = (
            "📅 <b>Как записаться на пробное занятие</b>\n\n"
            "Напиши мне в личные сообщения Telegram:\n"
            "• Твоё имя\n"
            "• Возраст (или возраст ребёнка)\n"
            "• Удобные дни и время"
        )
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    elif data == "contacts":
        text = (
            "📞 <b>Контакты и соцсети</b>\n\n"
            "Telegram: @твой_ник\n"
            "Телефон / WhatsApp: +7 (XXX) XXX-XX-XX\n"
            "Instagram: @твой_инстаграм"
        )
        await query.edit_message_text(text, reply_markup=get_back_button(), parse_mode="HTML")

    # FAQ
    elif data == "faq_age":
        text = "👶 Я беру детей с <b>4 лет</b>. Для взрослых ограничений по возрасту нет."
        await query.edit_message_text(text, reply_markup=get_faq_menu(), parse_mode="HTML")

    elif data == "faq_trial":
        text = "🎁 Да, пробное занятие стоит [ЦЕНА] ₽."
        await query.edit_message_text(text, reply_markup=get_faq_menu(), parse_mode="HTML")

    elif data == "faq_what_to_bring":
        text = "🩱 Обязательно: купальник/плавки, шапочка, очки, полотенце, шлёпанцы."
        await query.edit_message_text(text, reply_markup=get_faq_menu(), parse_mode="HTML")

    elif data == "faq_price":
        text = "💰 Актуальные цены смотри в разделе «Услуги и цены»."
        await query.edit_message_text(text, reply_markup=get_faq_menu(), parse_mode="HTML")

    elif data == "faq_format":
        text = "👥 Можно заниматься как индивидуально, так и в мини-группе (2-4 человека)."
        await query.edit_message_text(text, reply_markup=get_faq_menu(), parse_mode="HTML")

    elif data == "faq_fear":
        text = "😰 Конечно! Я специализируюсь на работе со страхом воды. Занятия проходят постепенно и комфортно."
        await query.edit_message_text(text, reply_markup=get_faq_menu(), parse_mode="HTML")


# ==================== ЗАПУСК ====================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот для тренера по плаванию запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()