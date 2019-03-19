"""
This module defines all the user endpoints
"""
import json
import re
from flask import request, jsonify, make_response, Blueprint, session

from app.api.v1.models.users import User, AuthenticationRequired
from app.api.v1.utils.users_validator import UserValidator
from app.api.v1.models.posts import Post
from app.api.v1.models.comments import Comment

v1 = Blueprint('userv1', __name__, url_prefix='/api/v1/')


""" This route fetches all users """
@v1.route("/users", methods=['GET'])
def get():

    users = User().fetch_all_users()
    users_list = []

    for user in users:
        users_list.append(user[0])

    return make_response(jsonify({
        "status": 200,
        "users": users_list
    }), 200)


""" This route allows unregistered users to sign up """
@v1.route("/auth/signup", methods=['POST'])
def registration():
    data = request.get_json()
    # print('user views called')

    # Validate user
    validate_user = UserValidator(data)

    if validate_user.signup_fields(data):
        return make_response(jsonify(validate_user.signup_fields(data)), 400)
    
    validation_methods = [
        validate_user.valid_email,
        validate_user.valid_name,
        validate_user.validate_password,
        validate_user.matching_password
    ]

    for error in validation_methods:
        if error():
            return make_response(jsonify({
                "error": error(),
                "status": 422
            }), 422)

    # Register user
    user_data = {
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email": data['email'],
        "username": data['username'],
        "password": data['password']
    }

    reg_user = User(user_data)

    if reg_user.save_user():
        return make_response(jsonify(reg_user.save_user()), 409)
    else:
        id = reg_user.fetch_user_id(user_data['username'])
        auth_token = reg_user.encode_auth_token(id[0])
        return make_response(jsonify({
            "status": 201,
            "message": "{} registered successfully".format(data['email']),
            "username": data['username'],
            "auth_token": auth_token.decode('utf-8')
        }), 201)        
            


######################################################################################################

# The log in and log out routes need a little refactoring

""" This route allows registered users to log in """
@v1.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json()
    missing_fields = UserValidator().login_fields(data)

    if missing_fields:
        return make_response(jsonify(missing_fields), 400)

    validate_user = UserValidator(data)
    reg_email = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

    if not re.match(reg_email, str(data['email'])):
        return make_response(jsonify({
            "error": validate_user.valid_email()
        }), 422)

    credentials = {
        "email": data['email'],
        "password": data['password']
    }

    log_user = User().log_in_user(credentials)
    username = User().fetch_specific_user('username', f"id = {log_user}")

    if isinstance(log_user, int):
        User().connection.close()
        auth_token = User().encode_auth_token(log_user)
        store = {
            "token": auth_token.decode('utf-8'),
            "email": credentials['email']
        }
        session.permanent = True
        session[f"{store['email']}"] = store
        print(session.get(store['email']))
        return make_response(jsonify({
            "status": 201,
            "message": "{} has been successfully logged in".format(data['email']),
            "auth_token": auth_token.decode('utf-8'),
            "id": log_user,
            "username": username[0]
        }), 201)
    else:
        return make_response(log_user)

            
""" This route allows registered users to log out """
@v1.route("/auth/<int:userId>/logout", methods=['GET'])
@AuthenticationRequired
def logout(userId):
    session.permanent = True
    print(session.permanent)
    # remove the user from the session
    print(session.get(User().fetch_specific_user('email', f"id = '{userId}'")[0]))

    try:
        email = User().fetch_specific_user('email', f"id = '{userId}'")
        if session.get(email[0]) != None:
            session.pop(email[0], None)
            return make_response(jsonify({
                "message": "You have been logged out",
                "status": 200
            }), 200)
        else:
            return make_response(jsonify({
                "error": "You are not logged in",
                "status": 400
            }), 400)
    except:
        return make_response(jsonify({
            "error": "user not found or does not exist",
            "status": 400
        }), 400)
######################################################################################################

""" This route allows a user to delete their account """
@v1.route("/profile/<int:userId>", methods=['DELETE'])
@AuthenticationRequired
def del_account(userId):

    remove_user = User().delete_user(userId)
    email = User().fetch_specific_user('email', f"id = {userId}")

    if isinstance(remove_user, dict) and session.get(email[0]):
        return make_response(jsonify(remove_user))
    else:
        return make_response(jsonify({
            "message": f"user with id '{userId}' deleted successfully",
            "status": 200
        }), 200)


""" This route allows a user to update their account """
@v1.route("/profile/<int:userId>", methods=['PUT', 'GET'])
@AuthenticationRequired
def update_account(userId):

    if request.method == 'PUT':
        data = request.get_json()
        if UserValidator().signup_fields(data):
            return make_response(jsonify(UserValidator().signup_fields(data)), 400)
        else:
            # Validate user
            validate_user = UserValidator(data)
            validation_methods = [
                validate_user.valid_email,
                validate_user.valid_name,
                validate_user.validate_password,
                validate_user.matching_password
            ]

            for error in validation_methods:
                if error():
                    return make_response(jsonify({
                        "error": error()
                    }), 422)
                    
        user_data = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "username": data['username'],
            "password": data['password'],
            "image": data['image']
        }    

        update_user = User().update_user(userId, user_data)
        email = User().fetch_specific_user('email', f"id = {userId}")

        if isinstance(update_user, dict) and session.get(email[0]):
            return make_response(jsonify(update_user))
        else:
            return make_response(jsonify({
                "message": f"user {user_data['email']} updated successfully",
                "status": 200
            }), 200)
    elif request.method == 'GET':
        user = User().grab_all_items('(username, image, first_name, last_name, email, password)', f"id = {userId}", 'users')
        if user:
            posts = Post().fetch_posts('(title, created_on, id)', f'author_id = {userId}')
            posts_list = []

            def loop(items,):
                for item in items:
                    item_result = {
                        "title": item[0]['f1'],
                        "createdAt": item[0]['f2'],
                        "id": item[0]['f3']
                    }
                    posts_list.append(item_result)

            loop(posts)

            user_dict = {
                "username": user[0][0]['f1'],
                "image": user[0][0]['f2'],
                "first_name": user[0][0]['f3'],
                "last_name": user[0][0]['f4'],
                "email": user[0][0]['f5'],
                "password": user[0][0]['f6']
            }
            return make_response(jsonify({
                "user": user_dict,
                "posts": posts_list
            }), 200)
        else:
            return make_response(jsonify({
                "message": "user not found",
                "status": 404
            }), 404)