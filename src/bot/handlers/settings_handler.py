import logging
from aiogram import Router, types, F

from src.bot.create_bot import Toggles
from src.bot.keyboards.all_keyboards import settings_menu_kb
from src.entities.callback_data import SwitchToggleCallback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='postman.log', filemode='a')
logger = logging.getLogger(__name__)

settings_router = Router()


@settings_router.callback_query(F.data == "settings")
async def settings_menu_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Воспользуйтесь настройками:", reply_markup=settings_menu_kb())
    await callback_query.answer()


@settings_router.callback_query(SwitchToggleCallback.filter())
async def switch_toggle_handler(callback_query: types.CallbackQuery, callback_data: SwitchToggleCallback):
    setattr(Toggles, callback_data.toggle_name, not getattr(Toggles, callback_data.toggle_name))
    await callback_query.message.edit_text("Воспользуйтесь настройками:", reply_markup=settings_menu_kb())
    await callback_query.answer()
