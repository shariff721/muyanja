from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import car, user

@app.route("/new")
def add_new_car():
    if "user_id" not in session:
        flash(" You must be logged in","login")
        return redirect("/")
    return render_template("new_car.html")

@app.route("/process/cars", methods = ["POST"])
def process_car():
    if not car.Car.validate_cars(request.form):
        return redirect(request.referrer)
    else:
        data = {
            "price":request.form["price"],
            "model":request.form["model"],
            "make":request.form["make"],
            "year":request.form["year"],
            "description":request.form["description"],
            "user_id":session["user_id"]
        }
        car.Car.add_car(data)
        return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete_car(id):
    data = {
        "id":id
    }
    car.Car.delete_car(data)
    return redirect("/dashboard")

@app.route("/update/<int:id>")
def update_car(id):
    one_car = car.Car.get_one_with_owner({"id":id})
    return render_template("edit_car.html", one_car = one_car)

@app.route("/process/update", methods = ["POST"])
def update_user_car():
    if not car.Car.validate_cars(request.form):
        return redirect(request.referrer)
    car.Car.update_car(request.form)
    return redirect("/dashboard")

@app.route("/viewcar/<int:id>")
def view_one_car(id):
    data = {
        "id":id
    }
    one_car_posted = car.Car.get_one_with_owner(data)
    return render_template("view_car.html", one_car_posted = one_car_posted)

@app.route("/buy/car", methods = ["POST"])
def buy_new_car():
    data = {
        "car_id":request.form["car_id"],
        "user_id":request.form["user_id"]
    }
    car.Car.add_buy(data)
    return redirect("/dashboard")

@app.route("/user/buys/<int:id>")
def view_user_buys(id):
    data = {
        "id":id
    }
    user_buys = user.User.get_user_with_cars(data)
    return render_template("user_buys.html", user_buys = user_buys)


