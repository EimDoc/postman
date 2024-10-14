from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiomysql import OperationalError
from src.bot.keyboards.all_keyboards import receivers_kb, back_to_menu_kb, delete_receiver_kb, send_channel_kb, tags_list_kb, menu_kb
from src.bot.create_bot import BotData
from src.bot.utils.my_utils import create_receiver_text
from src.entities.callback_data import DeleteReceiver, TagData


receive_router = Router()


class AddReceiver(StatesGroup):
    get_channel = State()
    get_tag = State()


@receive_router.callback_query(F.data == "receivers")
async def receivers_handler(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите действие для каналов-получателей:", reply_markup=receivers_kb())


@receive_router.callback_query(F.data == "check_receivers")
async def check_receivers_handler(callback_query: CallbackQuery):
    try:
        receivers = await BotData.receiver_db.read_receivers()
        text = create_receiver_text(receivers)

        await callback_query.message.reply(text=text, reply_markup=back_to_menu_kb())
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе")


@receive_router.callback_query(F.data == "delete_receiver")
async def start_delete_receiver_handler(callback_query: CallbackQuery):
    try:
        receivers = await BotData.receiver_db.read_receivers()
        await callback_query.message.edit_text("Выберите связку для удаления:", reply_markup=delete_receiver_kb(receivers))
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе")


@receive_router.callback_query(DeleteReceiver.filter())
async def end_delete_receiver_handler(callback_query: CallbackQuery, callback_data: DeleteReceiver):
    try:
        receiver_id = callback_data.receiver_id
        await BotData.receiver_db.delete_receiver(receiver_id)

        receivers = await BotData.receiver_db.read_receivers()
        await callback_query.message.delete()
        await callback_query.message.answer("Выберите связку для удаления:", reply_markup=delete_receiver_kb(receivers))
    except OperationalError:
        await callback_query.message.reply("ERROR: ошибка при sql запросе")


@receive_router.callback_query(F.data == "add_receiver")
async def start_add_receiver_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выберите канал для добавления:", reply_markup=send_channel_kb())
    await state.set_state(AddReceiver.get_channel)


@receive_router.message(AddReceiver.get_channel)
async def get_channel_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(channel_id=message.chat_shared.chat_id, channel_name=message.chat_shared.title)

        tags = await BotData.tag_db.read_tags()
        if len(tags) > 0:
            await message.answer("Выберите тег для канала:", reply_markup=tags_list_kb(tags))
            await state.set_state(AddReceiver.get_tag)
        else:
            await message.answer("ERROR: У вас нет тегов! Добавьте их чтобы создать пару донор-тег", reply_markup=ReplyKeyboardRemove())
            await state.clear()
            await message.answer("Воспользуйтесь меню", reply_markup=menu_kb())
    except OperationalError:
        await message.reply("ERROR: ошибка при sql запросе")
        await state.clear()
    except Exception:
        await message.answer("Ошибка при получении канала")
        await state.clear()


@receive_router.callback_query(TagData.filter(), AddReceiver.get_tag)
async def end_add_receiver_handler(callback_query: CallbackQuery, callback_data: TagData, state: FSMContext):
    try:
        state_data = await state.get_data()
        await BotData.receiver_db.add_receiver(state_data["channel_id"], state_data["channel_name"], callback_data.tag_id)
        await callback_query.message.answer("Новая пара получатель-ключ добавлена", reply_markup=ReplyKeyboardRemove())
        await callback_query.message.reply("Воспользуйтесь меню:", reply_markup=menu_kb())
    except OperationalError:
        await callback_query.message.answer("ERROR: ошибка при записи пары донор-ключ")
    finally:
        await state.clear()
