import unittest
import json

from app import create_app
from instance.config import app_config
from app.database import InitializeDb

class BaseTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        """ This method sets up the test client """
        self.app = create_app('testing')
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

        self.post = {
            "title": "Javascript",
            "body": "Javascript is an amazing language"
        }

        self.comment = {
            "comment": "Hello Dave over here!"
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


    def post_request(self, path, data, headers):
        """ This function utilizes the test client to send POST requests """
        
        req = self.client.post(
            path=path,
            data=json.dumps(data),
            headers=headers,
            content_type='application/json'
        )
        return req


    def get_request(self, path, headers):
        """ This method utilizes the test client to send GET requests """

        req = self.client.get(
            path=path,
            headers=headers,
            content_type='application/json'
        )
        return req


    def put_request(self, path, data, headers):
        """ This method utilizes the test client to send PUT requests """

        req = self.client.put(
            path=path,
            data=json.dumps(data),
            headers=headers,
            content_type='application/json'
        )
        return req


    def delete_request(self, path, headers):
        """ This method utilizes the test client to send DELETE requests """

        req = self.client.delete(
            path=path,
            headers=headers,
            content_type='application/json'
        )
        return req


    def tearDown(self):
        """ This method destroys all objects created by the test client """

        InitializeDb(app_config['testing']).drop_tables()
        InitializeDb(app_config['testing']).connection.close()
