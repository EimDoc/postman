import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from aiogram.client.session.aiohttp import AiohttpSession
from dataclasses import dataclass
from typing import Final
from src.database.db import DonorCommands, TagsCommands, ReceiversCommands
from src.entities.clients import Publisher, Consumer

session = AiohttpSession()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass(frozen=True, init=False)
class BotData:
    bot: Final[Bot] = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    dp: Final[Dispatcher] = Dispatcher(storage=MemoryStorage())
    donor_db: Final[DonorCommands] = DonorCommands()
    tag_db: Final[TagsCommands] = TagsCommands()
    receiver_db: Final[ReceiversCommands] = ReceiversCommands()
    publisher = Publisher()
    consumer = Consumer()
    MODERATION_ID: Final[int] = -4545511074


@dataclass(init=False)
class Toggles:
    send_news: bool = True
    auto_accept: bool = False
