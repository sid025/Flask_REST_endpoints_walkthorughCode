from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


# Api works with resources and every resource has to be a class
# You can't have two different GET endpoints on one resource class.

class Item(Resource):

    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'Error': 'The item is not found'}, 404

        # connection=sqlite3.connect('data.db')
        # cursor=connection.cursor()
        #
        # query="SELECT * FROM items WHERE name=?"
        # result=cursor.execute(query,(name,))
        # row=result.fetchone()
        # connection.close()
        #
        # if row:
        #     return {'item':{'name':row[0],'price':row[1]}},200


    '''
    @jwt_required()
    def get(self,name):
        print(item)
        item_find=next(filter(lambda x:x['name']==name,item),None)
        if(item_find):
            return (item_find),200
        OR
        for i in item: 
            if i['name']==name:
                return i,200
        
        return ({'Error':"Item not found"}),404
        '''

    def post(self,name):

        if ItemModel.find_by_name(name):
            return ({"Error": "Item already present"}), 400
        else:
            parser = reqparse.RequestParser()  # will validate the incoming request ( can also be used with form validation )
            parser.add_argument("price", type=float, required=True, help="This is a required field")

            request_body = parser.parse_args()

            # request_body=request.get_json(force=True) # force=True means you don't look specifically for the value "json" in content header, u process anything
            # but that can be dangerous, without force=True, if the content header is not json, it will not process the text and thro an error
            price = request_body['price']
            #new_item = {'name': name, 'price': price}
            new_item=ItemModel(name,price)

            try:
                new_item.insert()
            except:
                return {'message':'An error occurred while inserting the item'},500 # Internal server error.


            return new_item.json(),201

        '''
        # Since we want only unique items in the "item" list, we check if its there already before appending to the new list
        item_find=next(filter(lambda x:x['name']==name,item),None)
        if (item_find):
            return ({"Error":"Item already present"}),400
        else:
            parser = reqparse.RequestParser()  # will validate the incoming request ( can also be used with form validation )
            parser.add_argument("price", type=float, required=True, help="This is a required field")

            request_body = parser.parse_args()

            #request_body=request.get_json(force=True) # force=True means you don't look specifically for the value "json" in content header, u process anything
            # but that can be dangerous, without force=True, if the content header is not json, it will not process the text and thro an error
            price=request_body['price']
            new_item={'name':name,'price':price}
            item.append(new_item)
            return  (new_item),201
        '''


    def delete(self,name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="DELETE FROM items WHERE name=?"

        cursor.execute(query,(name,))
        connection.commit()
        connection.close()

        return {"message":"Item has been deleted."}

    def put(self,name):
        
        parser=reqparse.RequestParser() # will validate the incoming request ( can also be used with form validation )
        parser.add_argument("price",type=float,required=True,help="This is a required field")

        data=parser.parse_args()
        #data=request.get_json()

        '''
        for s in item:
            if s['name']==name:
                s['price']=data['price']
                return {"name":name,"price":data['price']},200
        new_item = {'name': name, 'price': data['price']}
        '''

        item_find=ItemModel.find_by_name(name)
        #updated_item={'name':name,'price':data['price']}
        updated_item=ItemModel(name,data['price'])

        if item_find is None:
            try:
                updated_item.insert()
            except:
                return {'Error': 'An error occurred'}, 500


        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "UPDATE items SET price=? WHERE name=?"

            try:
                cursor.execute(query, (data['price'],name))
                connection.commit()
                connection.close()
            except:
                return {'Error':'An error occurred'},500

        return updated_item.json(),202




class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        row = result.fetchall()
        item=[]

        for i in row:
            item.append(i)

        connection.close()

        return {'itemlist':item}

