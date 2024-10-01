# app/keyboards/admin_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_menu():
    buttons = [
        KeyboardButton("/admin_stats"),
        KeyboardButton("/admin_ban"),
        KeyboardButton("/admin_unban"),
        KeyboardButton("/admin_restart"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
