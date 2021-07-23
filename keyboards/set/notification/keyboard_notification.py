# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой настройки уведомлений.
"""
from telebot import types


def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры уведомлений.
    Возвращает: клавиатуру настройки уведомлений.
    """
    keyboard_notification = types.InlineKeyboardMarkup(row_width=1)
    button_day = types.InlineKeyboardButton(text="Раз в день",
                                            callback_data="День")
    button_2days = types.InlineKeyboardButton(text="Раз в два дня",
                                            callback_data="2Дня")
    button_week = types.InlineKeyboardButton(text="Раз в неделю",
                                            callback_data="Неделя")
    keyboard_notification.add(button_day, button_2days, button_week)
    return keyboard_notification
