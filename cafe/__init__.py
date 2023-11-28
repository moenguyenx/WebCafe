from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/cafe"
app.config['SECRET_KEY'] = 'e5ff79a61007b916057540a1'
mongo = PyMongo(app)

# Connected to collection, just need to call query function eg. menu.find()
menu = mongo.db.menu
orders = mongo.db.orders
users = mongo.db.users
finance = mongo.db.finance

from cafe import routes


