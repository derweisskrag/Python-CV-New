from flask import Flask, request
from pymongo import MongoClient

from database.user import User 


app = Flask(__name__)

client = MongoClient('mongodb+srv://adming:Mka-pnYLJ9KYgDH@cv-app.cn4g9ri.mongodb.net/?retryWrites=true&w=majority')
db = client['CV-APP']

@app.route('/api/users/create-user', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:  
        user = User(username=username, password=password)
        user.save()
        return 'User created successfully!'
    else:
        return 'Username and password are required.', 400 

if __name__ == '__main__':
    app.run()
