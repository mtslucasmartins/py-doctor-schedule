# GraphQL
from graphene import Mutation, Field, String, Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_schemas.objects import ProviderObject
from graphql_schemas.objects import HealthPlanObject

# Authentication
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from models.user import User
from models.provider import Provider
from models.health_plan import HealthPlan


class CreateProvider(Mutation):
    """ GraphQL Mutation for creating a Provider. """

    class Arguments:
        description = String(required=True)

    provider = Field(lambda: ProviderObject)

    @jwt_required
    def mutate(self, info, **args):
        current_user = User.find_by_email(get_jwt_identity())

        provider = Provider(
            description=args.get("description"), organization=current_user.organization
        )
        provider.save()

        return CreateProvider(provider=provider)


class CreateHealthPlan(Mutation):
    """ GraphQL Mutation for creating a Provider. """

    class Arguments:
        description = String(required=True)
        provider_id = Int(required=True)

    health_plan = Field(lambda: HealthPlanObject)

    @jwt_required
    def mutate(self, info, **args):
        current_user = User.find_by_email(get_jwt_identity())

        provider = Provider.find_by_id(args.get("provider_id"))

        health_plan = HealthPlan(
            description=args.get("description"), provider=provider, organization=current_user.organization
        )
        health_plan.save()

        return CreateHealthPlan(health_plan=health_plan)
