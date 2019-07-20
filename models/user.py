import sqlite3

class UserModel:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password

    @classmethod
    def find_by_username(cls,name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * from users WHERE username=?"

        result=cursor.execute(query,(name,))
        row=result.fetchone()

        if row:
            user=cls(row[0],row[1],row[2]) # OR just do *row instead of (row[0],row[1],row[2])
        else:
            user=None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from users WHERE id=?"

        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(row[0], row[1], row[2])  # OR just do *row instead of (row[0],row[1],row[2])
        else:
            user = None

        connection.close()
        return user
