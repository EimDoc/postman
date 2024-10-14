import uuid
from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from src.entities.callback_data import AcceptNews, RejectNews, RephraseNews


class DBConnection(ABC):
    @staticmethod
    @abstractmethod
    def _create_pool():
        pass

    @staticmethod
    @abstractmethod
    def get_pool():
        pass

    @staticmethod
    @abstractmethod
    def close(self):
        pass


class News:
    _instances = dict()

    def __init__(self, data: dict):
        try:
            self.__data = data
            self.__tag_id = data.get("news_tag_id")
            self.__media = None
            self.__text = None
            self.__header = None
            self.__keyboard = None
            self.__id = uuid.uuid4()
            News._instances[self.__id] = self
        except KeyError:
            del self

    @property
    def media(self) -> MediaGroupBuilder:
        if not self.__media:
            self.__media = self.__create_media()
        return self.__media

    def __create_media(self) -> MediaGroupBuilder:
        media = MediaGroupBuilder(caption=self.text)
        try:
            for elem in self.__data.get("news_data").get("media"):
                media.add(type=elem[1], media=elem[0])
        except KeyError:
            print("ERROR: отсутствие медиа в новости")
        return media

    @property
    def text(self) -> str:
        if not self.__text:
            try:
                text = f"<b>{self.header}</b>\n\n{self.__data.get('news_data').get('text')}"
                self.__text = text
            except KeyError:
                self.__text = "Ошибка получения текста новости"
        return self.__text

    @property
    def header(self) -> str:
        if not self.__header:
            try:
                self.__header = self.__data.get("news_data").get("header")
            except KeyError:
                self.__header = "Ошибка получения заголовка новости"
        return self.__header

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        if not self.__keyboard:
            self.__keyboard = self.__create_keyboard()
        return self.__keyboard

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def tag_id(self):
        return self.__tag_id

    def __create_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text="Принять ✅", callback_data=AcceptNews(news_id=self.__id).pack())
        builder.button(text="Отклонить ❌", callback_data=RejectNews(news_id=self.__id).pack())
        builder.button(text="Перефразировать 🔄", callback_data=RephraseNews(news_id=self.__id).pack())
        builder.adjust(2, 1)
        return builder.as_markup()

    @classmethod
    def get_instance(cls, instance_id: uuid.UUID):
        return cls._instances.get(instance_id, None)

    @classmethod
    def remove_instance(cls, instance_id: uuid.UUID):
        if instance_id in cls._instances:
            cls._instances.pop(instance_id, None)

    def __del__(self):
        self.remove_instance(self.__id)
