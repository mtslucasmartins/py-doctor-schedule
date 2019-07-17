from flask_jwt_extended import jwt_required, get_jwt_identity

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_schemas.objects import (
    UserObject,
    OrganizationObject,
    LocationObject,
    ProviderObject,
    ExamTypeObject,
)

from database import db

from models.user import User
from models.locations import Location
from models.provider import Provider
from models.exam_type import ExamType
from models.organization import Organization


class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()

    user = graphene.Field(UserObject, uuid=graphene.Int())
    users = graphene.Field(
        lambda: graphene.List(UserObject),
        id=graphene.Int(),
        page_index=graphene.Int(),
        page_size=graphene.Int(),
    )

    organization = graphene.Field(OrganizationObject, uuid=graphene.Int())
    organizations = graphene.Field(
        lambda: graphene.List(OrganizationObject),
        id=graphene.Int(),
        page_index=graphene.Int(),
        page_size=graphene.Int(),
    )

    location = graphene.Field(LocationObject, id=graphene.Int())
    locations = graphene.Field(
        lambda: graphene.List(LocationObject),
        id=graphene.Int(),
        l_description=graphene.String(),
        page_index=graphene.Int(),
        page_size=graphene.Int(),
    )

    provider = graphene.Field(ProviderObject, id=graphene.Int())
    providers = graphene.Field(
        lambda: graphene.List(ProviderObject),
        id=graphene.Int(),
        l_description=graphene.String(),
        page_index=graphene.Int(),
        page_size=graphene.Int(),
    )

    exam_type = graphene.Field(ExamTypeObject, id=graphene.Int())
    exam_types = graphene.Field(
        lambda: graphene.List(ExamTypeObject),
        id=graphene.Int(),
        l_description=graphene.String(),
        page_index=graphene.Int(),
        page_size=graphene.Int(),
    )

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------
    @jwt_required
    def resolve_user(self, info, **args):
        return User.resolve_user(**args)

    @jwt_required
    def resolve_users(self, info, **args):
        return User.resolve_users(**args)

    # -----------------------------------------------------
    # ORGANIZATIONS
    # -----------------------------------------------------
    @jwt_required
    def resolve_organization(self, info, **args):
        return Organization.resolve_organization(**args)

    @jwt_required
    def resolve_organizations(self, info, **args):
        return Organization.resolve_organizations(**args)

    # -----------------------------------------------------
    # LOCATIONS
    # -----------------------------------------------------
    @jwt_required
    def resolve_location(self, info, **args):
        return Location.resolve_location(**args)

    @jwt_required
    def resolve_locations(self, info, **args):
        return Location.resolve_locations(**args)

    # -----------------------------------------------------
    # PROVIDERS
    # -----------------------------------------------------
    @jwt_required
    def resolve_provider(self, info, **args):
        return Provider.resolve_provider(**args)

    @jwt_required
    def resolve_providers(self, info, **args):
        return Provider.resolve_providers(**args)

    # -----------------------------------------------------
    # EXAM TYPES
    # -----------------------------------------------------
    @jwt_required
    def resolve_exam_type(self, info, **args):
        return ExamType.resolve_exam_type(**args)

    @jwt_required
    def resolve_exam_types(self, info, **args):
        return ExamType.resolve_exam_types(**args)
