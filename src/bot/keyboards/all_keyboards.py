from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRequestChat
from typing import List
from src.entities.callback_data import DeleteDonor, TagData, TagDelete, DeleteReceiver


def menu_kb():
    kb_list = [
        [InlineKeyboardButton(text="Доноры", callback_data="donors"), InlineKeyboardButton(text="Получатели", callback_data="receivers")],
        [InlineKeyboardButton(text="Теги", callback_data="tags"), InlineKeyboardButton(text="Настройки", callback_data="settings")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def donor_kb():
    kb_list = [
        [InlineKeyboardButton(text="Просмотреть", callback_data="check_donor")],
        [InlineKeyboardButton(text="Добавить", callback_data="add_donor")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_donor")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_donor_kb(donors: List[tuple]):
    kb_list = []
    for donor in donors:
        donor_data = DeleteDonor(donor_id=int(donor[0])).pack()
        button = [InlineKeyboardButton(text=f"{donor[2]}:{donor[1]}", callback_data=donor_data)]
        kb_list.append(button)

    kb_list.append([InlineKeyboardButton(text="Меню", callback_data="menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def receivers_kb():
    kb_list = [
        [InlineKeyboardButton(text="Просмотреть", callback_data="check_receivers")],
        [InlineKeyboardButton(text="Добавить", callback_data="add_receiver")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_receiver")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_receiver_kb(receivers: List[tuple]):
    kb_list = []
    for receiver in receivers:
        receiver_data = DeleteReceiver(receiver_id=int(receiver[0])).pack()
        button = [InlineKeyboardButton(text=f"{receiver[2]}:{receiver[1]}", callback_data=receiver_data)]
        kb_list.append(button)

    kb_list.append([InlineKeyboardButton(text="Меню", callback_data="menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def tags_kb():
    kb_list = [
        [InlineKeyboardButton(text="Просмотреть", callback_data="check_tags")],
        [InlineKeyboardButton(text="Добавить", callback_data="add_tag")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete_tag")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def back_to_menu_kb():
    kb_list = [
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def send_channel_kb():
    kb_list = [
        [KeyboardButton(text="Выбрать канал", request_chat=KeyboardButtonRequestChat(
            request_id=1, chat_is_channel=True, request_title=True))],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def tags_list_kb(tags: List[tuple]):
    kb_list = []
    for tag in tags:
        tag_data = TagData(tag_id=tag[0]).pack()
        tag_button = [InlineKeyboardButton(text=tag[1], callback_data=tag_data)]
        kb_list.append(tag_button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_tag_kb(tags: List[tuple]):
    kb_list = []
    for tag in tags:
        tag_data = TagDelete(tag_id=tag[0]).pack()
        tag_button = [InlineKeyboardButton(text=tag[1], callback_data=tag_data)]
        kb_list.append(tag_button)

    kb_list.append([InlineKeyboardButton(text="Меню", callback_data="menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def accepted_kb():
    kb_list = [
        [InlineKeyboardButton(text="Принято ✅", callback_data="accepted")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def rejected_kb():
    kb_list = [
        [InlineKeyboardButton(text="Отклонено ❌", callback_data="rejected")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
