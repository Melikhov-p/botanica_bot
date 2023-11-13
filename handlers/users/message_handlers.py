from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext

from handlers.users.command_handlers import process_start_command
from loader import dp, bot, config
from aiogram import types
from keyboards.inline_keyboards import inline_main_menu
from utils.logger import send_log
import re, random


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'])
async def message_communication(message: types.Message):
    await send_log('INFO', message.from_user.username, 'Вопрос распознан | Сообщение: {}'.format(message.text))
    if re.findall(r'куп.*|заказ', message.text):
        await bot.send_message(message.from_user.id, f"Для заказа букета выберите в /menu кнопку Сделать заказ", parse_mode='html')
    elif re.findall(r'позвон.*|звон.*|контак.*|связ.*|пис.*', message.text):
        await bot.send_message(message.from_user.id, f"Чтобы узнать наши контакты выберите в /menu кнопку Поделиться контактами", parse_mode='html')
    elif re.findall(r'цен.*|стоим.*|стоит', message.text):
        cost_answers = ['Цены приятные', 'Цены доступные', 'Цены не кусаются', 'Цены симпатичные', 'Цены привлекательные']
        await bot.send_message(message.from_user.id, random.choice(cost_answers), parse_mode='html')
    else:
        await send_log('WARNING', message.from_user.username, 'Неизвестный запрос | Сообщение: {}'.format(message.text))
        await bot.send_message(message.from_user.id, f"К сожалению, я не знаю, что на это ответить, попробуйте найти, что вас интересует в меню.", parse_mode='html')
        await process_start_command(message)

