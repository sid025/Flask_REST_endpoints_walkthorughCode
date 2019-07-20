import sqlite3

connection=sqlite3.connect('data.db')
cursor=connection.cursor()

create_table_users="CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)" #id INTEGER this will create auto-incrementing id
cursor.execute(create_table_users)

create_table_items="CREATE TABLE IF NOT EXISTS items(name text, price real)" #id INTEGER this will create auto-incrementing id
cursor.execute(create_table_items)


#user= (1,'bob','password')

user_list=[('bob','password'),('alice','password'),('sid','password')]
insert_table_users="INSERT INTO users VALUES (NULL,?,?)"

item_list=[('whey protein',1234.5),('whey protein 2',1224.5),('whey protein 3',1244.5)]
insert_table_items="INSERT INTO items VALUES (?,?)"


cursor.executemany(insert_table_users,user_list)
cursor.executemany(insert_table_items,item_list)


select_q="SELECT * FROM users"
result_set=(cursor.execute(select_q))

print(result_set.fetchall())

select_q="SELECT * FROM items"
result_set=(cursor.execute(select_q))

print(result_set.fetchall())


connection.commit()
connection.close()


