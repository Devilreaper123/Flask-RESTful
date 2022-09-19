from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help="This field cannot be left blank!!!!!"
                        )

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query , (name,))
        row = result.fetchone()
        connection.close()

        if row : 
            return {'Items' : {'name' : row[0] , 'price' : row[1]}}
        return {"Message":"Item not Found"},404

    def post(self, name):
        # force=True(Converts the data into json, does not look for the content type) , silent=True (Does not give error just return none )
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {"Message": f"An item with the name '{name}' already exist"}, 400
        data = Item.parser.parse_args()
        item = {"name": name, "price": data['price']}
        items.append(item)
        return {'item': item}, 201
        # return {"Message": "Item not found"}, 404

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'Message': "Item Deleted"}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item


class ItemList(Resource):
    def get(self):
        return {"Item": items}
