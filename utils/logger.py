from datetime import datetime


async def send_log(type: str = 'INFO', customer: str = 'BOT', message: str = ''):
    print(f"[{type}]:{datetime.now().strftime('%Y-%m-%d %H:%M')} | @{customer} : {message}")
