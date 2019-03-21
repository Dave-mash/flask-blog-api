"""
This module sets up all the post endpoints
Author: Dave
"""

from flask import request, jsonify, make_response, Blueprint, session

from app.api.v1.utils.posts_validator import PostValidator
from app.api.v1.models.posts import Post, AuthenticationRequired
from app.api.v1.models.users import User, AuthenticationRequired

v1 = Blueprint('postv1', __name__, url_prefix='/api/v1/')


""" This route fetches all posts """
@v1.route("/posts", methods=['GET'])
def get():
    posts = Post().fetch_posts('(title, body, created_on, id, author_id)', 'True = True')
    posts_list = []

    for post in posts:
        username = User().fetch_specific_user('username', f"id = {post[0]['f5']}")[0]
        post_item = {
            "title": post[0]['f1'],
            "body": post[0]['f2'],
            "createdOn": post[0]['f3'],
            "id": post[0]['f4'],
            "author": username
        }
        posts_list.append(post_item)

    return make_response(jsonify({
        "status": 200,
        "posts": posts_list
    }), 200)


""" This route posts a post """
@v1.route("/<int:userId>/posts", methods=['POST'])
@AuthenticationRequired
def post(userId):
    data = request.get_json()
    auth_token = request.headers.get('Authorization')
    token = auth_token.split(" ")[1]
    
    if PostValidator().post_fields(data):
        return make_response(jsonify(PostValidator().post_fields(data)), 400)
    else:
        validate_post = PostValidator(data)
        validation_methods = [
            validate_post.valid_post,
            validate_post.data_exists
        ]

        for error in validation_methods:
            if error():
                return make_response(jsonify({
                    "error": error()
                }), 422)
        
        if User().fetch_specific_user('email', f"id = {userId}"):
            print('-->', User().fetch_specific_user('email', f"id = {userId}"))

            post = {
                "author_id": userId,
                "title": data['title'],
                "body": data['body']
            }
            
            if not User().blacklisted(token):
                post_model = Post(post)
                if isinstance(post_model.save_post(), dict):
                    return make_response(jsonify(post_model.save_post()))
                else:
                    post_model.save_post()
                    return make_response(jsonify({
                        "status": 201,
                        "message": "You have successfully posted a post",
                        "data": {
                            "title": data['title'],
                            "body": data['body'],
                            "user": userId,
                            "post_id": post_model.fetch_post_id(data['title'])[0],
                        }
                    }), 201)
            else:
                return make_response(jsonify({
                    "error": "Please log in first!",
                    "status": 403
                }), 403)
        else:
            return make_response(jsonify({
                "error": "user not found or does not exist!",
                "status": 404
            }), 404)

""" This route updates a post """
@v1.route("/<int:userId>/posts/<int:postId>", methods=['PUT'])
@AuthenticationRequired
def edit_post(postId, userId):
    data = request.get_json()
    auth_token = request.headers.get('Authorization')
    token = auth_token.split(" ")[1]
    
    if PostValidator().post_fields(data):
        return make_response(jsonify(PostValidator().post_fields(data)), 400)
    else:
        validate_post = PostValidator(data)
        validation_methods = [
            validate_post.valid_post,
            validate_post.data_exists
        ]

        for error in validation_methods:
            if error():
                return make_response(jsonify({
                    "error": error()
                }), 422)

    if Post().fetch_specific_post('author_id', f"id = {postId}")[0] == userId:

        post = Post().update_post(postId, data)

        if isinstance(post, dict):
            return make_response(post)
        else:
            if not User().blacklisted(token):
                return make_response(jsonify({
                    "message": "You have successfully updated this post",
                    "status": 200
                }), 200)
            else:
                return make_response(jsonify({
                    "error": 'Please log in first!',
                    "status": 403
                }), 403)
    else:
        return make_response(jsonify({
            "error": "You are not authorized to perform this action!",
            "status": 401
        }), 401)


""" This route deletes a post """
@v1.route("<int:userId>/posts/<int:postId>", methods=['DELETE'])
@AuthenticationRequired
def delete_post(postId, userId):
    auth_token = request.headers.get('Authorization')
    token = auth_token.split(" ")[1]
    
    
    if not User().blacklisted(token):  

        if Post().fetch_specific_post('author_id', f"id = {postId}") == (userId,):
            post = Post().delete_post(postId)
            if isinstance(post, dict):
                return make_response(post)
            else:
                return make_response(jsonify({
                    "error": 'post was deleted successfully',
                    "status": 200
                }), 200)
        else:
            return make_response(jsonify({
                "error": "You are not authorized to perform this action!",
                "status": 401
            }), 401)
    else:
        return make_response(jsonify({
            "error": 'Please log in first',
            "status": 403
        }), 403)