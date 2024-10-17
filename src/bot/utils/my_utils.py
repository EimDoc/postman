from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove
from pymysql import OperationalError

from src.bot.create_bot import BotData
from src.bot.keyboards.all_keyboards import tags_list_kb, menu_kb


def create_donor_text(donors):
    base = "Список каналов-доноров:\n"
    for i, donor in enumerate(donors):
        base += f"{i+1}. <b>{donor[2]}: {donor[1]}</b>\n"

    return base


def create_receiver_text(donors):
    base = "Список каналов-получателей:\n"
    for i, donor in enumerate(donors):
        base += f"{i+1}. <b>{donor[2]}: {donor[1]}</b>\n"

    return base


def create_tags_text(tags):
    base = "Список тегов:\n"
    for tag in tags:
        base += f"- <b>{tag[1]}</b>\n"

    return base


async def choose_tags_for_channel(message: Message, cur_state: FSMContext, next_state: State):
    try:
        await cur_state.update_data(channel_id=message.chat_shared.chat_id, channel_name=message.chat_shared.title)

        tags = await BotData.tag_db.read_tags()
        if len(tags) > 0:
            await message.answer("Выберите тег для канала:", reply_markup=tags_list_kb(tags))
            await cur_state.set_state(next_state)
        else:
            await message.answer("ERROR: У вас нет тегов! Добавьте их чтобы создать пару донор-тег",
                                 reply_markup=ReplyKeyboardRemove())
            await cur_state.clear()
            await message.answer("Воспользуйтесь меню", reply_markup=menu_kb())
    except OperationalError:
        await message.reply("ERROR: ошибка при sql запросе", reply_markup=ReplyKeyboardRemove())
        await cur_state.clear()
    except Exception:
        await message.answer("Ошибка при получении канала")
        await cur_state.clear()
