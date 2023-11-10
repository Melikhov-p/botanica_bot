import json
import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_keyboards import inline_main_menu
from loader import dp, bot, config
from aiogram import types


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'contacts')
async def process_callback_contacts(callback: types.CallbackQuery):
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
    await bot.send_message(callback.from_user.id, f"🚕 Для вызова такси нажмите по кнопке ниже 🚕 ",
                           parse_mode='html',
                           reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Проложить маршрут', url=config['taxi_api_url'])))

