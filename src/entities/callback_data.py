from uuid import UUID
from aiogram.filters.callback_data import CallbackData


class DeleteDonor(CallbackData, prefix="delete_donor"):
    donor_id: int


class DeleteReceiver(CallbackData, prefix="delete_receiver"):
    receiver_id: int


class TagData(CallbackData, prefix="tag"):
    tag_id: int


class TagDelete(CallbackData, prefix="tag_delete"):
    tag_id: int


class AcceptNews(CallbackData, prefix="accept_news"):
    news_id: UUID


class RejectNews(CallbackData, prefix="reject_news"):
    news_id: UUID


class RephraseNews(CallbackData, prefix="rephrase_news"):
    news_id: UUID


class SwitchToggleCallback(CallbackData, prefix="switch_toggle"):
    toggle_name: str
