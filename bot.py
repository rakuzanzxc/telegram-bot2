import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

# ТВОИ ДАННЫЕ
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 7749663865  # ID очищен от лишних знаков

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="⚔️ 𝕂𝕀𝕃𝕃𝔸𝕌ℝ𝔸 (100 ₽ / ⭐)", callback_data="view_killaura")], # ДОБАВЛЕНО
        [InlineKeyboardButton(text="🔥 ℍ𝕀𝕋𝔹𝕆𝕏𝔼𝕊 (40 ₽ / ⭐)", callback_data="view_hits")],
        [InlineKeyboardButton(text="🎯 𝕋ℝ𝕀𝔾𝔾𝔼ℝ𝕊 (100 ₽ / ⭐)", callback_data="view_triggers")],
        [InlineKeyboardButton(text="👁️ 𝕋𝔸ℝ𝔾𝔼𝕋 𝔼𝕊ℙ (30 ₽ / ⭐)", callback_data="view_esp")],
        [InlineKeyboardButton(text="🕹️ 𝔸𝕀𝕄 𝔸𝕊𝕊𝕀𝕊𝕋 (50 ₽ / ⭐)", callback_data="view_aim")],
        [InlineKeyboardButton(text="🛠 ℂ𝕌𝕊𝕋𝕆𝕄 𝕄𝕆𝔻 (250 ₽ / ⭐)", callback_data="view_custom")],
        [InlineKeyboardButton(text="🆘 𝕊𝕌ℙℙ𝕆ℝ𝕋", callback_data="view_support")]
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
    await message.answer(
        "✨ 𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 **𝕮𝖍𝖊𝖆𝖙𝕮𝖑𝖎𝖊𝖓𝖙𝖘** ✨\n\n"
        "Выберите товар из списка ниже.\n"
        "🆘 Поддержка: /support",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "to_main")
async def process_to_main(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    await cmd_start(callback.message)

# Обновленный фильтр (добавлена killaura)
@dp.callback_query(F.data.in_(["view_killaura", "view_hits", "view_triggers", "view_esp", "view_aim", "view_custom"]))
async def view_item(callback: types.CallbackQuery):
    data = callback.data
    if data == "view_killaura":
        item, price, desc = "Киллаура", "100 ₽ или 100 ⭐", "Мощная KillAura с обходом античитов."
    elif data == "view_hits":
        item, price, desc = "ХИТБОКСЫ", "40 ₽ или 40 ⭐", "Лучшие настраиваемые хитбоксы."
    elif data == "view_triggers":
        item, price, desc = "ТРИГГЕРЫ", "100 ₽ или 100 ⭐", "Легитный триггер 1.20.1 Fabric."
    elif data == "view_esp":
        item, price, desc = "TARGET ESP", "30 ₽ или 30 ⭐", "Визуальное отображение целей."
    elif data == "view_aim":
        item, price, desc = "AIM ASSIST", "50 ₽ или 50 ⭐", "Плавная доводка прицела до цели."
    else:
        item, price, desc = "МОД ПОД ЗАКАЗ", "250 ₽ или 250 ⭐", "Разработка мода по вашему описанию."

    instruction = (
        f"🎁 **Вы выбрали: {item}**\n"
        f"📝 {desc}\n\n"
        f"💵 Цена: {price}\n"
        "--- \n"
        "💳 **Как оплатить:**\n"
        "Для оплаты напишите напрямую администратору:\n"
        "👉 @wezroxss\n\n"
        "⚠️ **После оплаты нажмите кнопку «Я ОПЛАТИЛ»**"
    )

    await callback.message.delete()
    try:
        photo = FSInputFile("item.jpg")
        await callback.message.answer_photo(photo, caption=instruction, reply_markup=get_payment_menu(item), parse_mode="Markdown")
    except:
        await callback.message.answer(instruction, reply_markup=get_payment_menu(item), parse_mode="Markdown")

# --- ПОДТВЕРЖДЕНИЕ И ВЫДАЧА ---

@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    item_name = callback.data.split("_")[1]
    user = callback.from_user
    await callback.message.answer("⏳ Заявка отправлена! Ожидайте подтверждения от администратора.", reply_markup=get_back_button())

    await bot.send_message(
        ADMIN_ID,
        f"🔔 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👤 Юзер: @{user.username} (ID: `{user.id}`)\n"
        f"📦 Товар: {item_name}\n"
        f"--- \n"
        f"Команды выдачи:\n"
        f"Киллаура: `/give_killaura {user.id}`\n"
        f"Хиты: `/give_hits {user.id}`\n"
        f"Триггеры: `/give_triggers {user.id}`"
    )

# --- КОМАНДЫ ВЫДАЧИ (Админские) ---

@dp.message(Command("give_killaura"))
async def give_killaura(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        uid = int(message.text.split()[1])
        # Убедись, что файл killaura.rar лежит в папке с ботом
        await bot.send_document(uid, FSInputFile("killaura.rar"), 
                               caption="✅ Оплата подтверждена! Ваш файл: КИЛЛАУРА")
        await message.answer(f"✅ Киллаура отправлена пользователю {uid}")
    except Exception as e:
        await message.answer(f"Ошибка! Введите: /give_killaura ID\n{e}")

# (Остальные команды give_hits, give_triggers и т.д. остаются без изменений ниже)
@dp.message(Command("give_hits"))
async def give_hits(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        uid = int(message.text.split()[1])
        await bot.send_document(uid, FSInputFile("pop_visuals.rar"), caption="✅ Оплата подтверждена! Ваш файл: ХИТБОКСЫ")
        await message.answer(f"✅ Отправлено {uid}")
    except:
        await message.answer("Ошибка! /give_hits ID")

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer("🛡 Тех. поддержка: @wezroxss")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
