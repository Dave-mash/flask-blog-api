"""
This module tests the comment_validator methods
"""

import unittest
from app.api.v1.utils.comments_validator import CommentsValidator

class TestQuestionsValidator(unittest.TestCase):

    def setUp(self):
        """ Initializes app """
        self.comment = {
            "comment": "This is a comment",
        }

    def test_invalid_data(self):

        validator = CommentsValidator("")
        self.assertEqual(validator.valid_comment(), "The comment field is required!")
