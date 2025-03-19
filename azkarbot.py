import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# 🔹 تحميل متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("🚨 خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")

# 🔹 إعدادات البوت
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# 📝 قائمة الأذكار
azkar = [
    "سبحان الله وبحمده، سبحان الله العظيم 🌿",
    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير ☁️",
    "اللهم صل وسلم على نبينا محمد ﷺ 🌷",
    "أستغفر الله العظيم وأتوب إليه 💙",
    "اللهم اغفر لي، ولوالدي، وللمسلمين أجمعين 🤲"
]

# 🔹 زر التنقل بين الأذكار
def get_keyboard(index):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ السابق", callback_data=f"azkar_{index - 1}"))
    if index < len(azkar) - 1:
        buttons.append(InlineKeyboardButton(text="التالي ➡️", callback_data=f"azkar_{index + 1}"))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None

# 📌 أمر /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(azkar[0], reply_markup=get_keyboard(0))

# 📌 التنقل بين الأذكار
@router.callback_query(lambda c: c.data.startswith("azkar_"))
async def change_zekr(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    await callback_query.message.edit_text(azkar[index], reply_markup=get_keyboard(index))

# 🔹 تشغيل البوت باستخدام Polling
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
