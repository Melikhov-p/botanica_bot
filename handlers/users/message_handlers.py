from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.command_handlers import process_start_command
from loader import dp, bot, config
from aiogram import types
from keyboards.inline_keyboards import inline_main_menu, inline_make_order
from utils.logger import send_log
import re, random
import psycopg2


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'])
async def message_communication(message: types.Message):
    if re.findall(r'Хочу букет дня', message.text):
        await send_log('INFO', message.from_user.username, 'Вопрос распознан | Тематика букет дня | Сообщение: {}'.format(message.text))
        await bot.send_message(config['moders_chat'], f"🔴 Новый заказ🔴 : @{message.from_user.username} : {message.from_user.id}\n\n"
                                                      f"📦 Состав заказа: БУКЕТ ДНЯ\n\n", parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Принят', callback_data='order_accepted')))
        await bot.send_message(message.from_user.id, f"Заказ на букет дня сформирован, скоро с вами свяжутся для подтверждения.", parse_mode='html')
    elif re.findall(r'site@[0-9]*', message.text):
        product_id = message.text.split('@')[1]
        try:
            conn = psycopg2.connect(
                dbname='botanicaflowers',
                user='botanica_web',
                password='b0t@nic@',
                host='localhost'
            )
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM goods_product WHERE id = '{product_id}'")
                product = cur.fetchone()
                if product:
                    await send_log('SITE', message.from_user.username, 'Заказ с сайта | Сообщение: {}'.format(message.text))
                    await bot.send_message(config['moders_chat'], f"🔴 Новый заказ от сайта🔴 : @{message.from_user.username} : {message.from_user.id}\n\n"
                                                                  f"📦 Состав заказа: {product[1]}\n\n", parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Принят', callback_data='order_accepted')))
                else:
                    await send_log('ERROR', message.from_user.username, 'Не удалось найти товар с сайта | Сообщение: {}'.format(message.text))
                    await bot.send_message(message.from_user.id, 'Не удалось найти товар', parse_mode='html')
        except Exception as e:
            print(str(e))

    elif re.findall(r'куп.*|заказ', message.text):
        await send_log('INFO', message.from_user.username, 'Вопрос распознан | Тематика как заказать | Сообщение: {}'.format(message.text))
        await bot.send_message(message.from_user.id, f"Для заказа букета выберите в /menu кнопку Сделать заказ", parse_mode='html')
    elif re.findall(r'позвон.*|звон.*|контак.*|связ.*|пис.*', message.text):
        await send_log('INFO', message.from_user.username, 'Вопрос распознан | Тематика контакты | Сообщение: {}'.format(message.text))
        await bot.send_message(message.from_user.id, f"Чтобы узнать наши контакты выберите в /menu кнопку Поделиться контактами", parse_mode='html')
    elif re.findall(r'цен.*|стоим.*|стоит', message.text):
        await send_log('INFO', message.from_user.username, 'Вопрос распознан | Тематика стоимость | Сообщение: {}'.format(message.text))
        cost_answers = ['Цены приятные', 'Цены доступные', 'Цены не кусаются', 'Цены симпатичные', 'Цены привлекательные']
        await bot.send_message(message.from_user.id, random.choice(cost_answers), parse_mode='html', reply_markup=InlineKeyboardMarkup().add(inline_make_order))
    elif re.findall(r'добраться.*|добр.*|доеха.*|дойти|находит.*', message.text):
        await send_log('INFO', message.from_user.username, 'Вопрос распознан | Тематика как добраться | Сообщение: {}'.format(message.text))
        await bot.send_message(message.from_user.id, f"🚕 Я могу помочь вам вызвать такси, по кнопке ниже\n\n"
                                                     f"📌 Или же вы можете добраться сами, мы находимся по адресу:\n"
                                                     f"<b>{config['contacts']['address']}</b>", parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Проложить маршрут', url=config['taxi_api_url'])))
    else:
        await send_log('WARNING', message.from_user.username, 'Неизвестный запрос | Сообщение: {}'.format(message.text))
        await bot.send_message(message.from_user.id, f"К сожалению, я не знаю, что на это ответить, попробуйте найти, что вас интересует в меню.", parse_mode='html', reply_markup=inline_main_menu)

