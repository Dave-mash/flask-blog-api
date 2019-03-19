"""
This module validates incoming comments
"""

class CommentsValidator:

    def __init__(self, comment):
        self.comment = comment

    def valid_comment(self):
        if not self.comment:
            return "The comment field is required!"