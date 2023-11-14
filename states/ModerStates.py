from aiogram.dispatcher.filters.state import StatesGroup, State


# Выкладывание поста в канал модераторами
class PostState(StatesGroup):
    photo = State()
    title = State()
    # description = State()
    price = State()
    confirm = State()
