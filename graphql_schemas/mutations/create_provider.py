# GraphQL
from graphene import Mutation, Field, String
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_schemas.objects import ProviderObject

# Authentication
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from models.user import User
from models.provider import Provider


class CreateProvider(Mutation):
    """ GraphQL Mutation for creating a Provider. """

    class Arguments:
        description = String(required=True)

    provider = Field(lambda: ProviderObject)

    @jwt_required
    def mutate(self, info, **args):
        current_user = User.find_by_email(get_jwt_identity())

        provider = Provider(description=args.get("description"), user=current_user)
        provider.save()

        return CreateProvider(provider=provider)
