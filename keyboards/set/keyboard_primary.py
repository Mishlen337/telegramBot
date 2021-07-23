# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой начальной клавиатурой.
"""
from telebot import types

def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация начальной клавиатуры
    Возвращает: Начальную клавиатуру
    """
    keyboard_primary = types.InlineKeyboardMarkup(row_width=1)
    button_theory = types.InlineKeyboardButton(text="Теория",
                                            callback_data="Теория")
    button_quote = types.InlineKeyboardButton(text="Получение одной котировки",
                                            callback_data="Котировка")
    button_graph = types.InlineKeyboardButton(text="Построение графика",
                                            callback_data="График")
    button_notification = types.InlineKeyboardButton(text="Настройка уведомлений",
                                            callback_data="Уведомление")
    keyboard_primary.add(button_theory, button_quote,
                        button_graph, button_notification)
    return keyboard_primary
