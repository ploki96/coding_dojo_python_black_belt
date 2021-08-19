from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash



class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity_made = data['quantity_made']
        self.quantity_sold = data['quantity_sold']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def add_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, quantity_made, quantity_sold, user_id) VALUES (%(title)s, %(description)s, %(price)s, %(quantity_made)s, 0, %(user_id)s);"
        return connectToMySQL('black_belt_schema').query_db(query, data)


    @classmethod
    def edit_painting(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity_made = %(quantity_made)s WHERE id = %(id)s;"
        return connectToMySQL('black_belt_schema').query_db(query, data)

    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s"
        return connectToMySQL('black_belt_schema').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results = connectToMySQL('black_belt_schema').query_db(query)
        paintings = []
        for painting in results:
            paintings.append( cls(painting) )
        return paintings
    
    @classmethod
    def get_painting(cls, data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        result = connectToMySQL('black_belt_schema').query_db(query, data)
        return result
    
    @classmethod
    def purchase(cls, data):
        query = "UPDATE paintings SET quantity_sold = quantity_sold+1 WHERE id = %(id)s"
        return connectToMySQL('black_belt_schema').query_db(query, data)

    @staticmethod
    def validate_painting(input):
        is_valid = True
        if len(input['title']) > 255 or len(input['title']) < 2:
            flash('Title must be less than 255 characters')
            is_valid = False
        if len(input['description']) > 255 or len(input['description']) < 10:
            flash('Description must be between 10 and 255 characters')
            is_valid = False
        if len(input['price']) < 1:
            flash('Price must be a positive number')
            is_valid = False
        elif int(input['price']) <= 0:
            flash('Price must be a positive number')
            is_valid = False
        if len(input['quantity_made']) < 1:
            flash('Quantity must be a positive number')
            is_valid = False
        elif int(input['quantity_made']) <= 0:
            flash('Quantity must be a positive number')
            is_valid = False
        return is_valid


