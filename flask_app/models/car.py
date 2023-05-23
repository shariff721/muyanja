from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import re
from flask import flash


class Car:
    DB = "sharif_examDB"

    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]

        self.owner = None

    @classmethod
    def add_car(cls, data):
        query = """
            INSERT INTO cars (price, model, make, year, description, user_id)
            VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def get_all_cars_with_owner(cls):
        query = """
            SELECT * FROM cars JOIN users ON cars.user_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_cars = []

        for user_row in results:

            one_car = cls(user_row)

            user_data = {
                "id": user_row["users.id"],
                "first_name": user_row["first_name"],
                "last_name": user_row["last_name"],
                "email": user_row["email"],
                "password": user_row["password"],
                "created_at": user_row["created_at"],
                "updated_at": user_row["updated_at"]
            }

            one_car.owner = user.User(user_data)
            all_cars.append(one_car)

        return all_cars

    @classmethod
    def update_car(cls, data):
        query = """
            UPDATE cars
            SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one_with_owner(cls, data):
        query = """
            SELECT * FROM cars JOIN users ON cars.user_id = users.id
            WHERE cars.id = %(id)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)

        one_car = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        # we create an instance of the User class with the user data.
        one_user = user.User(user_data)
        one_car.owner = one_user

        return one_car

    @classmethod
    def delete_car(cls, data):
        query = """
            DELETE FROM cars WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def add_buy(cls, data):
        query = """
            INSERT INTO buys
            (user_id, car_id) VALUES (%(user_id)s, %(car_id)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_cars(car):
        is_valid = True

        if len(car['price']) < 1:
            flash("price must not be blank.")
            is_valid = False

        elif int(car['price']) <= 0:
            flash("invalid price.")
            is_valid = False

        if len(car['model']) < 1:
            flash("model must not be blank.")
            is_valid = False

        if len(car['make']) < 1:
            flash("make must not be blank.")
            is_valid = False

        if len(car['year']) < 1:
            flash("year must not be blank.")
            is_valid = False

        elif int(car['year']) <= 0:
            flash("Invalid year.")
            is_valid = False

        if len(car['description']) < 1:
            flash("Description must not be blank.")
            is_valid = False

        return is_valid

    def is_sold(self):
        query = """
            SELECT * FROM buys WHERE car_id = %(car_id)s;
        """
        data = {
            "car_id": self.id
        }
        results = connectToMySQL(Car.DB).query_db(query, data)
        if len(results) < 1:
            return False
        else:
            return True
