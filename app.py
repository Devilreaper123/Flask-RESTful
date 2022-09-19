# Importing required libraries and other files for the Flask Application
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)


# Using JWT to create a new endpoint for Authentication
jwt = JWT(app, authenticate, identity)  # Creates a new endpoint named /auth
items = []

# Item class has different HTTP Verbs as methods.
# @jwt_required() decorator is used to indicate Authentication is Required for the Method


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help="This field cannot be left blank!!!!!"
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"Item": item}, 200 if item else 404

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


# api.add_resource is used to create the endpoint for
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister , '/register')

# app.run basically starts the development server on your localhost on the specified port.
# debug=True helps in debug the code in case of errors
app.run(port=4000, debug=True)
