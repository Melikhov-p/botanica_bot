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


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'contacts')
async def process_callback_contacts(callback: types.CallbackQuery):
    await send_log('INFO', callback.from_user.username, 'Запросил контакты')
    await bot.send_message(callback.from_user.id, f"Способы связи:\n\n"
                                                  f"📞 <b>Телефон</b>: {config['contacts']['phone']}\n\n"
                                                  f"📧 <b>Email</b>: {config['contacts']['email']}\n\n"
                                                  f"📍 <b>Адрес</b>: {config['contacts']['address']}", parse_mode='html')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'all_products')
async def process_callback_all_products(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, f"🌷 Маленький букет - даром \n\n"
                                                  f"🌹 Средний букет - доплатим сами \n\n"
                                                  f"💐 Большой букет - Забирайте весь магазин", parse_mode='html')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'get_taxi')
async def process_callback_get_taxi(callback: types.CallbackQuery):
    await send_log('INFO', callback.from_user.username, 'Выбрал вызов такси')
    await bot.send_message(callback.from_user.id, f"🚕 Для вызова такси нажмите по кнопке ниже 🚕 ",
                           parse_mode='html',
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Проложить маршрут', url=config['taxi_api_url'])))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'report')
async def user_callback_report(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, f"📝 Опишите вашу проблему", parse_mode='html')
    await ReportState.report.set()
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=ReportState.report)
async def user_message_get_report(message: types.Message, state: FSMContext):
    await send_log('INFO', message.from_user.username, 'Возникли проблемы с ботом')
    await bot.send_message(config['superuser'], f"📛 REPORT от @{message.from_user.username}:\n\n"
                                                f"{message.text}", parse_mode='html')
    await bot.send_message(message.from_user.id, f"Я сообщил о ваших проблемах, спасибо за обращение ❤️", parse_mode='html')
    await state.finish()
    await process_start_command(message)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'ask_question')
async def user_callback_ask_question(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, f"📝 Напишите ваш вопрос, мы ответим на него как можно скорее.", parse_mode='html')
    await AskQuestionState.question.set()
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=AskQuestionState.question)
async def user_message_get_question(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, f"Ваш вопрос отправлен модераторам, скоро с вами свяжутся.", parse_mode='html')
    await bot.send_message(config['moders_chat'], f"❓ Вопрос от @{message.from_user.username} ({message.from_user.id})\n\n"
                                                  f"{message.text}", parse_mode='html')
    await send_log('INFO', message.from_user.username, 'Отправлен вопрос модераторам {}'.format(message.text))
    await state.finish()
    await process_start_command(message)
