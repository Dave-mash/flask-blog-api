"""
This module sets up the posts model and all it's functionality
"""

import os, json
from flask import jsonify

from app.api.v1.models.base_model import BaseModel, AuthenticationRequired

class Post(BaseModel):
    
    def __init__(self, post={}, database=os.getenv('FLASK_DATABASE_URI')):
    
        self.base_model = BaseModel()
        self.base_model.table_name = 'posts'
    
        if post:
            self.title = post['title']
            self.body = post['body']
            self.author_id = post['author_id']


    def save_post(self):

        post_item = dict(
            title=self.title,
            body=self.body,
            author_id=self.author_id
        )

        keys = ", ".join(post_item.keys())
        values = tuple(post_item.values())
        if self.fetch_specific_post('title', f"title = '{self.title}'"):
            return {
                "error": "Please make your title unique",
                "status": 409
            }
        else:
            self.base_model.add_item(keys, values)
    

    def fetch_posts(self, fields, condition, name=''):
        """ This method fetches all posts """

        return self.base_model.grab_all_items(f'{fields}', condition, name)


    def fetch_specific_post(self, column, condition):
        """ This method fetches a single post """

        return self.base_model.grab_items_by_name(column, condition)


    def fetch_post_id(self, title):
        """ This method fetches a post id """
    
        try:
            return self.fetch_specific_post('id', f"title = '{title}'")
        except:
            return False


    # Array --> [(['1', '1', '2'],)]

    def update_post(self, id, updates):
        """ This method updates a post """

        pairs_dict = {
            "title": f"title = '{updates['title']}'",
            "body": f"body = '{updates['body']}'",
        }
        
        pairs = ", ".join(pairs_dict.values())
        
        if self.fetch_specific_post('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return jsonify({
                "error": "post not found or does not exist!",
                "status": 404
            })


    def delete_post(self, id):
        """ This method deletes a post """

        if self.fetch_specific_post('id', f"id = {id}"):
            return self.base_model.delete_item(f"id = {id}")
        else:
            return {
                "error": "Post not found or does not exist!",
                "status": 404
            }
