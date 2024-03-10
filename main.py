from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
import warnings

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecret'
client = MongoClient('mongodb+srv://master:!!master@cluster1.x8c5jdd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
db = client['weatherApp']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = 'You Must Login to Access This Page!'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return db.users.find_one({'_id': user_id})

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
