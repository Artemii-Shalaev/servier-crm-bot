import telebot
from telebot import types

bot = telebot.TeleBot('7632100037:AAGqFsETXTWJc6QPiYcDBzNHDPqVOdhxDvY')

# Глобальные переменные
name = ''
surname = ''
age = 0

# Обработчик обычных сообщений
@bot.message_handler(func=lambda message: message.text and message.text.lower() == "привет")
def greet_user(message):
    bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Напиши 'Привет' или /reg для регистрации.")

# Регистрация по шагам
@bot.message_handler(commands=['reg'])
def start_registration(message):
    bot.send_message(message.chat.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    try:
        age = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введи возраст цифрами.")
        return bot.register_next_step_handler(message, get_age)

    # Кнопки подтверждения
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    key_no = types.InlineKeyboardButton(text="Нет", callback_data="no")
    keyboard.add(key_yes, key_no)

    question = f"Тебе {age} лет, тебя зовут {name} {surname}?"
    bot.send_message(message.chat.id, question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Запомню :)")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Окей, начнём заново. Напиши /reg")

# Запуск бота
bot.polling(none_stop=True)
