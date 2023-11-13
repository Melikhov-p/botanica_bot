from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import config


def keyboard_generator(keyboard: dict) -> InlineKeyboardMarkup:
    buttons = []
    for button_cd, button_text in keyboard.items():
        buttons.append(InlineKeyboardButton(button_text, callback_data=button_cd))
    return InlineKeyboardMarkup(row_width=1).add(*buttons)
