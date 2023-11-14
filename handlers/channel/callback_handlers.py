import json
import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.logger import send_log
from keyboards.inline_keyboards import inline_main_menu
from loader import dp, bot, config
from aiogram import types


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.CHANNEL), lambda callback: callback.data == 'channel_preorder')
async def channel_callback_preorder(callback: types.CallbackQuery):
    await send_log('INFO', callback.from_user.username, 'Запросил предзаказ с поста {}'.format(callback.message.text))
    await bot.send_message(callback.from_user.id, f"Для предзаказа позвоните по номеру {config['contacts']['phone']}", parse_mode='html')
