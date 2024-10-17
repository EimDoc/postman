from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiomysql import OperationalError

from src.bot.keyboards.all_keyboards import menu_kb, tags_kb, back_to_menu_kb, delete_tag_kb
from src.bot.create_bot import BotData
from src.bot.utils.my_utils import create_tags_text
from src.bot.filters.all_filters import StopFilter
from src.entities.callback_data import TagDelete


start_router = Router()


class AddTag(StatesGroup):
    get_tag = State()


class DeleteTag(StatesGroup):
    get_tag = State()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Воспользуйтесь меню:", reply_markup=menu_kb())


@start_router.callback_query(F.data == "menu")
async def menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("Воспользуйтесь меню:", reply_markup=menu_kb())


@start_router.callback_query(F.data == "stop")
async def stop_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.reply("Действие прервано")


@start_router.message(F.text, StopFilter())
async def stop_message_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Действие прервано", reply_markup=menu_kb())


@start_router.callback_query(F.data == "tags")
async def tags_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Воспользуйтесь меню тегов:", reply_markup=tags_kb())


@start_router.callback_query(F.data == "check_tags")
async def check_tags(callback_query: CallbackQuery):
    tags = await BotData.tag_db.read_tags()

    text = create_tags_text(tags)
    await callback_query.message.reply(text, reply_markup=back_to_menu_kb())


@start_router.callback_query(F.data == "add_tag")
async def start_add_tag_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите новый тег:")
    await state.set_state(AddTag.get_tag)


@start_router.message(AddTag.get_tag)
async def end_add_tag_handler(message: Message, state: FSMContext):
    try:
        await BotData.tag_db.create_tag(message.text)
        await message.reply(f"Тег \"{message.text}\" добавлен", reply_markup=back_to_menu_kb())
    except OperationalError:
        await message.reply("ERROR: ошибка при sql запросе")
    finally:
        await state.clear()


@start_router.callback_query(F.data == "delete_tag")
async def start_delete_tag_handler(callback_query: CallbackQuery):
    try:
        tags = await BotData.tag_db.read_tags()
        await callback_query.message.edit_text("Выберите тег для удаления:", reply_markup=delete_tag_kb(tags))
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе")


@start_router.callback_query(TagDelete.filter())
async def end_delete_tag_handler(callback_query: CallbackQuery, callback_data: TagDelete):
    try:
        tag_id = callback_data.tag_id
        await BotData.tag_db.delete_tag(tag_id)

        tags = await BotData.tag_db.read_tags()
        await callback_query.message.delete()
        await callback_query.message.answer("Выберите тег для удаления:", reply_markup=delete_tag_kb(tags))
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе")