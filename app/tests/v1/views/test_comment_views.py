import json

from ..base_test import BaseTest

class TestCommentViews(BaseTest):
    """ This class tests all the comments endpoint methods """

    def test_fetch_post_comment(self):
        """ Test fetch post's comments endpoint """

        self.post_req()
        user = self.post_req('api/v1/auth/login', self.user_login).json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}
        self.post_request('api/v1/1/posts', self.post, headers)

        # successful posting
        self.post_request('api/v1/1/posts', self.post, headers)
        req = self.get_request('api/v1/1/comments', headers)
        self.assertEqual(req.status_code, 200)

        # non-existing post
        self.post_request('api/v1/1/posts', self.post, headers)
        req2 = self.get_request('api/v1/0/comments', headers)
        self.assertEqual(req2.status_code, 404)
        self.assertEqual(req2.json['error'], 'Post not found or does not exist')

    def test_post_comment(self):
        """ Test post a comment endpoint """

        self.post_req()
        user = self.post_req('api/v1/auth/login', self.user_login).json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}
        self.post_request('api/v1/1/posts', self.post, headers)
        comment = {}

        # successful post
        req = self.post_request('api/v1/1/1/comments', self.comment, headers)
        self.assertEqual(req.status_code, 201)

        # logged out user
        self.client.post(
            'api/v1/auth/1/logout',
            headers=headers,
            content_type='application/json'
        )
        req = self.post_request('api/v1/1/1/comments', self.comment, headers)
        self.assertEqual(req.json['error'], 'Please log in first')

        # missing data
        req = self.post_request('api/v1/1/1/comments', comment, headers)
        self.assertEqual(req.status_code, 400)
        self.assertEqual(req.json['error'], 'You missed the comment key')

        comment['comment'] = ""
        req2 = self.post_request('api/v1/1/1/comments', comment, headers)
        self.assertEqual(req2.status_code, 422)

        # non-existing post
        req3 = self.post_request('api/v1/1/0/comments', self.comment, headers)
        self.assertEqual(req3.status_code, 404)
        self.assertEqual(req3.json['error'], 'post not found or does not exist')

        # non-existing user
        req4 = self.post_request('api/v1/0/1/comments', self.comment, headers)
        self.assertEqual(req4.status_code, 404)
        self.assertEqual(req4.json['error'], 'User not found or does not exist')


    def test_update_comment(self):
        """ Test the update a comment endpoint """

        self.post_req()
        user = self.post_req('api/v1/auth/login', self.user_login).json
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}
        self.post_request('api/v1/1/posts', self.post, headers)
        self.post_request('api/v1/1/1/comments', self.comment, headers)
        comment = {}

        # successful comment
        req = self.put_request('api/v1/1/1/comments/1', self.comment, headers)
        self.assertEqual(req.status_code, 200)

        # missing data
        req = self.put_request('api/v1/1/1/comments/1', comment, headers)
        self.assertEqual(req.status_code, 400)
        self.assertEqual(req.json['error'], 'You missed the comment key, value pair')

        comment['comment'] = ""
        req2 = self.put_request('api/v1/1/1/comments/1', comment, headers)
        self.assertEqual(req2.status_code, 422)

        # test non-existing user
        req4 = self.put_request('api/v1/0/1/comments/1', self.comment, headers)
        self.assertEqual(req4.status_code, 404)
        self.assertEqual(req4.json['error'], 'User not found or does not exist')

        # test non-existing post
        req5 = self.put_request('api/v1/1/0/comments/1', self.comment, headers)
        self.assertEqual(req5.status_code, 404)
        self.assertEqual(req5.json['error'], 'post not found or does not exist')

        # test non-existing comment
        req6 = self.put_request('api/v1/1/1/comments/0', self.comment, headers)
        self.assertEqual(req6.status_code, 404)
        self.assertEqual(req6.json['error'], 'Comment not found or does not exist!')

        # unauthorized user
        data = {
            "first_name" : "John",
            "last_name" : "Doe",
            "email" : "john@demo.com",
            "username" : "john",
            "password": "abc123@1A",
            "image": "",
            "confirm_password": "abc123@1A"
        }
        log = {
            "email": data['email'],
            "password": data['password']
        }
        self.post_req(data=data)
        user2 = self.post_req('api/v1/auth/login', log).json
        headers2 = {"Authorization": "Bearer {}".format(user2['auth_token'])}
        req7 = self.put_request('api/v1/2/1/comments/1', self.comment, headers2)
        self.assertEqual(req7.status_code, 401)
        self.assertEqual(req7.json['error'], 'You are not authorized to perform this action!')

        # logged out user
        self.client.post(
            'api/v1/auth/2/logout',
            headers=headers,
            content_type='application/json'
        )
        req8 = self.post_request('api/v1/2/1/comments', self.comment, headers)
        self.assertEqual(req8.json['error'], 'Please log in first')

    def test_delete_comment(self):
        """ Test the delete comment endpoint """

        self.post_req() # register user
        user = self.post_req('api/v1/auth/login', self.user_login).json # log in user
        headers = {"Authorization": "Bearer {}".format(user['auth_token'])}
        self.post_request('api/v1/1/posts', self.post, headers) # post
        self.post_request('api/v1/1/1/comments', self.comment, headers) # comment

        # successful delete comment
        req = self.delete_request('api/v1/1/1/comments/1', headers)
        self.assertEqual(req.status_code, 200)

        # non-existing comment
        req = self.delete_request('api/v1/1/1/comments/0', headers)
        self.assertEqual(req.status_code, 404)
        self.assertEqual(req.json['error'], 'Comment not found or does not exist')

        # test non-existing user
        req4 = self.put_request('api/v1/0/1/comments/1', self.comment, headers)
        self.assertEqual(req4.status_code, 404)
        self.assertEqual(req4.json['error'], 'User not found or does not exist')

        # test non-existing post
        req5 = self.put_request('api/v1/1/0/comments/1', self.comment, headers)
        self.assertEqual(req5.status_code, 404)
        self.assertEqual(req5.json['error'], 'post not found or does not exist')

        # # unauthorized user
        # data = {
        #     "first_name" : "John",
        #     "last_name" : "Doe",
        #     "email" : "john@demo.com",
        #     "username" : "john",
        #     "password": "abc123@1A",
        #     "image": "",
        #     "confirm_password": "abc123@1A"
        # }
        # log = {
        #     "email": data['email'],
        #     "password": data['password']
        # }
        # post = {
        #     "title": "post",
        #     "body": "sample test test"
        # }
        # self.post_req(data=data)
        # user2 = self.post_req('api/v1/auth/login', log).json
        # headers2 = {"Authorization": "Bearer {}".format(user2['auth_token'])}
        # self.post_request('api/v1/2/posts', post, headers2)
        # self.post_request('api/v1/2/1/comments', self.comment, headers2)
        # req7 = self.delete_request('api/v1/1/1/comments/2', headers)
        # self.assertEqual(req7.status_code, 401)
        # self.assertEqual(req7.json['error'], 'You are not authorized to perform this action!')

        # logged out user
        self.client.post(
            'api/v1/auth/1/logout',
            headers=headers,
            content_type='application/json'
        )
        self.post_request('api/v1/1/1/comments', self.comment, headers) # comment
        req8 = self.delete_request('api/v1/1/1/comments/2', headers)
        self.assertEqual(req8.status_code, 401)
        self.assertEqual(req8.json['error'], 'Please log in first')
