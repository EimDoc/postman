import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.bot.create_bot import BotData
from src.entities.entities import News
from src.entities.callback_data import AcceptNews, RejectNews, RephraseNews
from src.bot.keyboards.all_keyboards import accepted_kb, rejected_kb, choose_rephrase_way_kb, back_button_kb

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='postman.log', filemode='a')
logger = logging.getLogger(__name__)

send_router = Router()


class FSMRephrase(StatesGroup):
    choose_rephrase_way = State()
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
async def reject_news(query: types.CallbackQuery, callback_data: RejectNews):
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
async def start_rephrase_news(query: types.CallbackQuery, callback_data: RephraseNews, state: FSMContext):
    await state.set_state(FSMRephrase.choose_rephrase_way)
    await state.update_data(news_id=callback_data.news_id)
    await query.message.reply(text="Выберите способ перефразирования:", reply_markup=choose_rephrase_way_kb())
    await query.answer()


@send_router.callback_query(FSMRephrase.choose_rephrase_way, F.data == "gpt")
async def process_with_gpt(query: types.CallbackQuery, state: FSMContext):
    pass


@send_router.callback_query(FSMRephrase.choose_rephrase_way, F.data == "manually")
async def enter_header(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMRephrase.header_input)
    await query.message.reply("Введите заголовок новости:", reply_markup=back_button_kb())
    await query.answer()


@send_router.message(FSMRephrase.header_input)
async def enter_text(message: types.Message, state: FSMContext):
    await state.update_data(header=message.text)
    await state.set_state(FSMRephrase.text_input)
    await message.reply("Введите текст новости:", reply_markup=back_button_kb())


@send_router.message(FSMRephrase.text_input)
async def end_rephrase_news(message: types.Message, state: FSMContext):
    try:
        text = message.text
        data = await state.get_data()
        header = data["header"]
        news_id = data["news_id"]
        news = News.get_instance(news_id)
        news.header = header
        news.text = text
        await message.reply("Новость успешно перефразирована!")
        logger.info(f"Succesfully rephrased {news_id}")
    except TypeError:
        logger.error("TypeError accured while news rephrasing")
        await message.reply("Произошла ошибка при изменении новости")
    else:
        media = news.media
        keyboard = news.keyboard
        await BotData.bot.send_media_group(BotData.MODERATION_ID, media=media.build())
        await BotData.bot.send_message(
            BotData.MODERATION_ID,
            f"Действия с новостью <b>{news.header}</b>:",
            reply_markup=keyboard
        )
    finally:
        await state.clear()


async def send_news_to_channels(news: News):
    tag_id = news.tag_id
    if tag_id is not None:
        channels = await BotData.receiver_db.get_receivers_by_tag(tag_id)
        for channel in channels:
            await BotData.bot.send_media_group(chat_id=channel, media=news.media.build())
            logger.info(f"Sended news \"{news.header}\" to {channel}")
    await BotData.bot.send_message(BotData.MODERATION_ID, f"Новость \"{news.header}\" была успешно отправлена в каналы")
    del news
