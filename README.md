# Aiogram Inline Pagination

A comprehensive pagination system for aiogram inline keyboards with type safety and easy configuration.

## Features

- **Pagination System**: Navigate through large sets of data with back/next buttons
- **Type Safety**: Full type annotations for better code quality and IDE support
- **Easy Configuration**: Simple setup with customizable navigation buttons
- **Flexible**: Support for additional keyboards and custom page sizes
- **Automatic Handler Registration**: Built-in callback query handlers for navigation

## Installation

```bash
pip install pagination-aiogram3
```

## Quick Start

```python
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_pagination import Paginator, NavigationButtons
import asyncio

bot = Bot(token="YOUR_BOT_TOKEN_HERE")
dp = Dispatcher()

def get_test_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in range(500):
        inline_keyboard.append([
            InlineKeyboardButton(text=str(i), callback_data=f"kb__{i}"),
            InlineKeyboardButton(text=str(i + 1), callback_data=f"kb__{i + 1}")
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

# Additional keyboard at the bottom
add_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])

# Russian paginator
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

# English paginator
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
        text='Choose an option:',
        reply_markup=kb()
    )

async def main() -> None:  
    dp.message.register(menu_handler)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

### NavigationButtons

Configure the navigation buttons with the following parameters:

- `callback_prefix` (str): Unique prefix for callback data (required)
- `separator` (str): Separator for callback data (default: ":")
- `back` (str): Text for back button (default: "Back")
- `next` (str): Text for next button (default: "Next")

### Paginator

Configure the paginator with:

- `dp` (Dispatcher): Aiogram dispatcher object
- `keyboard` (InlineKeyboardMarkup): Base keyboard to paginate
- `nav_buttons` (NavigationButtons): Navigation configuration
- `page_size` (int): Items per page (default: 10)
- `additional_keyboard` (InlineKeyboardMarkup): Additional keyboard at the bottom (optional)

## Dependencies

- `aiogram>=3.0` - Telegram Bot API framework
- `pydantic>=2.0` - Data validation and settings management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 
