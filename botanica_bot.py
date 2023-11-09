from aiogram import types
from aiogram.utils import executor
import logging
from loader import dp, bot
from utils.set_commands import set_default_commands
# Handlers
from handlers.users import command_handlers, callback_handlers
from handlers.scripts import make_order


@dp.callback_query_handler()
async def process_callback_idk_callback(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, f"Что-то пошло не так. Этого я ещё не знаю.", parse_mode='html')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
