# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой выбора графика.
"""
from telebot import types


def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры графика.
    Возвраает: Клавиатуру выбора графика.
    """
    keyboard_graph = types.InlineKeyboardMarkup(row_width=1)
    button_gweek = types.InlineKeyboardButton(text="За неделю",
                                            callback_data="ГНеделя")
    button_gmonth = types.InlineKeyboardButton(text="За месяц",
                                            callback_data="ГМесяц")
    button_gyear = types.InlineKeyboardButton(text="За год",
                                            callback_data="ГГод")
    keyboard_graph.add(button_gweek, button_gmonth, button_gyear)
    return keyboard_graph
