import uvicorn
from fastapi import FastAPI

from src.bot.handlers.send import send_news_to_moderation
from src.bot.create_bot import Toggles
from src.api.models import NewsModel

app = FastAPI()


@app.post("/send")
async def send(news: NewsModel):
    if Toggles.send_news:
        await send_news_to_moderation(news.model_dump())


async def run_fastapi():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, loop="asyncio", reload=True)
    server = uvicorn.Server(config)
    await server.serve()
