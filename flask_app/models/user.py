from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import car

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{4,}$')


class User:
    DB = "sharif_examDB"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.buys = []

    @classmethod
    def save(cls,data):
        query = """ INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
        
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM users;"""
        results = connectToMySQL(cls.DB).query_db(query)
        
        all_users = []

        for user in results:
            all_users.append(cls(user))
        return all_users
    
    @classmethod
    def get_one_by_email(cls,data):
        query = """ SELECT * FROM users WHERE email = %(email)s """
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_by_id(cls,data):
        query = """
            SELECT * FROM users WHERE id = %(id)s
        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        print(result)
        return cls(result[0])
    
    @classmethod
    def get_user_with_cars(cls,data):
        query = """
            SELECT * FROM users
            LEFT JOIN buys on buys.user_id = users.id
            LEFT JOIN cars ON buys.car_id = cars.id
            WHERE users.id = %(id)s;
        """

        results = connectToMySQL(cls.DB).query_db(query,data)
        user = cls(results[0])

        for user_row in results:
            car_data = {
                "id":user_row["cars.id"],
                "price":user_row["price"],
                "model":user_row["model"],
                "make":user_row["make"],
                "year":user_row["year"],
                "description":user_row["description"]
            }
            user.buys.append(car.Car(car_data))

        return user


    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DB).query_db(query,user)
        if len(results) >=1:
            flash("Email already taken","register")
            is_valid = False

        if len(user['first_name']) < 3:
            flash("Name must be atleat 3 characters.","register")
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Name must be atleast 3 characters.","register")
            is_valid = False

        if len(user['password']) < 8:
            flash("password must atleast be 8 characters long!!!","register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords Don't match","register")
            is_valid = False

        # if not PASSWORD_REGEX.match(user['password']):
        #     flash("password must contain atleast 1 uppercase letter, 1 special character and 1 number and atleats 4 characters long","register")
        #     is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!!!","register")
            is_valid = False
        return is_valid



