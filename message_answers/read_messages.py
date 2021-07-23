"""
Модуль для чтения информации сообщения
"""
import sys
sys.path.insert(0, '.')
import config
def get_message(path) -> str:
    """
    Цель: Прочитать сообщение из файла "path"
    Возвращает: Cтроку содержимого
    """
    f = open(f"{config.message_answers_path}/{path}")
    message = f.read()
    f.close()
    return message
