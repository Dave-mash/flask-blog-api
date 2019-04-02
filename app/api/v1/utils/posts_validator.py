"""
This module validates incoming posts
"""

class PostValidator:

    def __init__(self, data={}):
        if data:
            self.title = data['title']
            self.body = data['body']

    def post_fields(self, data):
        
        fields = ['title', 'body']
        for key in fields:
            try:
                data[key]
            except:
                return {
                    "error": 'You missed the {} key, value pair'.format(key),
                    "status": 400
                }

    def data_exists(self):
        if not self.title:
            return "Title is a required field!"
        elif not self.body:
            return "body is a required field!"

    def valid_post(self):
        if isinstance(self.title, int) or isinstance(self.body, int):
            return "Invalid string"