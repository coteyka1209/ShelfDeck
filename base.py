import sqlite3
import time

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_exists(self, id):#проверяем, есть ли пользователь в бд
        with self.connection:
            result = self.cursor.execute('SELECT * FROM uinfos WHERE id = ?', (id,)).fetchall()
            return bool(len(result))

    def add_user(self, id, name, lname, usname, status):#добавляем пользователя в бд
        with self.connection:
            return self.cursor.execute("INSERT INTO uinfos (id, name, lname, usname, status) VALUES(?, ?, ?, ?, ?)", (id, name, lname, usname, status))

    def get_uinfos(self): #получаем список всех пользователей
        with self.connection:
            result = self.cursor.execute('SELECT * FROM uinfos').fetchall()
            return result


    #обновить статус администратора
    def update_admin(self, id, admin):
        with self.connection:
            return self.cursor.execute("UPDATE uinfos SET admin = ? WHERE id = ?", (admin, id))

    #получить статус администратора
    def get_admin(self, id): 
        with self.connection:
            result = self.cursor.execute('SELECT * FROM uinfos WHERE id = ?', (id,)).fetchall()
            return result[0][3]
    
    
    #обновить координаты
    def new_coords(self,id, user_x, user_y):
        with self.connection:
            self.cursor.execute("UPDATE uinfos SET user_x = ? WHERE id = ?", (user_x, id))
            return self.cursor.execute("UPDATE uinfos SET user_y = ? WHERE id = ?", (user_y, id))
           
    def get_coords(self, id):
        result = self.cursor.execute('SELECT * FROM uinfos WHERE id = ?', (id,)).fetchall()
        return result[0][5], result[0][6]
    

    #обновить статус
    def update_status(self, id, status):#обновить статус
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
    
    def update_usname(self, id, usname):#обновить usname
        with self.connection:
            return self.cursor.execute("UPDATE uinfos SET usname = ? WHERE id = ?", (usname, id))


    #получить lname
    def get_lname(self, id): 
        with self.connection:
            result = self.cursor.execute('SELECT lname FROM uinfos WHERE id = ?', (id,)).fetchall()
            if result:
                return result[0][0]
            else:
                return ""
            
    def update_lname(self, id, lname):#обновить lname
         with self.connection:
             return self.cursor.execute("UPDATE uinfos SET lname = ? WHERE id = ?", (lname, id))


        #получить имя
    def get_name(self, id):
            with self.connection:
                result = self.cursor.execute('SELECT name FROM uinfos WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return ""
    
    def update_name(self, id, name):#обновить имя
         with self.connection:
             return self.cursor.execute("UPDATE uinfos SET name = ? WHERE id = ?", (name, id,))
    
    def update_id_money(self, id):#добавляем пользователя в бд
        with self.connection:
            return self.cursor.execute("INSERT INTO money (id) VALUES(?)", (id,))
    
    #Получение денег
    def get_R1 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R1 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
    def get_R2 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R2 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
    def get_R5 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R5 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None    
                
    def get_R10 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R10 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
                
    def get_R50 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R50 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
                
    def get_R100 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R100 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
    
    def get_R200 (self, id):
        with self.connection:
            result = self.cursor.execute('SELECT R200 FROM money WHERE id = ?', (id,)).fetchone()
            if result:
                return result[0]
            else:
                return None
            
    def get_R500 (self, id):
        with self.connection:
            result = self.cursor.execute('SELECT R500 FROM money WHERE id = ?', (id,)).fetchone()
            if result:
                return result[0]
            else:
                return None
    def get_R1000 (self, id):
        with self.connection:
            result = self.cursor.execute('SELECT R1000 FROM money WHERE id = ?', (id,)).fetchone()
            if result:
                return result
            else:
                return "Ошибка!"
            
    def get_R2000 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R2000 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
                
    def get_R5000 (self, id):
            with self.connection:
                result = self.cursor.execute('SELECT R5000 FROM money WHERE id = ?', (id,)).fetchone()
                if result:
                    return result[0]
                else:
                    return None
    
    
    
    def close(self):
        self.connection.close()


