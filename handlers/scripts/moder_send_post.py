from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from utils.logger import send_log
from keyboards.inline_keyboards import inline_confirm_reject_kb, inline_post_confirm_send, inline_channel_post_keyboard
from keyboards.keyboard_generator import keyboard_generator
from loader import dp, bot, config
from aiogram import types
from states.ModerStates import PostState


@dp.callback_query_handler(lambda c: c.data == 'cancel_create_post', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_cancel_create_post(callback: types.CallbackQuery, state: FSMContext):
    await send_log('MODER', callback.from_user.username, 'Отменил создание поста')
    await state.finish()
    await callback.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'create_post', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'])
async def moders_command_send_post(callback: types.CallbackQuery, state: FSMContext):
    keyboard = {'post_photo': 'Добавить фото', 'post_title': 'Добавить заголовок', 'post_price': 'Добавить цену', 'post_preview': 'Предпросмотр', 'cancel_create_post': 'Отмена'}
    post_data = await state.get_data()
    if post_data.get('photo'):
        keyboard['post_photo'] = 'Фото добавлено'
    if post_data.get('title'):
        keyboard['post_title'] = 'Заголовок добавлен'
    # if post_data.get('description'):
    #     keyboard['post_description'] = 'Описание добавлено'
    if post_data.get('price'):
        keyboard['post_price'] = 'Цена добавлена'
    await bot.send_message(callback.from_user.id, f"📋 Создание поста\n\n"
                                                  f"<b>Обратите внимание, бот поддерживает посты только с <u>одной</u> фотографией</b>\n\n"
                                                  f"Опубликовать пост возможно <u>только</u> из предпросмотра.\n\n", reply_markup=keyboard_generator(keyboard), parse_mode='html')


@dp.callback_query_handler(lambda c: c.data == 'post_photo', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_callback_set_post_photo(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Добавьте фотографию для поста')
    await PostState.photo.set()
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=PostState.photo, content_types=['photo'])
async def moders_message_send_post_photos(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await send_log('MODER', message.from_user.username, 'Добавил фотографию для поста')
    await moders_command_send_post(message, state)


@dp.callback_query_handler(lambda c: c.data == 'post_title', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_callback_set_post_title(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Введите заголовок поста')
    await PostState.title.set()
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=PostState.title)
async def moders_message_set_post_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await send_log('MODER', message.from_user.username, 'Добавил заголовок для поста')
    await moders_command_send_post(message, state)


# @dp.callback_query_handler(lambda c: c.data == 'post_description', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
# async def moders_callback_set_post_description(callback: types.CallbackQuery):
#     await bot.send_message(callback.from_user.id, 'Введите описание поста')
#     await PostState.description.set()
# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=PostState.description)
# async def moders_message_set_post_description(message: types.Message, state: FSMContext):
#     await state.update_data(description=message.text)
#     await send_log('MODER', message.from_user.username, 'Добавил описание для поста')
#     await moders_command_send_post(message, state)


@dp.callback_query_handler(lambda c: c.data == 'post_price', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_callback_set_post_price(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Введите цену поста')
    await PostState.price.set()
async def moders_message_set_post_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await send_log('MODER', message.from_user.username, 'Добавил цену для поста')
    await moders_command_send_post(message, state)


@dp.callback_query_handler(lambda c: c.data == 'post_price', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_callback_set_post_price(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Введите цену поста')
    await PostState.price.set()
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=PostState.price)
async def moders_message_set_post_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await send_log('MODER', message.from_user.username, 'Добавил цену для Поста')
    await moders_command_send_post(message, state)


@dp.callback_query_handler(lambda c: c.data == 'post_preview', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_callback_post_preview(callback: types.CallbackQuery, state: FSMContext):
    post_data = await state.get_data()
    if post_data.get('photo'):
        keyboard = {'send_post_to_channel': 'ОПУБЛИКОВАТЬ'}
        await bot.send_photo(callback.from_user.id, photo=post_data['photo'], caption=f"<b>{post_data.get('title', '')}</b>\n\n"
                                                                                      f"<i>📌 г. Белгород ул. Гражданский проспект 47\n"
                                                                                      f"📞 тел . 21-90-08\n"
                                                                                      f"📱 +7 (930) 086-90-08\n"
                                                                                      f"🚘 доставка по городу в любое время</i>\n\n"
                                                                                      f"<b>{post_data.get('price', '')}</b> ₽", parse_mode='html', reply_markup=keyboard_generator(keyboard))
    else:
        await bot.send_message(callback.from_user.id, 'Для предпросмотра поста необходимо добавить фотографию')


@dp.callback_query_handler(lambda c: c.data == 'send_post_to_channel', ChatTypeFilter(chat_type=types.ChatType.PRIVATE), chat_id=config['moders'], state='*')
async def moders_callback_send_post_to_channel(callback: types.CallbackQuery, state: FSMContext):
    post_data = await state.get_data()
    await bot.send_photo(config['channel_id'], photo=post_data['photo'], caption=f"<b>{post_data.get('title', '')}</b>\n\n"
                                                                                 f"<i>📌 г. Белгород ул. Гражданский проспект 47\n"
                                                                                 f"📞 тел . 21-90-08\n"
                                                                                 f"📱 +7 (930) 086-90-08\n"
                                                                                 f"🚘 доставка по городу в любое время</i>\n\n"
                                                                                 f"<b>{post_data.get('price', '')}</b> ₽", parse_mode='html', reply_markup=inline_channel_post_keyboard)
    await send_log('MODER', callback.from_user.username, 'Опубликовал пост {0}'.format(post_data.get('title', '')))
    await state.finish()
    await callback.message.edit_caption(f'{callback.message.caption}\n--------------------\n✅ОПУБЛИКОВАН✅', parse_mode='html')
