# Importing required libraries and other files for the Flask Application
from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import ItemList, Item

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)


# Using JWT to create a new endpoint for Authentication
jwt = JWT(app, authenticate, identity)  # Creates a new endpoint named /auth

# Item class has different HTTP Verbs as methods.
# @jwt_required() decorator is used to indicate Authentication is Required for the Method



# api.add_resource is used to create the endpoint for
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister , '/register')

# app.run basically starts the development server on your localhost on the specified port.
# debug=True helps in debug the code in case of errors
app.run(port=4000, debug=True)
