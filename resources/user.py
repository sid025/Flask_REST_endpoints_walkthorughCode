import sqlite3
from flask_restful import Resource
from flask_restful import reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp

from flask_jwt_extended import create_access_token,create_refresh_token,jwt_refresh_token_required,get_jwt_identity

_user_parser = reqparse.RequestParser()  # will validate the incoming request ( can also be used with form validation )
_user_parser.add_argument("username", type=str, required=True, help="This is a required field")
_user_parser.add_argument("password", type=str, required=True, help="This is a required field")


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

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

class UserLogin(Resource):

    @classmethod
    def post(cls):
        # Get data from parser
        data= _user_parser.parse_args()

        # Find user in database
        user=UserModel.find_by_username(data['username'])

        # Check password, this is what authentication() from flask_JWT used to do
        if user and safe_str_cmp(user.password,data['password']):
        # identity= is what the identity() from flask_JWT used to do
            access_token=create_access_token(identity=user.id, fresh=True)
            refresh_token=create_refresh_token(identity=user.id)

            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200

        return {'Error':'Invalid Credentials'},401

        # Create an access token
        # Create a refresh token
        # Return them

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        #After getting the identity we create 1 more access token using the refresh token and fresh=False meaning this is not the first time the user is login in
        # and we will be able to check if the token passed is fresh or not

        new_access_token=create_access_token(identity=current_user,fresh=False) # This create and unfresh token

        return {
            'access_token':new_access_token
        },200



