import sqlite3
import config

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_chat_id):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT state FROM User WHERE user_chat_id=?", (user_chat_id,))
        try:
            return cur.fetchone()[0]
        except TypeError:
            return config.States.S_START

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_chat_id, state):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        #Проверка на наличие user_chat_id в БД
        if cur.execute("SELECT user_chat_id FROM User WHERE user_chat_id=?", (user_chat_id,)).fetchone():
            #Обновляем значение state для полльзователя user_chat_id
            cur.execute("UPDATE User SET state = ? WHERE user_chat_id = ?", (state,user_chat_id))
        else:
            #Добавляем пользователя в БД
            cur.execute( "INSERT or IGNORE INTO User (user_chat_id, state) VALUES (?,?)", (user_chat_id, state) )
        conn.commit()

def set_notification_state(user_chat_id, state):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE User SET notification_state = ? WHERE user_chat_id = ?", (state,user_chat_id))
        conn.commit()

def set_notification_time(user_chat_id, time):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE User SET notification_time = ? WHERE user_chat_id = ?", (time,user_chat_id))
        conn.commit()

def set_notification_member(user_chat_id, company):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        cur.execute( "INSERT or IGNORE INTO Member (user_id, company_id) VALUES (?,?)", (user_id, company) )
        conn.commit()