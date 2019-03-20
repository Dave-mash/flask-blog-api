import unittest
import datetime
import json
import os

from app import create_app
from app.api.v1.models.base_model import BaseModel
from app.database import InitializeDb
from instance.config import app_config
from ..base_test import BaseTest

class TestUser(BaseTest):
    """ This class tests all the user endpoint methods """

    def test_fetch_all_user(self):
        """ Test that fetch all users works correctly """

        payload = self.get_req('api/v1/users')
        self.assertEqual(payload.status_code, 200)
    

    def test_sign_up_user(self):
        """ Test that sign up users route works correctly """

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

        user3 = {**self.user_item}
        user3['first_name'] = "w"
        payload3 = self.post_req(data=user3)
        self.assertEqual(payload3.status_code, 422)
        self.assertEqual(payload3.json['error'], 'Your first name should be between 4 to 24 characters long!')
        

    def test_log_in_user(self):
        """ Test that the log in user route works correctly """

        # test non existing account
        user = {
            "email": "fake@test.com",
            "password": "abc123"
        }
        payload = self.post_req('api/v1/auth/login', user)
        self.assertEqual(payload.json['error'], 'Details not found. Try signing up!')

        # test successful log in
        user2 = {
            "email": self.user_item['email'],
            "password": self.user_item['password']
        }
        self.post_req()
        payload4 = self.post_req(path='api/v1/auth/login', data=user2)
        self.assertEqual(payload4.status_code, 201)
        self.assertEqual(payload4.json['status'], 201)

        # test invalid log in credentials
        user1 = {
            "email": self.user_item['email'],
            "password": "abc123"
        }
        payload3 = self.post_req(path='api/v1/auth/login', data=user1)
        print('-->', payload3)
        self.assertEqual(payload3.status_code, 403)
        self.assertEqual(payload3.json['error'], 'Your email or password is incorrect!')


    def test_update_account(self):
        """ Test that the update account route works correctly """

        # test successful update
        user = self.post_req().json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}

        update_user = {
            "first_name" : "Travis",
            "last_name" : "Scott",
            "email" : "trav@demo.com",
            "username" : "trav",
            "image": "",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }
        
        req = self.put_request('api/v1/profile/1', update_user, headers)
        self.assertEqual(req.json['message'], 'user trav@demo.com updated successfully')

        # test invalid data
        update_user2 = {**update_user}
        update_user2['first_name'] = ''

        req2 = self.put_request('api/v1/profile/1', update_user2, headers)
        self.assertEqual(req2.json['error'], 'please enter valid first name!')

        # test missing data
        update_user3 = {
            "last_name" : "Scott",
            "email" : "trav@demo.com",
            "username" : "trav",
            "image": "",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }

        req3 = self.put_request('api/v1/profile/1', update_user3, headers)
        self.assertEqual(req3.json['error'], 'You missed the first_name key, value pair')

        # test none existing user
        req4 = self.put_request('api/v1/profile/5', update_user, headers)
        self.assertEqual(req4.json['error'], 'User not found or does not exist!')


    def test_get_user_details(self):
        """ Test that a user can access all their details """

        # test successful fetch
        user = self.post_req().json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}

        req = self.get_request('api/v1/profile/1', headers)       
        self.assertEqual(req.status_code, 200)

        # test non existing user
        req2 = self.get_request('api/v1/profile/5', headers)
        self.assertEqual(req2.status_code, 404)


    def test_delete_user_account(self):
        """ Test that a user can delete their account """

        # test successful delete
        user = self.post_req().json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}

        req = self.delete_request('api/v1/profile/1', headers)
        self.assertEqual(req.status_code, 200)

        # test non existing user
        req2 = self.delete_request('api/v1/profile/5', headers)
        self.assertEqual(req2.status_code, 404)


    def test_log_out_user(self):
        """ Test that a user can log out """

        # test successful log out
        user2 = {
            "email": self.user_item['email'],
            "password": self.user_item['password']
        }
        self.post_req()
        payload4 = self.post_req(path='api/v1/auth/login', data=user2).json        
        headers = {"Authorization": "Bearer {}".format(payload4['auth_token'])}

        req = self.client.post(
            'api/v1/auth/1/logout',
            headers=headers,
            content_type='application/json'
        )
        self.assertEqual(req.status_code, 200)

        # test non existing user
        req = self.client.post(
            'api/v1/auth/5/logout',
            headers=headers,
            content_type='application/json'
        )
        self.assertEqual(req.status_code, 404)