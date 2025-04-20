import sqlite3
from config import DATABASE

class Database_Manager:
    def __init__(self, database):
        self.database = database    

    def get_id(self, question):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f'SELECT id FROM faq WHERE question = ? and Is_Closed = 0',(question,))
        return cur.fetchall()
    
    def is_closed(self, qstid):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f'SELECT Is_Closed FROM faq WHERE id = ?',(qstid,))
        return cur.fetchall()
    def update_Closed(self,data):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE faq SET Is_Closed = 1 WHERE id = ?",(data,)) 
        conn.commit()
    def update_answer(self,answer,data):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE faq SET answer = ? WHERE id = ?",(answer,data)) 
        conn.commit()

    def get_user_id(self, qstid):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f'SELECT user FROM faq WHERE id = ? and Is_Closed = 0',(qstid,))
        return cur.fetchall()
    
    def get_question(self, question):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(f'SELECT question FROM faq WHERE id = ? and Is_Closed = 0',(question,))
        return cur.fetchall()
    def get_all_id(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur. execute(f'SELECT id FROM faq')
        return cur.fetchall()
    
    def admin_id(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur. execute(f'SELECT chat_id FROM admins')
        return cur.fetchall()
    def add_user_answer(self,user_id, question):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('INSERT INTO faq (user, question, answer, Is_Closed) VALUES (?, ?,?,?)', (user_id, question, 'no response', 0))
            conn.commit()
if __name__ == '__main__':
    manager2 = Database_Manager(DATABASE)