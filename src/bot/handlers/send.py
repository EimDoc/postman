import logging
from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State

from src.bot.create_bot import BotData
from src.entities.entities import News
from src.entities.callback_data import AcceptNews, RejectNews, RephraseNews
from src.bot.keyboards.all_keyboards import accepted_kb, rejected_kb

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='postman.log', filemode='a')
logger = logging.getLogger(__name__)

send_router = Router()


class FSMRephrase(StatesGroup):
    header_input = State()
    text_input = State()


async def send_news_to_moderation(data: dict):
    news = News(data)
    media = news.media
    keyboard = news.keyboard
    await BotData.bot.send_media_group(BotData.MODERATION_ID, media=media.build())
    await BotData.bot.send_message(
        BotData.MODERATION_ID,
        f"Действия с новостью <b>{news.header}</b>:",
        reply_markup=keyboard
    )


@send_router.callback_query(AcceptNews.filter())
async def accept_news(query: types.CallbackQuery, callback_data: AcceptNews):
    await BotData.bot.edit_message_text(
        chat_id=BotData.MODERATION_ID,
        message_id=query.message.message_id,
        text=query.message.text,
        reply_markup=accepted_kb()
    )
    news = News.get_instance(callback_data.news_id)

    await send_news_to_channels(news=news)


@send_router.callback_query(RejectNews.filter())
async def reject_news(query: types.CallbackQuery, callback_data: AcceptNews):
    await BotData.bot.edit_message_text(
        chat_id=BotData.MODERATION_ID,
        message_id=query.message.message_id,
        text=query.message.text,
        reply_markup=rejected_kb()
    )
    news = News.get_instance(callback_data.news_id)
    news_id = news.id
    try:
        logger.info(f"Deleting {news_id}")
        del news
        logger.info(f"Succesfully deleted {news_id}")
    except Exception as e:
        logger.error(e)


@send_router.callback_query(RephraseNews.filter())
async def rephrase_news(query: types.CallbackQuery, callback_data: AcceptNews):
    await BotData.bot.edit_message_text(
        chat_id=BotData.MODERATION_ID,
        message_id=query.message.message_id,
        text=query.message.text,
        reply_markup=rejected_kb()
    )
    news = News.get_instance(callback_data.news_id)
    del news


async def send_news_to_channels(news: News):
    tag_id = news.tag_id
    if tag_id is not None:
        channels = await BotData.receiver_db.get_receivers_by_tag(tag_id)
        for channel in channels:
            await BotData.bot.send_media_group(chat_id=channel, media=news.media.build())
            logger.info(f"Sended news \"{news.header}\" to {channel}")
    del news
