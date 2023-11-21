import json

from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from loader import dp, bot, config
from aiogram import types
from keyboards.inline_keyboards import inline_main_menu, inline_moder_keyboard
from utils.logger import send_log


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], commands=['moder_menu'])
async def command_moder_menu(message: types.Message):
    await bot.send_message(message.from_user.id, f"👑 Меню модератора 👑\n\n", parse_mode='html', reply_markup=inline_moder_keyboard)


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], commands=['users'])
async def command_moder_users(message: types.Message):
    with open('users.json', 'r') as f:
        users = json.load(f)
        print(users)
        users_string = "Количество пользователей: " + str(len(users)) + "\n---------------------\n"
        for user in list(users.keys()):
            users_string += f"{user} @{users[user]['username']}\n"
        await bot.send_message(message.from_user.id, users_string, parse_mode='html')
        f.close()
