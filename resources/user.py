import sqlite3
from flask_restful import Resource
from flask_restful import reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()  # will validate the incoming request ( can also be used with form validation )
    parser.add_argument("username", type=str, required=True, help="This is a required field")
    parser.add_argument("password", type=str, required=True, help="This is a required field")

    def post(self):
        data = UserRegister.parser.parse_args()

        #Checking if the username is already preent in the DB, in this implementation we consider "username" unique as "id" is always unique as
        #AUTO INCREMENT for ID is on
        if UserModel.find_by_username(data['username']):
            return ({'Message':'Duplicate username entered. Try again '},400)

        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            insert_user_query="INSERT INTO users VALUES(NULL,?,?)" # id column is NULL here as it is auto-incrementing
            cursor.execute(insert_user_query,(data['username'],data['password']))

            connection.commit()
            connection.close()
            return {"message":"User created successfully"},201

