from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import config


# Главное меню
inline_products = InlineKeyboardButton('💵 Рассказать цены на товары 💵', callback_data='all_products')
inline_make_order = InlineKeyboardButton('📫 Сделать заказ 📫', callback_data='make_order')
inline_contacts = InlineKeyboardButton('☎ Поделиться контактами ☎', callback_data='contacts')
inline_get_taxi = InlineKeyboardButton('🚕 Вызвать такси до магазина 🚕', callback_data='get_taxi')
inline_report = InlineKeyboardButton('❗ Возникли проблемы ❗', callback_data='report')
vk_button = InlineKeyboardButton('VK', url=config['links']['vk'])
inst_button = InlineKeyboardButton('Instagram', url=config['links']['instagram'])
inline_main_menu = InlineKeyboardMarkup(row_width=1)
inline_main_menu.add(inline_products, inline_make_order, inline_contacts, inline_get_taxi).row(vk_button, inst_button)


# Клавиатура Подтверждение/Отмена
inline_confirm = InlineKeyboardButton('Да', callback_data='confirm_yes')
inline_reject = InlineKeyboardButton('Нет', callback_data='confirm_no')
inline_confirm_reject_kb = InlineKeyboardMarkup(row_width=2)
inline_confirm_reject_kb.add(inline_confirm, inline_reject)
