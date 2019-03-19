import unittest
import datetime
import json
import os

from app import create_app
from app.api.v1.models.base_model import BaseModel
from app.database import InitializeDb

class TestUser(unittest.TestCase):

    def setUp(self):
        """ Initializes app"""

        self.app = create_app('testing')
        self.base_model = BaseModel()
        self.client = self.app.test_client()
        self.user_item = {
            "first_name" : "David",
            "last_name" : "Mwangi",
            "email" : "dave@demo.com",
            "username" : "dave",
            "image": "",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }


    def post_req(self, path='api/v1/auth/signup', data={}):
        """ This function utilizes the test client to send POST requests """
        
        data = data if data else self.user_item
        res = self.client.post(
            path,
            data=json.dumps(data),
            content_type='application/json'
        )
        return res


    def get_req(self, path):
        """ This function utilizes the test client to send GET requests """
        
        res = self.client.get(path)
        return res


    def test_fetch_all_user(self):
        """ This method tests that fetch all users works correctly """

        payload = self.get_req('api/v1/users')
        self.assertEqual(payload.status_code, 200)
    

    def test_sign_up_user(self):
        """ This method tests that sign up users route works correctly """

        # test successful registration
        
        payload = self.post_req()
        self.assertEqual(payload.json['status'], 201)
        self.assertTrue(payload.json['auth_token'])
        self.assertEqual(payload.json['message'], "dave@demo.com registered successfully")

        # test missing fields

        user = {
            "last_name" : "Mwangi",
            "email" : "jjj@demo.com",
            "username" : "jjj",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }
        payload2 = self.post_req(data=user)
        self.assertEqual(payload2.status_code, 400)
        self.assertEqual(payload2.json['error'], 'You missed the first_name key, value pair')

        # test invalid data

        user2 = {**self.user_item}
        user2['first_name'] = "1234214"
        payload3 = self.post_req(data=user2)
        self.assertEqual(payload3.status_code, 422)
        self.assertEqual(payload3.json['error'], 'please enter valid first name!')


    # def test_log_in_user(self):
    #     """ This method tests that the log in user route works correctly """

        # test successful log in
        # user = {
        #     "email": self.user_item['email'],
        #     "password": self.user_item['password']
        # }
        
        # payload4 = self.post_req(path='api/v1/auth/login', data=user)
        # InitializeDb('TEST_DATABASE_URI').create_tables()
        # self.post_req()
        # self.assertEqual(payload4.status_code, 201)
        # # self.assertTrue(payload4.json['auth_token'])

        # user_payload = self.post_req()
        # self.assertEqual(user_payload.json['message'], "dave@demo.com registered successfully")

        # # test log in credentials
        # user1 = {
        #     "email": self.user_item['email'],
        #     "password": "abc123"
        # }
        # payload = self.post_req(path='api/v1/auth/login', data=user1)
        # self.assertEqual(payload.status_code, 403)
        # self.assertEqual(payload.json['error'], 'Your email or password is incorrect!')

        # test non-existing user
        # user4 = {
        #     "email": "abc@demo.com",
        #     "password": "abc4A#@"
        # }
        # payload2 = self.post_req(path='api/v1/auth/login', data=user4)
        # self.assertEqual(payload2.status_code, 401)
        # self.assertEqual(payload2.json['error'], "Details not found. Try signing up!")

        # # test invalid email
        # user2 = {
        #     "email": "jjjdemo.com",
        #     "password": self.user_item['password']
        # }
        # payload3 = self.post_req(path='api/v1/auth/login', data=user2)
        # self.assertEqual(payload3.status_code, 422)
        # self.assertEqual(payload3.json['error'], "Invalid email address!")


    def tearDown(self):
        """ This method destroys the test tables """

        BaseModel().drop_tables()