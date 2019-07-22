from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister,UserLogin,TokenRefresh, UserLogout
from resources.item import Item, ItemList
from blacklist import BLACKLIST


from flask_jwt_extended import JWTManager,jwt_required,get_jwt_claims

# If we import q module, all the code inside it gets executed while importing, that is why , in each module, we should mention to execute the code only when the code is run by that module by:
# if __name__=='__main__:' and only the module that is used to run i.e the module on which we right clock and run is assigned the '__main__' name


# Not all REST endpoint or so called resources should run on non-fresh token for example we might have critical endpoints like change-password ,etc.

app=Flask(__name__)
app.secret_key='cisco'
api=Api(app)
# Blacklisting users from access to resources
app.config['JWT_BLACKLIST_ENABLED']=True
# We enable the blacklist for both 'access' and 'refresh' types
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']




#item=[]

#JWT below create a new endpoint "/auth"
#When we call "/auth", we send it a username and a password and the JWT extension gets the username and password and send it over to
# "authenticate handler: (authenticate below) and identity handler: (identity below)
#jwt=JWT(app,authenticate,identity)

jwt=JWTManager(app) # Does not create /auth endpoint, we have to manually create it in the UserRegister resource
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity==1:
        return {'is_admin':True}
    else:
        return {
            'is_admin':False
        }


# If the token is blacklisted ( by means of blacklisted IDs here ), then this function ( if it returns True ) goes to @revoked_token_callback
# If false, it does nothing
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# When Flask-JWT-Extended realizes that the token that has been sent to us has expired ( usually 5 mins after create_access_token ), it calls the below method()
# in order for us to instruct Flask-JWT-Extended on what message needs to be sent out back to the client
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            'Description':'The token has expired.',
            'Error':'token_expired'
        }
    ),401

# The below function() is called when an invalid structure of token is sent (i.e. suppose abcsd) in the authorization header
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            'Description':'Signature Verification failed. Please enter correct structure of authorization header token.',
            'Error':'invalid_token'
        }
    ),401

# The below function() is called when no JWT-Token is sent in the authorization header
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {
            'Description': 'Request does not contain an access token.',
            'Error': 'authorization_required'
        }
    ), 401


# The below function() is called when we get a non-fresh token but we require a fresh token
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify(
        {
            'Description': 'The token is not fresh.',
            'Error': 'fresh_token_required'
        }
    ), 401


# The below function() is called when we want to make a valid token as invalid e.g. when a user logs out
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify(
        {
            'Description': 'The token has been revoked.',
            'Error': 'token_revoked'
        }
    ), 401



api.add_resource(ItemList,"/items")
api.add_resource(Item,"/item/<string:name>")
api.add_resource(UserRegister,"/register")
api.add_resource(UserLogin,"/login")
api.add_resource(TokenRefresh,"/refresh")
api.add_resource(UserLogout,"/logout")



if __name__=='__main__':

    #db.init_app(app)
    app.run(port=5000,debug=True)