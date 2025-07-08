import os
import ssl
import certifi

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# SSL-контекст
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

# Словарь часто задаваемых вопросов
FAQ = {
    "привет": "Здравствуйте! Чем могу помочь?",
    "crm": "Система CRM Servier позволяет автоматизировать работу медицинских представителей.",
    "отчет": "Вы можете сформировать отчет через вкладку 'Отчеты' в интерфейсе CRM.",
    "поддержка": "Обратитесь в техническую поддержку через корпоративную почту или HelpDesk."
}

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    response = None
    for question, answer in FAQ.items():
        if question in user_message:
            response = answer
            break
    if not response:
        response = "Извините, я пока не знаю ответа на этот вопрос."
    await update.message.reply_text(response)

# Запуск бота
app = ApplicationBuilder().token(os.environ.get("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
