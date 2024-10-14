import asyncio
from src.api.postman_api import run_fastapi
from src.bot.aiogram_run import start_bot
from concurrent.futures import ThreadPoolExecutor
from src.bot.create_bot import BotData
from src.bot.handlers.send import send_news_to_channels


async def run_app():
    # await MySqlConnection("login_data") #rewritea
    await asyncio.gather(
        run_fastapi(),
        start_bot()
    )


if __name__ == "__main__":
    asyncio.run(run_app())

