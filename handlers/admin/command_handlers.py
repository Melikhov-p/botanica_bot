from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from loader import dp, bot, config
from aiogram import types
from keyboards.inline_keyboards import inline_main_menu
from utils.logger import send_log


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['superuser'], commands=['send_msg'])
async def admin_command_send_msg(message: types.Message):
    command_args = message.get_args().split('|')
    if len(command_args) != 2:
        await send_log('ADMIN_WARNING', message.from_user.username, 'Неверный формат команды | Сообщение: {}'.format(message.text))
        await message.reply('Неверный формат команды\n\n'
                            '/send_msg user_id|message')
    else:
        user_info = await bot.get_chat_member(command_args[0], command_args[0])
        await bot.send_message(command_args[0], command_args[1])
        await send_log('ADMIN', message.from_user.username, f"Отправил через бота сообщение пользователю @{user_info['user']['username']}: {command_args[1]}")

