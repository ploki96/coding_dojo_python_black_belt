from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.painting import Painting
from flask import flash
import re
        


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]{8,255}$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9._-]{2,255}$')
NAME_REGEX = re.compile(r"^[A-Z]{1}[\w. '-]{1,254}$") 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.purchases = []
    
    @classmethod
    def single_user(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        user = connectToMySQL('black_belt_schema').query_db(query, data)
        return user[0]
        

    @classmethod
    def single_user_w_purchases(cls, data):
        query = "SELECT * FROM users LEFT JOIN paintings ON users.id = paintings.user_id LEFT JOIN users_paintings ON users.id = users_paintings.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('black_belt_schema').query_db(query, data)
        user = cls(results[0])
        for row in results:
            painting = {
                'id': row['paintings.id'],
                'title': row['title'],
                'description': row['description'],
                'price': row['price'],
                'quantity_made': row['quantity_made'],
                'quantity_sold': row['quantity_sold'],
                'created_at': row['paintings.created_at'],
                'updated_at': row['paintings.updated_at'],
                'user_id': row['user_id']
            }
            user.purchases.append(Painting(painting))
        return user

    @classmethod
    def show_purchases(cls, data):
        query = "SELECT * FROM users_paintings LEFT JOIN users ON users.id = users_paintings.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('black_belt_schema').query_db(query, data)
        return results


    @classmethod
    def purchase(cls, data):
        query = "SELECT * FROM users_paintings WHERE user.id = %(users)s AND painting.id = %(paintings)s;"
        result = connectToMySQL('black_belt_schema').query_db(query, data)
        if not result:
            query = "INSERT INTO users_paintings (users_paintings.user_id, users_paintings.painting_id) VALUES (%(users)s, %(paintings)s);"
            return connectToMySQL('black_belt_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('black_belt_schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('black_belt_schema').query_db(query, data)

    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('black_belt_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_user(input):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results_email = connectToMySQL('black_belt_schema').query_db(query, input)
        if len(results_email) >= 1:
            flash('Email address already used.')
            is_valid = False

        if not NAME_REGEX.match(input['first_name']): 
            flash("Invalid first name!")
            is_valid = False

        if not NAME_REGEX.match(input['last_name']): 
            flash("Invalid last name!")
            is_valid = False

        if not EMAIL_REGEX.match(input['email']): 
            flash("Invalid email!")
            is_valid = False
        
        if not PASSWORD_REGEX.match(input['password']): 
            flash("Invalid password")
            is_valid = False
        return is_valid
        
