from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DATABASE
from flask import flash, session

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Login:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM registration;"
        results = connectToMySQL(DATABASE).query_db(query)

        users = []

        for row in results:
            users.append( cls(row) )
        return users

    @classmethod
    def insert(cls, data):
        query = "INSERT INTO registration (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,now(),now());"

        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM registration WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)

        return cls(result[0])
        

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM registration WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_input_reg(input):
        is_valid = True # we assume this is true
        if len(input['first_name']) < 1:
            flash("field is required", 'err_first_name')
            is_valid = False

        if len(input['last_name']) < 1:
            flash("field is required", 'err_last_name' )
            is_valid = False

        if len(input['email']) <1:
            flash("field is required", 'err_email')
            is_valid = False

        elif not EMAIL_REGEX.match(input['email']):
            flash("Invalid Email Address!", 'err_email')
            is_valid = False
        
        else:
            potential_user = Login.get_by_email({'email' : input['email']})
            if potential_user:
                flash("Email already exists!", 'err_email')
                is_valid = False

        if len(input['password']) < 1:
            flash("field is required", 'err_password')
            is_valid = False

        if len(input['confirm_password']) < 1:
            flash("field is required", 'err_confirm_password')
            is_valid = False

        elif input['password'] != input['confirm_password']:
            flash("Passwords do not match!", 'err_confirm_password')
            flash("Passwords do not match!", 'err_password')
            is_valid = False
            
        return is_valid

    @staticmethod
    def validate_input_inp(input):
        is_valid = True # we assume this is true
        if len(input['email']) <1:
            flash("field is required", 'err_email_login')
            is_valid = False

        elif not EMAIL_REGEX.match(input['email']):
            flash("Invalid Email Address!", 'err_email_login')
            is_valid = False
        
        else:
            potential_user = Login.get_by_email({'email' : input['email']})
            if not potential_user:
                flash("Email doesn't exist!", 'err_email_login')
                is_valid = False
                
        if len(input['password']) < 1:
            flash("field is required", 'err_password_login')
            is_valid = False

        

        return is_valid


    

