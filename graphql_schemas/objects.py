import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models.user import User
from models.organization import Organization


class LocationObject(graphene.ObjectType):
    id = graphene.ID()
    description = graphene.String()


class ProviderObject(graphene.ObjectType):
    id = graphene.ID()
    description = graphene.String()


class ExamTypeObject(graphene.ObjectType):
    id = graphene.ID()
    description = graphene.String()


class OrganizationObject(graphene.ObjectType):
    id = graphene.ID()
    cpf_cnpj = graphene.String()
    description = graphene.String()

    created_at = graphene.Date()
    updated_at = graphene.Date()


class UserObject(graphene.ObjectType):

    id = graphene.ID()
    cpf = graphene.String()
    email = graphene.String()
    username = graphene.String()

    fullname = graphene.String()
    password = graphene.String()

    created_at = graphene.Date()
    updated_at = graphene.Date()

    reset_password_key = graphene.String()
    reset_password_key_validity = graphene.Date()

    organizations = graphene.List(OrganizationObject)
    locations     = graphene.List(LocationObject)
    providers     = graphene.List(ProviderObject)
    exam_types    = graphene.List(ExamTypeObject)


# ]
#
##
# class UserObject(SQLAlchemyObjectType):
#     class Meta:
#         model = User
#         interfaces = (graphene.relay.Node,)


# class OrganizationObject(SQLAlchemyObjectType):
#     class Meta:
#         model = Organization
#         interfaces = (graphene.relay.Node,)
