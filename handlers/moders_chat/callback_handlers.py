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
from states.BasicStates import ReportState, AskQuestionState


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.GROUP), lambda callback: callback.data == 'order_accepted')
async def moder_accept_order(callback: types.CallbackQuery):
    if callback.message.photo:
        await callback.message.edit_caption(f"{callback.message.caption}\n--------------------\n✅ЗАКАЗ ПРИНЯТ✅\n\n👤 Ответственный: @{callback.from_user.username}", parse_mode='html')
    else:
        await callback.message.edit_text(f"{callback.message.text}\n--------------------\n✅ЗАКАЗ ПРИНЯТ✅\n\n👤 Ответственный: @{callback.from_user.username}", parse_mode='html')
