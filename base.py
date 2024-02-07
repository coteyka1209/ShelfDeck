import sqlite3

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_exists(self, id):#проверяем, есть ли пользователь в бд
        with self.connection:
            result = self.cursor.execute('SELECT * FROM uinfos WHERE id = ?', (id,)).fetchall()
            return bool(len(result))

    def add_user(self, id, name, lname, usname):#добавляем пользователя в бд
        with self.connection:
            return self.cursor.execute("INSERT INTO uinfos (id, name, lname, usname) VALUES(?, ?, ?, ?)", (id, name, lname, usname))

    def get_uinfos(self): #получаем список всех пользователей
        with self.connection:
            result = self.cursor.execute('SELECT * FROM uinfos').fetchall()
            return result

    def update_name(self, id, name):#обновить имя
         with self.connection:
             return self.cursor.execute("UPDATE uinfos SET name = ? WHERE id = ?", (name, id))

    #обновить статус
    def update_status(self, id, status):#обновить статус
        with self.connection:
            return self.cursor.execute("UPDATE uinfos SET status = ? WHERE id = ?", (status, id))
        
    #обновить режим
    def update_mode(self, mode):#обновить статус
        with self.connection:
            return self.cursor.execute("UPDATE uinfos SET status = ? WHERE id = ?", (status, id))
    
    #получить статус
    def get_status(self, id): 
        with self.connection:
            result = self.cursor.execute('SELECT * FROM uinfos WHERE id = ?', (id,)).fetchall()
            return result[0][1]


    #получить usname
    def get_usname(self, id): 
        with self.connection:
            result = self.cursor.execute('SELECT usname FROM uinfos WHERE id = ?', (id,)).fetchall()
            if result:
                return result[0][0]
            else:
                return ""
            
        #получить имя
    def get_name(self, id): 
        with self.connection:
            result = self.cursor.execute('SELECT name FROM uinfos WHERE id = ?', (id,)).fetchall()
            if result:
                return result[0][0]
            else:
                return ""

    def close(self):
        self.connection.close()

