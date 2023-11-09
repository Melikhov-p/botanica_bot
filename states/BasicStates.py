from aiogram.dispatcher.filters.state import StatesGroup, State


# Создание заказа
class OrderState(StatesGroup):
    products = State()
    ready_date = State()
    delivery = State()
    delivery_date = State()
    contact = State()
    confirm = State()
