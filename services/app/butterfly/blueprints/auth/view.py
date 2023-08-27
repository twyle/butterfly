"""This module contains the view functions for authorization.

Declares the following methods:

register:
    Register a new user.
send_confirm_account_email:
    Send the user registration email.
confirm_account:
    Confirm the user account.
login:
    Login a registered user.
logout:
    Logout a logged in user
reset_request:
    Handle the request to reset the password.
reset_password:
    Reset the user password
send_reset_email:
    Send the password reset email
"""

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from http import HTTPStatus
from ..database.schemas.user import (
    UserCreate, GetUser, GetUsers, User as UserSchema, UserCreated as UserCreatedSchema,
    ActivateUser, LoginUser, LoggedInUser, RequestPasswordReset, RequestPasswordResetToken,
    PasswordReset
)
from ..database.crud.user import (
    create_user, get_user_by_email, get_user, get_users, delete_user, user_account_active,
    activate_user_account, loggin_user, generate_password_reset_token, password_repeated,
    reset_password
)
from ..database.models.user import User
from ..database.database import get_db
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError, IntegrityError


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == 'GET':
        return {'success': 'registration form'}, HTTPStatus.OK
    elif request.method == 'POST':
        try:
            user_data = UserCreate(**request.form) 
        except ValidationError:
            return {'Error': 'The data provided is invalid or incomplete!'}, HTTPStatus.BAD_REQUEST
        try:
            if get_user_by_email(email=user_data.email_address, session=get_db):
                return {'Error': f'User with email address {user_data.email_address} already exists.'}, HTTPStatus.CONFLICT
            user = create_user(user_data=user_data, session=get_db) 
        except (OperationalError, IntegrityError) as e:
            print(e)
            # Send email to
            return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
        resp = UserCreatedSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            id=user.id,
            activation_token='AccActi_' + User.encode_auth_token(user.id)
        )
        return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@auth.route("/send_confirm_account_email", methods=["GET"])
def send_confirm_account_email():
    """Send account confirmation email."""
    return {'success': 'email sent'}, HTTPStatus.OK


@auth.route("/confirm_account", methods=["GET"])
def confirm_account():
    """Confirm a newly created account."""
    return {'success': 'account confirmed'}, HTTPStatus.OK


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Login a registered user."""
    return {'success': 'user logged in'}, HTTPStatus.OK


@auth.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    """Handle the request to reset the password."""
    return {'success': 'reset request received'}, HTTPStatus.OK


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    """Reset the user password."""
    return {'success': 'password reset'}, HTTPStatus.OK


@auth.route("/logout", methods=["GET"])
def logout():
    """Logout a logged in user."""
    return {'success': 'user logged out'}, HTTPStatus.OK


@auth.route("/update", methods=["POST"])
def update():
    """Update a logged in user."""
    return {'success': 'user updated'}, HTTPStatus.OK


@auth.route("/delete", methods=["DELETE", "GET"])
def delete():
    """Delete a logged in user."""
    if request.method == 'GET':
        return {'success': 'delete form'}, HTTPStatus.OK
    elif request.method == 'DELETE':
        try:
            user_data = GetUser(user_id=request.args.get('user_id'))
        except ValidationError:
            return {'error': 'Invalid input: you probably did not include the user id.'}, HTTPStatus.BAD_REQUEST
        try:
            user = get_user(session=get_db, user_data=user_data)
            if not user:
                return {'Error': f'User with id {user_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND
            user = delete_user(get_db, GetUser(user_id=request.args.get('user_id')))
        except OperationalError as e:
                print(e)
                # Send email to
                return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
        resp = UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            id=user.id
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
@auth.route("/get", methods=["DELETE", "GET"])
def get():
    """Get a logged in user."""
    pass


@auth.route("/all_users", methods=["GET"])
def list_all():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    try:
        users = get_users(get_db, GetUsers(offset=offset, limit=limit))
    except ValidationError:
        return {'Error': 'The data provided is invalid or incomplete!'}, HTTPStatus.BAD_REQUEST
    except (IntegrityError, OperationalError) as e:
        print(e)
        # Send email to
        return {'Error': 'The application is experiencing a tempoary error. Please try again in a few minutes.'}, HTTPStatus.INTERNAL_SERVER_ERROR
    users = [
        UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            id=user.id
            ).model_dump()
        for user in users
    ]
    return users, HTTPStatus.OK