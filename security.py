from resources.user import UserModel
from werkzeug.security import  safe_str_cmp
from models.user import UserModel

users=[
    UserModel(100,'bob','password')
]

#index on user
username_mapping={
    u.username: u for u in users
}

'''
'bob':{
    'id':1,
    'username':'bob',
    'password':'password'
}
'''


#index on userid
userid_mapping={
    u.id:u for u in users }
'''
1:{
    'id':1,
    'username':'bob',
    'password':'password'
}
'''

def authenticate(username,password): ## This is used at the beginning that is when authenticating initially
    #user=username_mapping.get(username,None) # if there is no key for this username, it would return None
    user=UserModel.find_by_username(username)

    if user and safe_str_cmp(user.password,password):
        #safe_str_cmp(a,b) takes care of different encoding schemes used by a and b and compares them
        return user

def identity(payload): # This is used after authentication whenever the client makes a request and passes the JWT token as an identity
    user_id=payload['identity']
    #return userid_mapping.get(user_id,None)
    return UserModel.find_by_id(user_id)

