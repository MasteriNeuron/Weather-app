import string
from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functions import get_weather_data
from main import app, db, login_manager
from flask import redirect, url_for, flash, render_template
from models import User, City, db

@login_manager.user_loader
def load_user(user_id):
    return db.users.find_one({'_id': user_id})

@app.route('/')
@login_required
def index_get():
    print("hello i am don")
    cities = db.cities.find()

    weather_data = []

    for city in cities:
        r = get_weather_data(city['name'])
        weather = {
            'city': city['name'],
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'country': r['sys']['country'],
        }
        weather_data.append(weather)

    return render_template('index.html', weather_data=weather_data)

@app.route('/', methods=['POST'])
@login_required
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    new_city = new_city.lower().capitalize()  # Ensuring proper capitalization
    if new_city:
        existing_city = db.cities.find_one({'name': new_city})
        
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = {'name': new_city}

                db.cities.insert_one(new_city_obj)
            else:
                err_msg = 'That is not a valid city!'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully!', 'success')

    return redirect(url_for('index_get'))

@app.route('/delete/<name>')
@login_required
def delete_city(name):
    db.cities.delete_one({'name': name})
    flash(f"Deleted {name} Successfully!", 'success')
    return redirect(url_for('index_get'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', first_name=current_user.first_name)



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = db.users.find_one({'email': email})

        # check if the user actually exists
        # and compare the hashed password from the database
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['_id'], user['first_name'], user['last_name'], user['email'], user['password'])
            user_obj.authenticated = True
            login_user(user_obj, remember=remember)

            flash('Logged in successfully.')
            return redirect(url_for('index_get'))
        else:
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))  # if the user doesn't exist or password is wrong, reload the page
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user['authenticated'] = False
    db.users.update_one({'_id': user['_id']}, {'$set': {'authenticated': False}})
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup',  methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.users.find_one({'email': email})

        if user:
            flash('User exists!', 'error')
            return redirect(url_for("signup"))

        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': generate_password_hash(password, method="sha256"),
            'authenticated': False
        }

        db.users.insert_one(new_user)

        return redirect(url_for("login"))

    return render_template('signup.html')
