import asyncio
from src.bot.create_bot import BotData
from src.bot.handlers.general import start_router
from src.bot.handlers.donors import donor_router
from src.bot.handlers.receivers import receive_router
from src.bot.handlers.send import send_router, send_news_to_channels


async def start_bot():
    BotData.dp.include_router(start_router)
    BotData.dp.include_router(donor_router)
    BotData.dp.include_router(receive_router)
    BotData.dp.include_router(send_router)
    await BotData.bot.delete_webhook(drop_pending_updates=True)
    await BotData.dp.start_polling(BotData.bot)

if __name__ == "__main__":
    asyncio.run(start_bot())
