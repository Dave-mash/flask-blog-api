"""
This module sets up the question model and all it's functionality
"""

import os
import uuid
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v1.models.base_model import BaseModel, AuthenticationRequired

class User(BaseModel):
    
    def __init__(self, user={}):

        self.base_model = BaseModel()
        self.base_model.table_name = 'users'

        if user:
            self.Fname = user['first_name']
            self.Lname = user['last_name']
            self.email = user['email']
            self.username = user['username']
            self.password = generate_password_hash(user['password'])
            self.isAdmin = False
      
      
    def save_user(self):
        """ This method saves a non-existing user """

        user = dict(
            first_name=self.Fname,
            last_name=self.Lname,
            email=self.email,
            username=self.username,
            password=self.password,
            image='user.png'
        )

        keys = ", ".join(user.keys())
        values = tuple(user.values())


        if self.fetch_specific_user('email', f"email = '{self.email}'"):
            return {
                "error": "This email already exists try logging in!",
                "status": 409
            }
        elif self.fetch_specific_user('username', f"username = '{self.username}'"):
            return {
                "error": "This username is already taken!",
                "status": 409
            }
        else:
            return self.base_model.add_item(keys, values)


    def fetch_user_id(self, username):
        """ This method fetches a user id """
    
        try:
            return self.fetch_specific_user('id', f"username = '{username}'")
        except:
            return False


    def fetch_all_users(self):
        """ This method fetches all users """

        return self.base_model.grab_all_items('(username, email)', f"True = True")


    def fetch_specific_user(self, cols, condition):
        """ This method fetches a single user """

        return self.base_model.grab_items_by_name(cols, condition)
        

    # Log in user
    def log_in_user(self, details):
        """ This method logs in a user """

        user = self.fetch_specific_user('email', f"email = '{details['email']}'")
        password = self.fetch_specific_user('password', f"email = '{details['email']}'")
        
        if not user:
            return {
                "error": "Details not found. Try signing up!",
                "status": 401
            }
        elif not check_password_hash(password[0], details['password']):
            return {
                "error": "Your email or password is incorrect!",
                "status": 403
            }
        else:
            return self.base_model.grab_items('(id, username)', f"email = '{details['email']}'")[0]


    # Log out user
    def log_out_user(self, id):
        """ This method logs in a user """

        user = self.fetch_specific_user('username', f"id = '{id}'")
        
        if user:
            return user[0]
        else:
            return False


    def delete_user(self, id):
        """ This method defines the delete query """

        if self.fetch_specific_user('id', f"id = {id}"):
            return self.base_model.delete_item(f"id = {id}")
        else:
            return {
                "error": "User not found or does not exist!"
            }


    def update_user(self, id, updates):
        """ This method defines the update query """

        image = updates['image'] if updates['image'] else '{user.png}'

        pairs_dict = {
            "first_name": f"first_name = '{updates['first_name']}'",
            "last_name": f"last_name = '{updates['last_name']}'",
            "email": f"email = '{updates['email']}'",
            "username": f"username = '{updates['username']}'",
            "password": f"password = '{generate_password_hash(updates['password'])}'",
            "image": f"image = '{image}'"
        }
        
        pairs = ", ".join(pairs_dict.values())

        if self.fetch_specific_user('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return {
                "error": "User not found or does not exist!"
            }
