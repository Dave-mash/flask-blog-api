"""
This module sets up all the comments endpoints
Author: Dave
"""


from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint, session

from app.api.v1.models.posts import Post
from app.api.v1.utils.comments_validator import CommentsValidator
from app.api.v1.models.comments import Comment, AuthenticationRequired
from app.api.v1.models.users import User

v1 = Blueprint('commentv1', __name__, url_prefix='/api/v1/')


""" This route fetches a post's comments """
@v1.route("<int:postId>/comments", methods=['GET'])
def get_comments(postId):
    
    try:
        comments = Comment().fetch_comments('(comment, post_id, user_id, id)', f'post_id = {postId}')
        comments_list = []
        for comment in comments:
            obj = {
                "comment": comment[0]['f1'],
                "post_id": comment[0]['f2'],
                "user_id": comment[0]['f3'],
                "username": User().fetch_specific_user('username', f"id = {comment[0]['f3']}")[0],
                "id": comment[0]['f4']
            }
            comments_list.append(obj)

        return make_response(jsonify({
            "status": 200,
            "comments": comments_list
        }), 200)
    except:
        return make_response(jsonify({
            "error": "Post not found or does not exist",
            "status": 404
        }), 404)


""" This route posts a comment on a post """
@v1.route("/<int:userId>/<int:postId>/comments", methods=['POST'])
@AuthenticationRequired
def comment_on_post(postId, userId):
    data = request.get_json()

    try:
        data['comment']
    except:
        return make_response(jsonify({
            "error": 'You missed the comment key',
            "status": 400
        }), 400)

    comment = CommentsValidator(data['comment'])
        
    if comment.valid_comment():
        return make_response(jsonify({
            "error": comment.valid_comment(),
            "status": 422
        }), 422)

    
    post = Post().fetch_specific_post('id', f"id = {postId}")
    user = User().fetch_specific_user('id', f"id = {userId}")
    
    if not post:
        return make_response(jsonify({
            "error": "post not found or does not exist",
            "status": 404
        }), 404)
    
    if user:
    
        comment = {
            "authorId": userId,
            "comment": data['comment'],
            "postId": postId,
        }

        comment_model = Comment(comment)

        print('This ran')
        comment_model.save_comment()
        email = User().fetch_specific_user('email', f"id = {userId}")

        try:
            session.get(email[0])
            return make_response(jsonify({
                "status": 201,
                "message": "You have successfully commented on this post",
                "data": [{
                    "post": postId,
                    "comment": comment['comment']
                }]
            }), 201)
        except:
            return make_response(jsonify({
                "error": 'Please log in first',
                "status": 403
            }), 403)

    elif not user:
        return make_response(jsonify({
            "error": "User not found or does not exist",
            "status": 404
        }), 404)


""" This route updates a comment """
@v1.route("/<int:userId>/comments/<int:commentId>", methods=['PUT'])
@AuthenticationRequired
def edit_comment(userId, commentId):
    data = request.get_json()

    try:
        data['comment']
    except:
        return jsonify({
            "error": 'You missed the {} key, value pair'.format(data['comment'])
        })

    try:
        Comment().fetch_specific_comment('user_id', f"id = {commentId}")[0]  
        if Comment().fetch_specific_comment('user_id', f"id = {commentId}")[0] == userId:
            
            comment = Comment().update_comment(commentId, data)
            
            if isinstance(comment, dict):
                return make_response(comment, 404)
            else:
                email = User().fetch_specific_user('email', f"id = {userId}")

                # if session.get(email[0]):
                return make_response(jsonify({
                    "message": "You have successfully updated this comment",
                    "comment": data['comment'],
                    "status": 200
                }), 200)
                # else:
                #     return make_response(jsonify({
                #         "error": 'Please log in first',
                #         "status": 403
                #     }), 403)
        else:
            return make_response(jsonify({
                "error": "You are not authorized to perform this action!",
                "status": 401
            }), 401)
    except:
        return make_response(jsonify({
            "error": "Comment not found or does not exist!",
            "status": 404
        }), 404)    

""" This route deletes a comment """
@v1.route("/<int:userId>/comments/<int:commentId>", methods=['DELETE'])
@AuthenticationRequired
def delete_comment(userId, commentId):

    try:
        Comment().fetch_specific_comment('user_id', f"id = {commentId}")[0] 
        if Comment().fetch_specific_comment('user_id', f"id = {commentId}")[0] == userId:
            
            comment = Comment().delete_comment(commentId)

            if isinstance(comment, dict):
                return make_response(jsonify(comment), 404)
            else:
                # email = User().fetch_specific_user('email', f"id = {userId}")

                # if session.get(email[0]):
                return make_response(jsonify({
                    "message": 'comment was deleted successfully',
                    "status": 200
                }), 200)
                # else:
                #     return make_response(jsonify({
                #         "error": 'Please log in first',
                #         "status": 403
                # }), 403)
        else:
            return make_response(jsonify({
                "error": "You are not authorized to perform this action!",
                "status": 401
            }), 401)
    except:
        return make_response(jsonify({
            "error": "Comment not found or does not exist",
            "status": 404
        }), 404)

