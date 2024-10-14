import uvicorn
from fastapi import FastAPI, Body
from src.bot.handlers.send import send_news_to_moderation

app = FastAPI()


@app.post("/send")
async def send(data=Body()):
    await send_news_to_moderation(data)


async def run_fastapi():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, loop="asyncio", reload=True)
    server = uvicorn.Server(config)
    await server.serve()
