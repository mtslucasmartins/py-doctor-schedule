# Imports
from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from flask_restful import Api

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)

from config import HOST, PORT
from database import db
from graphql_schemas import schema
from libs.strings import gettext

from resources import auth as auth_resource
from resources import signup as signup_resource

# app initialization
app = Flask(__name__)
app.config.from_object("default_settings")

# Configs
# TO-DO
api = Api(app)

jwt = JWTManager(app)

CORS(app)

# Modules
db.init_app(app)


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify(
            {"description": gettext("security_token_expired"), "error": "token_expired"}
        ),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(err):
    return (
        jsonify(
            {
                "description": gettext("secutity_invalid_signature"),
                "error": "invalid_token",
            }
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(err):
    return (
        jsonify(
            {
                "description": gettext("security_request_without_token"),
                "error": "token_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return (
        jsonify(
            {
                "description": gettext("security_token_not_fresh"),
                "error": "fresh_token_required",
            }
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": gettext("security_token_revoked"), "error": "token_revoked"}
        ),
        401,
    )


# Routes
@app.before_first_request
def create_tables():
    print("")
    print(">>> app.before_first_request")
    print("    Creating Tables...")
    db.create_all()


# GraphQL View.
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

# RESTful Endpoints.
api.add_resource(auth_resource.AuthAccessToken, "/auth/token")
api.add_resource(auth_resource.AuthRefreshToken, "/auth/refresh")

# 
api.add_resource(signup_resource.SignUp, "/register")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
