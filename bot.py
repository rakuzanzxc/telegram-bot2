import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, URLInputFile

# --- НАСТРОЙКИ ---
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 7749663865  # Твой ID

# ССЫЛКА НА ТВОЙ ЕДИНЫЙ БАННЕР (Замени на свою ссылку из Imgur или TG)
BANNER_URL = "https://i.postimg.cc/Dw6v2H1B/banner.png"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="⚔️ ᴋɪʟʟᴀᴜʀᴀ (100 ₽ / ⭐)", callback_data="view_killaura")],
        [InlineKeyboardButton(text="🔥 ʜɪᴛʙᴏxᴇꜱ (40 ₽ / ⭐)", callback_data="view_hits")],
        [InlineKeyboardButton(text="🎯 ᴛʀɪɢɢᴇʀʙᴏᴛ (100 ₽ / ⭐)", callback_data="view_triggers")],
        [InlineKeyboardButton(text="👁️ ᴛᴀʀɢᴇᴛ ᴇꜱᴘ (30 ₽ / ⭐)", callback_data="view_esp")],
        [InlineKeyboardButton(text="🕹️ ᴀɪᴍ ᴀꜱꜱɪꜱᴛ (50 ₽ / ⭐)", callback_data="view_aim")],
        [InlineKeyboardButton(text="🛠 ᴄᴜꜱᴛᴏᴍ ᴍᴏᴅ (250 ₽ / ⭐)", callback_data="view_custom")],
        [InlineKeyboardButton(text="🆘 ꜱᴜᴘᴘᴏʀᴛ", callback_data="view_support")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_button():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ 𝔹𝔸ℂ𝕂", callback_data="to_main")]])

def get_payment_menu(item_name):
    buttons = [
        [InlineKeyboardButton(text="✅ Я ОПЛАТИЛ", callback_data=f"confirm_{item_name}")],
        [InlineKeyboardButton(text="⬅️ 𝔹𝔸ℂ𝕂", callback_data="to_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- ХЕНДЛЕРЫ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "✨ <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴡᴇᴀᴢᴢᴇʀᴄʟɪᴇɴᴛ</b> ✨\n\n"
        "Выберите товар из списка ниже.\n\n"
        "🆘 Поддержка: @wezroxss"
    )
    try:
        await message.answer_photo(
            photo=BANNER_URL,
            caption=welcome_text,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
    except:
        await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="HTML")

@dp.callback_query(F.data == "to_main")
async def process_to_main(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    await cmd_start(callback.message)

@dp.callback_query(F.data.startswith("view_"))
async def view_item(callback: types.CallbackQuery):
    data = callback.data
    
    # Словарь товаров
    content = {
        "view_killaura": ("Киллаура", "100 ₽ / 100 ⭐", "Лучшая Killaura среди читов."),
        "view_hits": ("ХИТБОКСЫ", "40 ₽ / 40 ⭐", "Лучшие хитбоксы, а главное легитные."),
        "view_triggers": ("ТРИГГЕРЫ", "100 ₽ / 100 ⭐", "Легитный триггер 1.20.1 Fabric."),
        "view_esp": ("TARGET ESP", "30 ₽ / 30 ⭐", "Визуальное отображение целей."),
        "view_aim": ("AIM ASSIST", "50 ₽ / 50 ⭐", "Плавная доводка прицела до цели."),
        "view_custom": ("МОД ПОД ЗАКАЗ", "250 ₽ / 250 ⭐", "Разработка мода по вашему описанию."),
        "view_support": ("ПОДДЕРЖКА", "-", "Пишите по всем вопросам: @wezroxss")
    }

    if data not in content: return
    item, price, desc = content[data]

    instruction = (
        f"🎁 <b>Вы выбрали: {item}</b>\n"
        f"📝 {desc}\n\n"
        f"💵 <b>Цена: {price}</b>\n\n"
        f"💳 <b>Как оплатить:</b>\n"
        f"Напишите администратору: @wezroxss\n\n"
        f"⚠️ <b>После оплаты нажмите кнопку ниже</b>"
    )

    await callback.message.delete()
    try:
        await callback.message.answer_photo(
            photo=BANNER_URL,
            caption=instruction,
            reply_markup=get_payment_menu(item),
            parse_mode="HTML"
        )
    except:
        await callback.message.answer(instruction, reply_markup=get_payment_menu(item), parse_mode="HTML")

# --- ПОДТВЕРЖДЕНИЕ И ВЫДАЧА ---

@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    item_name = callback.data.split("_")[1]
    user = callback.from_user
    await callback.message.answer("⏳ Заявка отправлена! Ожидайте подтверждения от администратора.", reply_markup=get_back_button())

    await bot.send_message(
        ADMIN_ID,
        f"🔔 <b>НОВЫЙ ЗАКАЗ!</b>\n\n"
        f"👤 Юзер: @{user.username} (ID: <code>{user.id}</code>)\n"
        f"📦 Товар: {item_name}\n"
        f"━━━━━━━━━━━━\n"
        f"Команда выдачи:\n"
        f"<code>/give {user.id} {item_name}</code>",
        parse_mode="HTML"
    )

@dp.message(Command("give"))
async def cmd_give(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        # Формат: /give ID название_файла
        args = message.text.split()
        user_id = int(args[1])
        file_alias = args[2].lower()
        
        # Маппинг файлов (имена должны совпадать с файлами в папке бота)
        files = {
            "киллаура": "killaura.rar",
            "хитбоксы": "pop_visuals.rar",
            "триггеры": "pops_visuals.rar",
            "esp": "target_esp.rar",
            "aim": "aim_assist.rar"
        }
        
        filename = files.get(file_alias, "file.rar")
        
        from aiogram.types import FSInputFile
        await bot.send_document(user_id, FSInputFile(filename), caption=f"✅ Оплата подтверждена! Ваш файл: {file_alias}")
        await message.answer(f"✅ Файл {filename} отправлен пользователю {user_id}")
    except Exception as e:
        await message.answer(f"Ошибка выдачи! Проверь ID и наличие файла.\n{e}")

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("🛡 Тех. поддержка: @wezroxss")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
