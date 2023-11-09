import json

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

with open('config/botanicabot_config.json', 'r', encoding='utf8') as config_file:
    config = json.load(config_file)


bot = Bot(token=config['token'])
dp = Dispatcher(bot, storage=MemoryStorage())
