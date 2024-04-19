from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt


MONGO_URI = "your-mongo-URI"

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI
app.config['SECRET_KEY'] = 'your-app-secret-key'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Connected to collection, just need to call query function eg. menu.find()
menu = mongo.db.menu
orders = mongo.db.orders
users = mongo.db.users
finance = mongo.db.finance
drinks = mongo.db.drinks

from cafe import routes


