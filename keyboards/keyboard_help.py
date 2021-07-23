# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой выбора команд.
"""
from telebot import types


def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры помощи комманд.
    Возвращает: Клавиатуру выбора команды.
    """
    keyboard_help = types.ReplyKeyboardMarkup(row_width=3)
    button_set = types.KeyboardButton('/set')
    button_settings = types.KeyboardButton('/settings')
    button_help = types.KeyboardButton('/help')
    keyboard_help.add(button_set, button_settings, button_help)
    return keyboard_help
