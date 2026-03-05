import telebot
import os

# Получаем токен из переменных окружения сервера
TOKEN = os.getenv('BOT_TOKEN')

# Проверка: если токен не найден, бот выдаст понятную ошибку вместо вылета
if TOKEN is None:
    raise ValueError("Ошибка: Переменная BOT_TOKEN не установлена в настройках Railway!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я работаю 24/7 на Railway!")

# Важно для Railway: добавьте бесконечный цикл
bot.infinity_polling()
