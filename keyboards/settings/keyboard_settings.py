# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой настроек.
"""
from telebot import types

def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры настроек.
    Возвращает: Клавиатуру настроек.
    """
    keyboard_settings = types.InlineKeyboardMarkup(row_width=1)
    button_companies = types.InlineKeyboardButton(text = "Изменить список компаний", 
                                                    callback_data = "НКомпании")
    button_notification = types.InlineKeyboardButton(text = "Отменить посылку уведомлений", 
                                                    callback_data = "НУведомления")
    keyboard_settings.add(button_companies, button_notification)
    return keyboard_settings
