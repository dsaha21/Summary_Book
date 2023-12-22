import sqlite3

class DataBaseFunction:
    def __init__(self, database_name="maindata.db"):
        self.connection = sqlite3.connect(database_name,check_same_thread=False)
        self.cursor = self.connection.cursor()
        #self.create_table()

    def create_table(self, table_name="newusers", columns="id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, passkey INTEGER, usertype TEXT"):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data(self,value1,value2,value3,value4, table_name="newusers"):
        query = f"INSERT INTO {table_name} (name, email, passkey, usertype) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query,(value1, value2, value3, value4))
        self.connection.commit()

    def get_mail_tabledata(self,uname,table_name="newusers"):
        q = f"SELECT email FROM {table_name} WHERE name='{uname}' ORDER BY id DESC LIMIT 1"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]
    def rowsofcol(self, column_name, table_name="newusers", condition=None):
        q = f"SELECT {column_name} FROM {table_name}"
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_the_usertype(self, uname, table_name="newusers"):
        q = f"SELECT usertype FROM {table_name} WHERE name='{uname}' "
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]

    def passcheck(self, uname, table_name='newusers'):
        q = f"SELECT passkey FROM {table_name} WHERE name='{uname}'"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]

    # def fetchbook(self, page_no, book_url, user_ID, table_name="bookdetails_time"):
    #     q = f"SELECT range FROM {table_name} WHERE bookurl='{book_url}' AND userID={user_ID} AND timetaken = (SELECT MAX(timetaken) FROM {table_name})";
    #     self.cursor.execute(q)
    #     return self.cursor.fetchall()
    # def booktable(self, table_name="bookdetails_time", columns="id INTEGER PRIMARY KEY AUTOINCREMENT,userID TEXT, bookurl TEXT, range TEXT, timetaken TEXT"):
    #     query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    #     self.cursor.execute(query)
    #     self.connection.commit()
    #
    # def bookinput(self, value1, value2, value3, value4, table_name="bookdetails_time"):
    #     query = f"INSERT INTO {table_name} (userID, bookurl, range, timetaken) VALUES (?, ?, ?, ?)"
    #     self.cursor.execute(query, (value1, value2, value3, value4))
    #     self.connection.commit()
    #=====================================================================================
    def fetchbook(self,page_no, book_url, table_name="testbookdetails"):
        q = f"SELECT summary_range FROM {table_name} WHERE bookurl='{book_url}' ORDER BY id DESC LIMIT 1"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]
    def booktable(self, table_name="testbookdetails", columns="id INTEGER PRIMARY KEY AUTOINCREMENT,bookurl TEXT, summary_range TEXT, whole_range TEXT, userID TEXT,timetaken TEXT"):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()

    def bookinput(self, value1, value2, value3, value4, value5, table_name="testbookdetails"):
        query = f"INSERT INTO {table_name} (bookurl, summary_range, whole_range, userID, timetaken) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (value1, value2, value3, value4, value5))
        self.connection.commit()

    def fetchbook_wholedict(self, book_url,table_name="testbookdetails"):
        q = f"SELECT whole_range FROM {table_name} WHERE bookurl='{book_url}' ORDER BY id DESC LIMIT 1"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]

    def last_time_user(self, userID, bookurl, table_name="testbookdetails"):
        q = f"SELECT timetaken FROM {table_name} WHERE bookurl='{bookurl}' ORDER BY id DESC LIMIT 1"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]
#===================================================================
    def time_table(self, table_name="TD", columns="id INTEGER PRIMARY KEY AUTOINCREMENT, userID TEXT, mailID TEXT, timetaken TEXT"):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()

    def time_input(self, value1, value2, value3, value4, table_name="TD"):
        query = f"INSERT INTO {table_name} (userID, mailID, timetaken, status) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (value1, value2, value3, value4))
        self.connection.commit()

    def fetch_time(self, userid, table_name="TD"):
        q = f"SELECT timetaken FROM {table_name} WHERE userID='{userid}' ORDER BY id DESC LIMIT 1"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]

    def fetch_status_timetable(self, uname, table_name="TD"):
        q = f"SELECT status FROM {table_name} WHERE userID='{uname}'"
        self.cursor.execute(q)
        return self.cursor.fetchone()[0]
    def set_status_timetable(self,blocked,uname, table_name="TD"):
        if blocked:
            q = f"UPDATE {table_name} SET status ='B' WHERE userID ='{uname}'"
        else:
            q = f"UPDATE {table_name} SET status ='UB' WHERE userID ='{uname}'"
        self.cursor.execute(q)
        self.connection.commit()

    def whether_blocked(self,uname,table_name="TD"):
        # q = f"SELECT status FROM {table_name} WHERE userID='{uname}'"
        # self.cursor.execute(q)
        # return self.cursor.fetchone()[0]
        q = f"SELECT status FROM {table_name} WHERE userID = ? LIMIT 1"
        self.cursor.execute(q, (uname,))
        result = self.cursor.fetchone()
        if result == "B":
            return True
        else:
            return False

    def update_time_timetable(self,uname,newtime,table_name="TD"):
        q = f"UPDATE {table_name} SET timetaken='{newtime}' WHERE userID='{uname}'"
        self.cursor.execute(q)
        self.connection.commit()
    def whether_name_timetable(self,uname,table_name="TD"):
        q = f"SELECT 1 FROM {table_name} WHERE userID = ? LIMIT 1"
        self.cursor.execute(q, (uname,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False


    def get_users_timetable(self,table_name="TD"):
        q = f"SELECT userID FROM {table_name}"
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_mails_timetable(self,table_name="TD"):
        q = f"SELECT mailID FROM {table_name}"
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_times_timetable(self,table_name="TD"):
        q = f"SELECT timetaken FROM {table_name}"
        self.cursor.execute(q)
        return self.cursor.fetchall()
    def get_statuses_timetable(self,table_name="TD"):
        q = f"SELECT status FROM {table_name}"
        self.cursor.execute(q)
        return self.cursor.fetchall()




    def create_blockedusers(self,table_name="blocked", columns="id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT"):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()
    def input_blockedusers(self, value1,table_name="blocked"):
        query = f"INSERT INTO {table_name} (userID) VALUES (?)"
        self.cursor.execute(query, (value1))
        self.connection.commit()
    def fetch_blockedusers(self,uname,table_name="blocked"):
        q = f"SELECT userID FROM {table_name} WHERE userID='{uname}'"
        self.cursor.execute(q)
        return self.cursor.fetchall()





    # def select_data(self, table_name, columns="*", condition=None):
    #     if condition:
    #         query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
    #     else:
    #         query = f"SELECT {columns} FROM {table_name}"
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()

    # def update_data(self, table_name, set_values, condition=None):
    #     if condition:
    #         query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
    #     else:
    #         query = f"UPDATE {table_name} SET {set_values}"
    #     self.cursor.execute(query)
    #     self.connection.commit()
    #
    def delete_data(self, table_name, condition=None):
        if condition:
            query = f"DELETE FROM {table_name} WHERE {condition}"
        else:
            query = f"DELETE FROM {table_name}"
        self.cursor.execute(query)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

# db = DataBaseFunction("maindata.db")
# # db.create_table("employee","id INTEGER PRIMARY KEY, name TEXT, age INTEGER")
# db.insert_data(2,"shshs",56)
