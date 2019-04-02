"""
This module tests the post_validator methods
"""

import unittest
from app.api.v1.utils.posts_validator import PostValidator

class TestQuestionsValidator(unittest.TestCase):

    def setUp(self):
        """ Initializes app """
        self.post = {
            "title": "Python",
            "body": "Python is an amazing language"
        }

    def test_post_fields_exists(self):
        post =  {
            "body": "Python is an amazing language"
        }
        validate = PostValidator()

        # test missing sign up fields
        self.assertEqual(validate.post_fields(post), {
            "error": 'You missed the title key, value pair',
            "status": 400
        })  


    def test_invalid_data(self):
    
        # test short title
        post = {}
        post.update(self.post)
        post['title'] = 'D'
        validator = PostValidator(post)
        self.assertEqual(validator.valid_post(), "Your title is too short!")

        # test short body
        post2 = {}
        post2.update(self.post)
        post2['body'] = 'm'
        valid2 = PostValidator(post2)
        self.assertEqual(valid2.valid_post(), "Your post is too short. Try being a bit more descriptive")


    def test_data_exists(self):
        """ Test that check_fields method works correctly """
        post = {
            "title": "",
            "body": "Python is an amazing language"
        }

        validator = PostValidator(post)
        self.assertEqual(validator.data_exists(), "Title is a required field!")