from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList

# If we import q module, all the code inside it gets executed while importing, that is why , in each module, we should mention to execute the code only when the code is run by that module by:
# if __name__=='__main__:' and only the module that is used to run i.e the module on which we right clock and run is assigned the '__main__' name

app=Flask(__name__)
app.secret_key='cisco'
api=Api(app)

#item=[]

#JWT below create a new endpoint "/auth"
#When we call "/auth", we send it a username and a password and the JWT extension gets the username and password and send it over to
# "authenticate handler: (authenticate below) and identity handler: (identity below)
jwt=JWT(app,authenticate,identity)


api.add_resource(ItemList,"/items")
api.add_resource(Item,"/item/<string:name>")
api.add_resource(UserRegister,"/register")

if __name__=='__main__':

    db.init_app(app)
    app.run(port=5000,debug=True)