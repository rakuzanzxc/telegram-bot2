import telebot
from telebot import types
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Данные о товарах (настрой цены здесь)
MODS = {
    "killaura": {
        "name": "⚔️ KillAura Pro",
        "price": "500 ⭐ / 450 руб",
        "desc": "Обход всех популярных античитов. Плавная наводка.",
        "img": "https://i.imgur.com/your_image_killaura.jpg" # ЗАМЕНИ НА СВОЮ ССЫЛКУ
    },
    "hitbox": {
        "name": "🎯 HitBoxes + Reach",
        "price": "300 ⭐ / 250 руб",
        "desc": "Увеличение хитбоксов врага без палева со стороны.",
        "img": "https://i.imgur.com/your_image_hitbox.jpg"
    },
    "esp": {
        "name": "👁️ Target ESP / Tracers",
        "price": "200 ⭐ / 150 руб",
        "desc": "Видишь всех сквозь стены. 3D боксы и линии.",
        "img": "https://i.imgur.com/your_image_esp.jpg"
    }
}

# Твой контакт для покупки
ADMIN_CONTACT = "@твой_юзернейм" # ИЗМЕНИ НА СВОЙ

@bot.message_handler(commands=['start'])
def main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Создаем кнопки для каждого мода
    btn1 = types.InlineKeyboardButton("⚔️ KillAura", callback_data="buy_killaura")
    btn2 = types.InlineKeyboardButton("🎯 HitBoxes", callback_data="buy_hitbox")
    btn3 = types.InlineKeyboardButton("👁️ ESP", callback_data="buy_esp")
    btn4 = types.InlineKeyboardButton("🔄 Items/AutoSwap", callback_data="buy_swap")
    btn5 = types.InlineKeyboardButton("🔫 AimAssist", callback_data="buy_aim")
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    welcome_text = (
        "<b>💎 MINECRAFT MODS STORE 💎</b>\n\n"
        "Лучшие софты для доминации на серверах.\n"
        "Выбери интересующий модуль ниже:"
    )
    
    # Отправляем главное меню с красивой общей картинкой
    bot.send_photo(message.chat.id, 
                   "https://i.imgur.com/main_menu_bg.jpg", # Главное фото магазина
                   caption=welcome_text, 
                   parse_mode="HTML", 
                   reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def product_page(call):
    item_key = call.data.replace("buy_", "")
    
    if item_key in MODS:
        product = MODS[item_key]
        
        text = (
            f"<b>{product['name']}</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📜 <i>{product['desc']}</i>\n\n"
            f"💰 <b>Цена:</b> {product['price']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🤝 Для покупки и активации пиши: {ADMIN_CONTACT}"
        )
        
        markup = types.InlineKeyboardMarkup()
        buy_btn = types.InlineKeyboardButton("💳 Купить сейчас", url=f"https://t.me/{ADMIN_CONTACT.replace('@', '')}")
        back_btn = types.InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")
        markup.add(buy_btn)
        markup.add(back_btn)

        # Редактируем сообщение (эффект перелистывания)
        bot.edit_message_media(
            media=types.InputMediaPhoto(product['img'], caption=text, parse_mode="HTML"),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back(call):
    # Возврат в меню (можно просто вызвать main_menu или отредактировать текущее)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    main_menu(call.message)

bot.infinity_polling()
