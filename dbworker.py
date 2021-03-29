import sqlite3
import config
from datetime import datetime

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

def set_notification_state(user_chat_id:int, state:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE User SET notification_state = ? WHERE user_chat_id = ?", (state,user_chat_id))
        conn.commit()

def set_notification_time(user_chat_id:int, time: datetime):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE User SET notification_time = ? WHERE user_chat_id = ?", (time.strftime("%H:%M"),user_chat_id))
        conn.commit()

def set_notification_member(user_chat_id:int, company:str):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM Company WHERE symbol = ?", (company,))
        company_id = cur.fetchone()[0]
        cur.execute( "INSERT or IGNORE INTO Member (user_id, company_id) VALUES (?,?)", (user_id, company_id) )
        conn.commit()

def get_notification_list(user_chat_id:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT Company.name, Exchange.name 
                        FROM User JOIN Member JOIN Company JOIN Exchange 
                        ON Member.user_id = User.id AND Member.company_id = Company.id AND Company.exchange_id = Exchange.id 
                        WHERE User.user_chat_id = ?''', (user_chat_id,))
        rows = cur.fetchall()
        str_query = '\n'.join(map(' - '.join,rows))
        return str_query
#get_notification_list(4433)