from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from libs.strings import gettext
from models.user import User


def parse_auth_token_args():
    parser = reqparse.RequestParser()
    parser.add_argument("username", help="This field cannot be blank", required=True)
    parser.add_argument("password", help="This field cannot be blank", required=True)
    return parser.parse_args()


class AuthCheckToken(Resource):

    @jwt_required
    def get(self):
        current_user = User.find_by_email(get_jwt_identity())

        if not current_user:
            return (
                {
                    "description": gettext("security_invalid_credentials"),
                    "error": "invalid_credentials",
                },
                401,
            )

        return (
            current_user.json(),
            200,
        )


class AuthAccessToken(Resource):
    def post(self):
        current_user = get_jwt_identity()
        request_args = parse_auth_token_args()

        username = request_args.get("username")
        password = request_args.get("password")

        current_user = User.find_by_email(username)

        if not current_user:
            return (
                {
                    "description": gettext("security_invalid_credentials"),
                    "error": "invalid_credentials",
                },
                401,
            )

        if User.check_password(password, current_user.password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                "token_type": "Bearer",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        return (
            {
                "description": gettext("security_invalid_credentials"),
                "error": "invalid_credentials",
            },
            401,
        )


class AuthRefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}

