import telebot
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN не найден! Добавь его в Railway Variables")

bot = telebot.TeleBot(TOKEN)
