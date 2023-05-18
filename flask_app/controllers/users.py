from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register/user', methods = ["POST"])
def add_entry():
    if not user.User.validate_user(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":pw_hash
        }
    user_id = user.User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods = ["POST"])
def login():
    data = { "email": request.form["email"]}
    user_in_db = user.User.get_one_by_email(data)

    if not user_in_db:
        flash(" Invalid Email/Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash(" Invalid Email/password","login")
        return redirect('/')
    # ---> The lines below puts our logged in user(object of our class user) in session
    session['user_id'] = user_in_db.id
    session['name'] = user_in_db.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def user_dashboard():
    # This is to prevent non logged in users from acess to our app
    if "user_id" not in session:
        flash(" You must be logged in","login")
        return redirect('/')
    logged_in_user = user.User.get_one_by_id({"id": int(session['user_id'])})
    all_cars = car.Car.get_all_cars_with_owner()
    return render_template("dashboard.html", one_user = logged_in_user, all_cars = all_cars)


@app.route('/logout')
def logout():
    session.clear()
    # session.pop('email', None) ---> Another way to clear user data from session
    return redirect('/')
