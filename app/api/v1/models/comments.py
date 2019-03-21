"""
This module sets up the comment model and all it's functionality
"""

import os
from flask import jsonify

from app.api.v1.models.base_model import BaseModel, AuthenticationRequired

class Comment(BaseModel):
    
    def __init__(self, comment={}, database=os.getenv('FLASK_DATABASE_URI')):
    
        self.base_model = BaseModel()
        self.base_model.table_name = 'comments'

        if comment:
            self.comment = comment['comment']
            self.user_id = comment['authorId']
            self.post_id = comment['postId']


    def save_comment(self):
        """ This method saves a comment """

        comment_item = dict(
            user_id=self.user_id,
            post_id=self.post_id,
            comment=self.comment
        )

        keys = ", ".join(comment_item.keys())
        values = tuple(comment_item.values())
        self.base_model.add_item(keys, values)


    def fetch_comments(self, fields, condition="True = True"):
        """ This method fetches all comments """

        return self.base_model.grab_all_items(f'{fields}', f'{condition}')


    def fetch_specific_comment(self, column, condition):
        """ This method fetches a single comment """

        return self.base_model.grab_items_by_name(column, condition)


    def update_comment(self, id, updates):
        """ This method updates a comment """

        pairs_dict = {
            "comment": f"comment = '{updates['comment']}'",
        }
        
        pairs = ", ".join(pairs_dict.values())
        
        if self.fetch_specific_comment('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return jsonify({
                "error": "Comment not found or does not exist!",
                "status": 404
            })


    def delete_comment(self, id):
        """ This method deletes a comment """

        return self.base_model.delete_item(f"id = {id}")

