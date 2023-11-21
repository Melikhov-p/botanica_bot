import json
import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.command_handlers import process_start_command
from utils.logger import send_log
from keyboards.inline_keyboards import inline_main_menu
from loader import dp, bot, config
from aiogram import types
from states.ModerStates import MailingState


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'mailing')
async def moder_send_mailing(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, f"Отправьте сообщение для рассылки.", parse_mode='html')
    await MailingState.message.set()
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=MailingState.message, content_types=['photo', 'text'])
async def moder_send_mailing_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
        for user in list(users.keys()):
            if message.photo:
                await bot.send_photo(user, photo=message.photo[-1].file_id, caption=f"{message.caption}", parse_mode='html')
            else:
                await bot.send_message(user, f"{message.text}", parse_mode='html')
        file.close()
    await bot.send_message(message.from_user.id, f"Рассылка отправлена.", parse_mode='html')
    await send_log('INFO', message.from_user.username, 'Рассылка отправлена')
    await state.finish()


