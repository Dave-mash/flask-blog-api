"""
This module takes care of validating input from the endpoint
"""

from datetime import datetime
import re
import string

class UserValidator:
  
    def __init__(self, data={}):
        self.data = data

    # Helper methods

    def errorHandler(self, error_name):
        errors = {
            "first_name": "Your first name should be between 4 to 24 characters long!",
            "last_name": "Your last name should be between 4 to 24 characters long!",
            "username": "Your username should be between 4 to 24 characters long!",
            "email": "Invalid email address!",
            "password": "Weak password!",
            "phoneNumber": "Use valid numbers for phone number",
            "unmatching_pass": "Your passwords don't match!",
            "valid_Fname": "please enter valid first name!",
            "valid_Lname": "please enter valid last name!",
            "valid_username": "please enter valid username!"
        }
        return errors[error_name]

    def check_fields(self, data, fields):
        for key in fields:
            try:
                data[key]
            except:
                return {
                    "error": 'You missed the {} key, value pair'.format(key),
                    "status": 400
                }

    # Validator methods

    def signup_fields(self, data):

        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']

        return self.check_fields(data, fields)

    def login_fields(self, data):

        fields = ['email', 'password']

        return self.check_fields(data, fields)

    def valid_name(self):
        field_names = {
            'first_name': str(self.data['first_name']),
            'last_name': str(self.data['last_name']),
            'username': str(self.data['username'])
        }

        if not field_names['first_name'].isalpha():
            return self.errorHandler("valid_Fname")
        elif not field_names['last_name'].isalpha():
            return self.errorHandler('valid_Lname')
        elif isinstance(field_names['username'], int):
            return self.errorHandler('valid_username')

        for key, value in field_names.items():
            if len(value) < 3 or len(value) > 25:
                return self.errorHandler(key)

    def valid_email(self):
        reg_email = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

        if not re.match(reg_email, str(self.data['email'])):
            return self.errorHandler('email')

    def validate_password(self):
        reg_password = re.compile(r"^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])")

        if not re.match(reg_password, str(self.data['password'])):
            return self.errorHandler('password')

    def matching_password(self):
        if str(self.data['password']) != str(self.data['confirm_password']):
            return self.errorHandler('unmatching_pass')


# password ref.
# Minimum 8 characters.
# The alphabets must be between [a-z]
# At least one alphabet should be of Upper Case [A-Z]
# At least 1 number or digit between [0-9].
# At least 1 character symbol ie[@, #].
# eg abc123@1A