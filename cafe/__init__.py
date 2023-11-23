from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/cafe"
mongo = PyMongo(app)

# Connected to collection, just need to call query function eg. menu.find()
menu = mongo.db.menu
orders = mongo.db.orders
users = mongo.db.users

from cafe import routes


