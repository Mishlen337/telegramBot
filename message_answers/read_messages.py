"""
Модуль для чтения информации сообщения
"""
import sys
sys.path.insert(0, '.')
def get_message(path) -> str:
    """
    Цель: Прочитать сообщение из файла "path"
    Возвращает: Cтроку содержимого
    """
    f = open(f"./message_answers/{path}")
    message = f.read()
    f.close()
    return message
