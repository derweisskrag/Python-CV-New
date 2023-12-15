from flask import Flask, render_template, request, session, redirect, url_for
from mongoengine import connect
from models.user import User
from flask import jsonify

import json

from resume.create import create_cv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my$key'

# Connect to your MongoDB database
connect('CV-APP', host='mongodb+srv://<name>:<password>@cv-app.cn4g9ri.mongodb.net/?retryWrites=true&w=majority')

@app.route('/api/users/create-user', methods=['POST'])
def create_user():
	print(request.form)
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')
	repeat_password = request.form.get('repeat-password')

	if password != repeat_password:
		return jsonify({"error": 'Passwords do not match!'}), 400
    
    # Create a new User instance
	new_user = User(name=username, email=email, password=password)
    
	try:
		new_user.save()  # Save the new user to the database
		return 'User created successfully!'
	except Exception as e:
		return f'Error creating user: {str(e)}', 500  # Return an error message if something goes wrong

@app.get("/")
def home():
	user_name = session.get('name') if 'logged_in' in session else 'Guest'
	return render_template('home.html', user_name=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.objects(email=email).first()
        if user and user.password == password:
        	session['logged_in'] = True
        	session['email'] = email
        	session['name'] = user.name
        	return redirect(url_for('dashboard'))
        else:
            'Incorrect email/password'

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.clear()
	return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
	if 'logged_in' in session:
		user_name = session.get('name')
		return render_template('dashboard.html', user_name=user_name)
	else:
		return redirect('login')

@app.route('/build-cv', methods=['GET', 'POST'])
def build_cv():
	user_name = session.get('name') if 'logged_in' in session else "Guest"
	if request.method == "POST":
		form_data = request.form.to_dict()
		with open('shared/cv_data.py', 'w') as file:
			file.write(f"form data = {json.dumps(form_data, indent=4)}")
		return render_template('exported.html', user_name=user_name)
	elif request.method == "GET":
		form_data = request.args.to_dict()
		with open('shared/cv_data.py', 'w') as file:
			file.write(f"form data = {json.dumps(form_data, indent=4)}")

		create_cv(form_data, 'my_cv.pdf')



		return render_template('exported.html', user_name=user_name)
	else:
		return render_template('error.html', user_name=user_name)

def main():
	app.run()

if __name__ == "__main__":
	main()
