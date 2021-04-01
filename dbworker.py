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

def get_notification_state(user_chat_id:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT notification_state FROM User WHERE user_chat_id = ?", (user_chat_id,))
        return cur.fetchone()[0]

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

def set_notification_member(user_chat_id:int, name:str):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM Company WHERE name = ?", (name,))
        company_id = cur.fetchone()[0]
        cur.execute( "INSERT or IGNORE INTO Member (user_id, company_id) VALUES (?,?)", (user_id, company_id) )
        conn.commit()

def get_notification_list(user_chat_id:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT Company.name, Company.symbol, Exchange.name 
                        FROM User JOIN Member JOIN Company JOIN Exchange 
                        ON Member.user_id = User.id AND Member.company_id = Company.id AND Company.exchange_id = Exchange.id 
                        WHERE User.user_chat_id = ?''', (user_chat_id,))
        rows = cur.fetchall()
        str_query = '\n'.join(map(' - '.join,rows))
        return str_query
    
def get_notification_companies(user_chat_id:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT Company.name
                        FROM User JOIN Member JOIN Company JOIN Exchange 
                        ON Member.user_id = User.id AND Member.company_id = Company.id AND Company.exchange_id = Exchange.id 
                        WHERE User.user_chat_id = ?''', (user_chat_id,))
        rows = cur.fetchall()
        return rows
#Удаление всех компаний в списке уведомлений
def delete_all_members(user_chat_id:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        cur.execute('''DELETE FROM Member WHERE user_id = ?''', (user_id,)) 
        conn.commit()

#Удаление выборочных компаний в списке уведомлений
def delete_selectively_member(user_chat_id:int, name:str):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM Company WHERE name = ?", (name,))
        company_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]

        #Проверка на существование пары (обрабатывается в bot.py через AttributeError)
        cur.execute("SELECT * FROM Member WHERE user_id = ? AND company_id = ?", (user_id,company_id))
        if not cur.fetchone():
            raise AttributeError

        cur.execute('''DELETE FROM Member WHERE user_id = ? AND company_id = ?''', (user_id,company_id)) 
        conn.commit()

def get_companies_list(short_name:str, offset:int):
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute(fr'''SELECT Company.name, Company.symbol, Exchange.name FROM Company JOIN Exchange ON Company.exchange_id = Exchange.id
                        WHERE Company.name LIKE '%{short_name}%' ORDER BY Company.id ASC LIMIT 5 OFFSET ?''', (offset,))
        companies = cur.fetchall()
        return companies

def get_company_ticker(name:str)->str:
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT symbol FROM Company WHERE name = ?",(name,))
        ticker = cur.fetchone()[0]
    return ticker
#print(get_company_ticker('Apple '))