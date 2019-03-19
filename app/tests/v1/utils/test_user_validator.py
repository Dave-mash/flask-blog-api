"""
This module tests the user_validator methods
"""

import unittest
from app.api.v1.utils.users_validator import UserValidator

class TestQuestionsValidator(unittest.TestCase):

    def setUp(self):
        """ Initializes app """
        self.user = {
            "first_name": "Dave",
            "last_name": "Mwangi",
            "username": "Mash",
            "email": "demo@email.com",
            "password": "password",
            "image": "",
            "confirm_password": "password"
        }

    def test_user_fields_exists(self):
        user =  {
            "last_name": "Mwangi",
            "username": "Mash",
            "email": "demo@email.com",
            "password": "password",
            "confirm_password": "password"
        }
        validate = UserValidator(user)

        # test missing sign up fields
        self.assertEqual(validate.signup_fields(user), {
            "error": 'You missed the first_name key, value pair',
            "status": 400
        })  

        user2 =  {
            "password": "password",
        }

        validate2 = UserValidator(user2)

        # test missing log in fields
        self.assertEqual(validate2.login_fields(user2), {
            "error": 'You missed the email key, value pair',
            "status": 400
        })

    def test_invalid_data(self):

        # test short first name
        user = {}
        user.update(self.user)
        user['first_name'] = 'D'
        validator = UserValidator(user)
        self.assertEqual(validator.valid_name(), "Your first name should be between 4 to 24 characters long!")

        # test short last name
        user2 = {}
        user2.update(self.user)
        user2['last_name'] = 'm'
        valid2 = UserValidator(user2)
        self.assertEqual(valid2.valid_name(), "Your last name should be between 4 to 24 characters long!")

        # test invalid email address
        user3 = {}
        user3.update(self.user)
        user3['email'] = 'abc.com'
        valid3 = UserValidator(user3)
        self.assertEqual(valid3.valid_email(), 'Invalid email address!')

        # test weak password
        user4 = {}
        user4.update(self.user)
        user4['password'] = 'wf'
        valid4 = UserValidator(user4)
        self.assertEqual(valid4.validate_password(), 'Weak password!')

        # test non-matching password
        user5 = {}
        user5.update(self.user)
        user5['confirm_password'] = 'abc'
        valid5 = UserValidator(user5)
        self.assertEqual(valid5.matching_password(), "Your passwords don't match!")

    def test_errorHandler(self):
        """ Test that errorHandler method works correctly """

        validator = UserValidator(self.user)
        self.assertEqual(validator.errorHandler('first_name'), "Your first name should be between 4 to 24 characters long!")
        self.assertEqual(validator.errorHandler('last_name'), "Your last name should be between 4 to 24 characters long!")
        self.assertEqual(validator.errorHandler('username'), "Your username should be between 4 to 24 characters long!")
        self.assertEqual(validator.errorHandler('email'), "Invalid email address!")
        self.assertEqual(validator.errorHandler('unmatching_pass'), "Your passwords don't match!")
        self.assertEqual(validator.errorHandler('password'), "Weak password!")

    def test_check_fields(self):
        """ Test that check_fields method works correctly """
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']
        user = {
            "last_name": "Mwangi",
            "username": "Mash",
            "email": "demo@email.com",
            "password": "password",
            "confirm_password": "password"
        }

        validator = UserValidator(user)
        self.assertEqual(validator.check_fields(user, fields), {
            "error": "You missed the first_name key, value pair",
            "status": 400
        })