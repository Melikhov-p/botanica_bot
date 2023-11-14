from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from loader import dp, bot, config
from aiogram import types
from keyboards.inline_keyboards import inline_main_menu, inline_moder_keyboard
from utils.logger import send_log


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], commands=['moder_menu'])
async def command_moder_menu(message: types.Message):
    await bot.send_message(message.from_user.id, f"👑 Меню модератора 👑\n\n", parse_mode='html', reply_markup=inline_moder_keyboard)



