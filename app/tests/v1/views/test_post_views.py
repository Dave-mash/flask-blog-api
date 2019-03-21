import json

from ..base_test import BaseTest

class TestPostViews(BaseTest):
    """ This class tests all the posts endpoint methods """

    def test_fetch_all_posts(self):
        """ This method tests the fetch posts method """

        req = self.get_req(path='api/v1/posts')

        self.assertEqual(req.status_code, 200)

    
    def test_post(self):
        """ This method tests the post method """

        # successful posting
        self.post_req()
        user = self.post_req('api/v1/auth/login', self.user_login).json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}

        req = self.post_request('api/v1/1/posts', self.post, headers)
        self.assertEqual(req.status_code, 201)

        # test invalid data
        post = {
            "body": "This is a post"
        }
        req2 = self.post_request('api/v1/1/posts', post, headers)
        self.assertEqual(req2.json['error'], 'You missed the title key, value pair')

        post3 = {
            "title": "javascript",
            "body": "This"
        }
        req4 = self.post_request('api/v1/1/posts', post3, headers)
        self.assertEqual(req4.json['error'], 'Your post is too short. Try being a bit more descriptive')
        
        # test non existing user
        req5 = self.post_request('api/v1/5/posts', self.post, headers)
        self.assertEqual(req5.status_code, 404)

        # test unique title
        self.assertEqual(self.post_req().status_code, 409)

        # test logged out user
        self.client.post(
            'api/v1/auth/1/logout',
            headers=headers,
            content_type='application/json'
        )
        req = self.post_request('api/v1/1/posts', self.post, headers)
        self.assertEqual(req.json['error'], 'Please log in first!')


    def test_update_post(self):
        """ This method tests the update post method """

        # successful update
        self.post_req()
        user = self.post_req('api/v1/auth/login', self.user_login).json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}

        post = {
            "title": "Artificial Intelligence",
            "body": "Awesome world of AI"
        }
        self.post_request('api/v1/1/posts', post, headers)
        req = self.put_request('api/v1/1/posts/1', post, headers)
        self.assertEqual(req.status_code, 200)

        # test invalid data
        post2 = {
            "body": "Awesome world of AI"
        }
        req2 = self.post_request('api/v1/1/posts', post2, headers)
        self.assertEqual(req2.json['error'], 'You missed the title key, value pair')

        post3 = {
            "title": "Artificial Intelligence",
            "body": "This"
        }
        req4 = self.post_request('api/v1/1/posts', post3, headers)
        self.assertEqual(req4.json['error'], 'Your post is too short. Try being a bit more descriptive')
        
        # test non existing user
        req5 = self.post_request('api/v1/5/posts', self.post, headers)
        self.assertEqual(req5.status_code, 404)

        # test unique title
        self.assertEqual(self.post_req().status_code, 409)

        # unauthorized user
        req6 = self.put_request('api/v1/5/posts/1', post, headers)
        self.assertEqual(req6.json['error'], 'You are not authorized to perform this action!')

        # test logged out user
        self.client.post(
            'api/v1/auth/1/logout',
            headers=headers,
            content_type='application/json'
        )
        self.post_request('api/v1/1/posts', post, headers)
        req = self.put_request('api/v1/1/posts/1', post, headers)
        self.assertEqual(req.json['error'], 'Please log in first!')


    def test_delete_post(self):
        """ This method tests the delete method """

        # successful delete
        self.post_req()
        user = self.post_req('api/v1/auth/login', self.user_login).json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}

        self.post_request('api/v1/1/posts', self.post, headers)
        req = self.delete_request('api/v1/1/posts/1', headers=headers)
        self.assertEqual(req.status_code, 200)

        # unauthorized user
        req6 = self.delete_request('api/v1/5/posts/1', headers)
        self.assertEqual(req6.json['error'], 'You are not authorized to perform this action!')

        # test logged out user
        self.client.post(
            'api/v1/auth/1/logout',
            headers=headers,
            content_type='application/json'
        )
        req = self.delete_request('api/v1/1/posts/1', headers=headers)
        self.assertEqual(req.json['error'], 'Please log in first')
