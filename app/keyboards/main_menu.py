# app/keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    buttons = [
        KeyboardButton("/transfer"),
        KeyboardButton("/referrals"),
        KeyboardButton("/balance"),
        KeyboardButton("/buy_points"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
