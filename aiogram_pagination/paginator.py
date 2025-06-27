from abc import ABC
from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional



class BaseModelConfig(BaseModel, ABC):
    model_config = {"arbitrary_types_allowed": True}


class NavigationButtons(BaseModelConfig):
    """
        Configuration for navigation buttons in a paginated keyboard.

        Parameters:
            callback_prefix (``str``):
                Any UNIQUE name. It will be used for next/back buttons build-in handler.
                E.g.: "my_callback".
            
            separator (``str``):
                String that will be used for next/back buttons build-in handler
                Default: ':'
            
            back (``str):
                Button text that will be used for back button
                Default: 'Back'
            
            next (``str``):
                Button text that will be used for next button
                Default: 'Next'          
    """
    
    callback_prefix: str = Field(max_length=40)
    separator: str = Field(":", max_length=5)
    back: str = Field("Back", max_length=20)
    next: str = Field("Next", max_length=20)


    def _navigation(self, page: int, total_pages: int) -> List[InlineKeyboardButton]:
        buttons = []
        if page > 0:
            buttons.append(
                InlineKeyboardButton(
                    text=self.back,
                    callback_data=f"{self.callback_prefix}{self.separator}{page - 1}"
                )
            )
        if page < total_pages - 1:
            buttons.append(
                InlineKeyboardButton(
                    text=self.next,
                    callback_data=f"{self.callback_prefix}{self.separator}{page + 1}"
                )
            )

        return buttons


class Paginator(BaseModelConfig):
    """
        A paginator for aiogram inline keyboards.

        Parameters:
            dp (``Dispatcher``):
                Aiogram dispatcher object.

            keyboard (``InlineKeyboardMarkup``):
                Base keyboard to paginate

            nav_buttons (``NavigationButtons``):
                Navigation class object

            page_size (``int``):
                Items per page
                Default: '10'

            additional_keyboard (``InlineKeyboardMarkup | None``):
                Additional inline keyboard at the bottom
    """
    dp: Dispatcher
    keyboard: InlineKeyboardMarkup
    nav_buttons: NavigationButtons
    page_size: int = Field(10, ge=1)
    additional_keyboard: Optional[InlineKeyboardMarkup] = None

    @model_validator(mode='after')
    def register_handler(self) -> 'Paginator':
        add_kb_len = 0
        if self.additional_keyboard.inline_keyboard:
            add_kb_len = len(self.additional_keyboard.inline_keyboard)
        if self.page_size+add_kb_len>98:
            raise Exception("Max kb len is 100, reduce page_size in configuration")
        self.dp.callback_query.register(self._handler, F.data.startswith(self.nav_buttons.callback_prefix))
            
        return self

    async def _handler(self, callback: CallbackQuery) -> None:
        page = int(callback.data.split(self.nav_buttons.separator)[1])
        keyboard: InlineKeyboardMarkup = self._get_keyboard_markup(page=page)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()

    def _chunk(self, page: int) -> List[List[InlineKeyboardButton]]:
        start = page * self.page_size
        end = start + self.page_size
        return self.keyboard.inline_keyboard[start:end]

    def _get_keyboard_markup(self, page: int = 0) -> InlineKeyboardMarkup:
        total_items= len(self.keyboard.inline_keyboard)
        if total_items == 0:
            return InlineKeyboardMarkup(inline_keyboard=[])

        total_pages= (total_items + self.page_size - 1) // self.page_size

        page_buttons = self._chunk(page)
        nav_buttons_row= self.nav_buttons._navigation(page=page, total_pages=total_pages)

        final_keyboard = []
        final_keyboard.extend(page_buttons)
        if nav_buttons_row:
            final_keyboard.append(nav_buttons_row)

        if self.additional_keyboard:
            final_keyboard+=self.additional_keyboard.inline_keyboard

        return InlineKeyboardMarkup(inline_keyboard=final_keyboard)

    def __call__(self, page: int = 0) -> InlineKeyboardMarkup:
        return self._get_keyboard_markup(page) 