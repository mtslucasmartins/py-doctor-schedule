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


class HealthPlanObject(graphene.ObjectType):

    id = graphene.ID()

    description = graphene.String()
    days_for_receipt = graphene.Int()
    cut_off_day = graphene.Int()

    provider = graphene.Field(ProviderObject)


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

    organization = graphene.Field(OrganizationObject)

class ExamObject(graphene.ObjectType):

    id = graphene.ID()
    
    description = graphene.String()
    photo_url = graphene.String()
    procedure_code = graphene.String()
    date_for_receipt = graphene.Date()
    cut_off_date = graphene.Date()

    location = graphene.Field(LocationObject)
    exam_type = graphene.Field(ExamTypeObject)
    provider = graphene.Field(ProviderObject)
    health_plan = graphene.Field(HealthPlanObject)
    user = graphene.Field(UserObject)

    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
