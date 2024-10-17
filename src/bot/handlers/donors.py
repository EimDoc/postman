from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiomysql import OperationalError
from src.bot.create_bot import BotData
from src.entities.callback_data import DeleteDonor, TagData
from src.bot.keyboards.all_keyboards import donor_kb, back_to_menu_kb, delete_donor_kb, send_channel_kb, tags_list_kb, \
    menu_kb
from src.bot.utils.my_utils import create_donor_text, choose_tags_for_channel

donor_router = Router()


class AddDonor(StatesGroup):
    get_channel = State()
    get_tag = State()


@donor_router.callback_query(F.data == "donors")
async def donor_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите действие для каналов-доноров:", reply_markup=donor_kb())


@donor_router.callback_query(F.data == "check_donor")
async def check_donors_handler(callback_query: CallbackQuery):
    try:
        donors = await BotData.donor_db.read_donors()
        text = create_donor_text(donors)

        await callback_query.message.reply(text=text, reply_markup=back_to_menu_kb())
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе", reply_markup=ReplyKeyboardRemove())


@donor_router.callback_query(F.data == "delete_donor")
async def start_delete_donor_handler(callback_query: CallbackQuery):
    try:
        donors = await BotData.donor_db.read_donors()
        await callback_query.message.edit_text("Выберите связку для удаления:", reply_markup=delete_donor_kb(donors))
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе", reply_markup=ReplyKeyboardRemove())


@donor_router.callback_query(DeleteDonor.filter())
async def end_delete_donor_handler(callback_query: CallbackQuery, callback_data: DeleteDonor):
    try:
        donor_id = callback_data.donor_id
        await BotData.donor_db.delete_donor(donor_id)

        donors = await BotData.donor_db.read_donors()
        await callback_query.message.delete()
        await callback_query.message.answer("Выберите связку для удаления:", reply_markup=delete_donor_kb(donors))
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе", reply_markup=ReplyKeyboardRemove())


@donor_router.callback_query(F.data == "add_donor")
async def start_add_donor_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выберите канал для добавления:", reply_markup=send_channel_kb())
    await state.set_state(AddDonor.get_channel)


@donor_router.message(AddDonor.get_channel, F.chat_shared)
async def get_channel_handler(message: Message, state: FSMContext):
    await choose_tags_for_channel(message, state, AddDonor.get_tag)


@donor_router.callback_query(TagData.filter(), AddDonor.get_tag)
async def end_add_donor_handler(callback_query: CallbackQuery, callback_data: TagData, state: FSMContext):
    try:
        state_data = await state.get_data()
        await BotData.donor_db.add_donor(state_data["channel_id"], state_data["channel_name"], callback_data.tag_id)

        await callback_query.message.answer("Новая пара донор-ключ добавлена", reply_markup=ReplyKeyboardRemove())
        await callback_query.message.reply("Воспользуйтесь меню:", reply_markup=menu_kb())
    except OperationalError:
        await callback_query.message.answer("ERROR: ошибка при записи пары донор-ключ", reply_markup=ReplyKeyboardRemove())
    finally:
        await state.clear()
