import telebot
import os

TOKEN = "8740639535:AAHbyI0EszZcmguJSFPFBJCZ0ZrKvb4J1MQ"

if not TOKEN:
    raise Exception("TOKEN не найден! Добавь его в Railway Variables")

bot = telebot.TeleBot(TOKEN)
