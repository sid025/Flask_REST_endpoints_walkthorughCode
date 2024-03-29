import sqlite3

class ItemModel:
    def __init__(self,name,price):
        self.name=name
        self.price=price

    def json(self):
        return {'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            #return {'item': {'name': row[0], 'price': row[1]}}, 200
            return ItemModel(row[0],row[1]) ################################# OR use *row
        return False

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"

        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()
