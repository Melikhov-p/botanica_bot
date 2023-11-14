from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            # types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('menu', 'Вызвать основное меню'),
            types.BotCommand('cancel', 'Отмена / Выход из сценария'),
            types.BotCommand('report', 'Возникли проблемы с ботом?'),
        ]
    )
