from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from functools import singledispatchmethod


class StopFilter(BaseFilter):
    def __init__(self, stop_words: str | list[str] = ("стоп", "отмена", "stop")):
        self.stop_words = stop_words

    async def __call__(self, message: Message):
        if isinstance(self.stop_words, str):
            return message.text.lower() == self.stop_words
        return message.text.lower() in self.stop_words
