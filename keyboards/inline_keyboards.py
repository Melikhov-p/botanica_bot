from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import config


# Главное меню
# inline_products = InlineKeyboardButton('💵 Рассказать цены на товары 💵', callback_data='all_products')
inline_make_order = InlineKeyboardButton('📫 Сделать заказ 📫', callback_data='make_order')
inline_contacts = InlineKeyboardButton('☎ Поделиться контактами ☎', callback_data='contacts')
inline_get_taxi = InlineKeyboardButton('🚕 Вызвать такси до магазина 🚕', callback_data='get_taxi')
inline_ask_question = InlineKeyboardButton('❓ Задать свой вопрос ❓', callback_data='ask_question')
inline_report = InlineKeyboardButton('❗ Возникли проблемы с ботом ❗', callback_data='report')
vk_button = InlineKeyboardButton('VK', url=config['links']['vk'])
inst_button = InlineKeyboardButton('Instagram', url=config['links']['instagram'])
inline_main_menu = InlineKeyboardMarkup(row_width=1)
inline_main_menu.add(inline_make_order, inline_contacts, inline_get_taxi, inline_ask_question, inline_report).row(vk_button, inst_button)


# Клавиатура Подтверждение/Отмена
inline_confirm = InlineKeyboardButton('Да', callback_data='confirm_yes')
inline_reject = InlineKeyboardButton('Нет', callback_data='confirm_no')
inline_confirm_reject_kb = InlineKeyboardMarkup(row_width=2)
inline_confirm_reject_kb.add(inline_confirm, inline_reject)


# Клавиатура Модераторов
inline_send_post = InlineKeyboardButton('Отправить пост', callback_data='create_post')
inline_mailing = InlineKeyboardButton('Отправить рассылку', callback_data='mailing')
inline_moder_keyboard = InlineKeyboardMarkup(row_width=1)
inline_moder_keyboard.add(inline_send_post, inline_mailing)


# Клавиатура создания поста
inline_post_photo = InlineKeyboardButton('Добавить фото', callback_data='post_photo')
inline_post_title = InlineKeyboardButton('Добавить заголовок', callback_data='post_title')
inline_post_description = InlineKeyboardButton('Добавить описание', callback_data='post_description')
inline_post_price = InlineKeyboardButton('Добавить цену', callback_data='post_price')
inline_post_preview = InlineKeyboardButton('Предпросмотр', callback_data='post_preview')
inline_post_confirm_send = InlineKeyboardMarkup(row_width=1)
inline_post_confirm_send.add(inline_post_photo, inline_post_title, inline_post_description, inline_post_price, inline_post_preview)


# Клавиатура для постов в канале
inline_channel_preorder_btn = InlineKeyboardButton('Предзаказ', callback_data='channel_preorder')
inline_channel_post_keyboard = InlineKeyboardMarkup(row_width=1)
inline_channel_post_keyboard.add(inline_channel_preorder_btn)



