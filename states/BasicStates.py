from aiogram.dispatcher.filters.state import StatesGroup, State


# Создание заказа
class OrderState(StatesGroup):
    products = State()
    is_products_photo = State()
    ready_date = State()
    delivery = State()
    delivery_address = State()
    delivery_recipient = State()
    contact = State()
    confirm = State()
