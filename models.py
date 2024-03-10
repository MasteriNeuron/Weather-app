from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient('mongodb+srv://master:!!master@cluster1.x8c5jdd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
db = client['weatherApp']

class City:
    def __init__(self, name):
        self.name = name

class User:
    def __init__(self, _id, first_name, last_name, email, password):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.authenticated = False

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

