from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio
from aiogram import Dispatcher, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram_pagination import Paginator, NavigationButtons


bot = Bot(token="YOUR_BOT_TOKEN_HERE")  # Replace with your actual bot token
dp = Dispatcher()

def get_test_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in range(500):
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=str(i), callback_data=f"kb__{i}"),
                InlineKeyboardButton(text=str(i + 1), callback_data=f"kb__{i + 1}")
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)




add_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]])

ru_test_paginator = Paginator(
    dp=dp,
    keyboard=get_test_keyboard(),
    page_size=30,
    nav_buttons=NavigationButtons(
        callback_prefix="call",
        back="Назад",
        next="Дальше"
    ),
    additional_keyboard=add_kb
)

en_test_paginator = Paginator(
    dp=dp,
    keyboard=get_test_keyboard(),
    page_size=30,
    nav_buttons=NavigationButtons(
        callback_prefix="en_call"
    ),
    additional_keyboard=add_kb
)


async def menu_handler(message: Message, bot: Bot):
    if message.from_user.language_code == "ru":
        kb = ru_test_paginator
    else:
        kb = en_test_paginator
    await message.answer(
        text='Some text',
        reply_markup=kb()
    )



async def main() -> None:  
    dp.message.register(menu_handler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())