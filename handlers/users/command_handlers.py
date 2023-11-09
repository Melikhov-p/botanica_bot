from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from loader import dp, bot, config
from aiogram import types
from keyboards.inline_keyboards import inline_main_menu


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start', 'menu'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"🌸 Я Botanica Bot 🌸\n\n"
                                                 f"⬇️ Вот что я могу: ⬇️", parse_mode='html', reply_markup=inline_main_menu)


# Команда выход из любого сценария
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['cancel'], state='*')
async def process_cancel_command(message: types.Message, state: FSMContext):
    await state.finish()
    await process_start_command(message)

