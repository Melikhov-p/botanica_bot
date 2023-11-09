import asyncio
import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_keyboards import inline_confirm_reject_kb
from loader import dp, bot, config
from aiogram import types
from states.BasicStates import OrderState

# --- СЦЕНАРИЙ СОЗДАНИЯ ЗАКАЗА --- #
@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), lambda callback: callback.data == 'make_order')
async def process_callback_start_make_order(callback: types.CallbackQuery):
    await OrderState.products.set()
    await bot.send_message(callback.from_user.id, f"Какой букет вы бы хотели заказать?\n\n"
                                                  f"Опишите ваш идеальный букет", parse_mode='html')


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.products)
async def process_message_get_ready_order_date(message: types.Message, state: FSMContext):
    await state.update_data(products=message.text)
    await OrderState.ready_date.set()
    await bot.send_message(message.from_user.id, f"Когда заказ должен быть готов?")


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.ready_date)
async def process_message_need_delivery(message: types.Message, state: FSMContext):
    await state.update_data(ready_date=message.text)
    await OrderState.delivery.set()
    await bot.send_message(message.from_user.id, 'Доставка или самовывоз?', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Доставка', callback_data='inline_delivery_true'),
                                                                                                                    InlineKeyboardButton('Самовывоз', callback_data='inline_delivery_false')))


@dp.callback_query_handler(lambda callback: callback.data == 'inline_delivery_true' or callback.data == 'inline_delivery_false',
                           ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.delivery)
async def process_callback_get_delivery_date_order(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'inline_delivery_true':
        await state.update_data(delivery='нужна')
        await OrderState.delivery_date.set()
        await bot.send_message(callback.from_user.id, f"Когда доставить?")
    else:
        await state.update_data(delivery='не нужна')
        await state.update_data(delivery_date='')
        await OrderState.contact.set()
        await bot.send_message(callback.from_user.id, f"Оставьте ваш номер телефона для связи.")


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.delivery_date)
async def process_message_get_contact(message: types.Message, state: FSMContext):
    await state.update_data(delivery_date=message.text)
    await OrderState.contact.set()
    await bot.send_message(message.from_user.id, f"Оставьте ваш номер телефона для связи.")


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.contact)
async def process_message_confirm_order(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    order_data = await state.get_data()
    await OrderState.confirm.set()
    await bot.send_message(message.from_user.id, f"Итак, проверим заказ\n\n"
                                                 f"💐 Ваш идеальный букет: {order_data['products']}\n\n"
                                                 f"➡ Заказ должен быть готов: {order_data['ready_date']}\n\n"
                                                 f"🚕 Доставка: {order_data['delivery']} {order_data['delivery_date']}\n\n"
                                                 f"📞 Контактный номер: {order_data['contact']}")
    await bot.send_message(message.from_user.id, 'Все верно?', reply_markup=inline_confirm_reject_kb)


@dp.callback_query_handler(lambda c: c.data == 'confirm_yes', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.confirm)
async def process_order_confirmed(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(confirm=callback.data)
    order_data = await state.get_data()
    for admin in config['admins']:
        await bot.send_message(admin, f"🔴 Новый заказ 🔴 : @{callback.from_user.username} : {callback.from_user.id}\n\n"
                                      f"📦 Состав заказа: {order_data['products']}\n\n"
                                      f"➡️ Заказ должен быть готов {order_data['ready_date']}\n\n"
                                      f"🚕 Доставка {order_data['delivery']} {order_data['delivery_date']}\n\n"
                                      f"📞 Контактный номер: {order_data['contact']}")
    await bot.send_message(callback.from_user.id, 'Заказ успешно создан, скоро с вами свяжутся для подтверждения.\n\n'
                                                  'Для возврата в меню /menu', parse_mode='html')
    await state.finish()
@dp.callback_query_handler(lambda c: c.data == 'confirm_no', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=OrderState.confirm)  # Если окончательную информацию не подтвердили
async def process_decline_send_beat_in_channel(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, f'Ладно, попробуем ещё раз.', parse_mode='html')
    await state.finish()
    await process_callback_start_make_order(callback)
