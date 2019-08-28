from flask_jwt_extended import jwt_required, get_jwt_identity

from graphql_schemas.objects import LocationObject
from graphql_schemas.objects import UserObject
from graphql_schemas.objects import ExamTypeObject

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from models.user import User
from models.locations import Location
from models.exam_type import ExamType
from database import db


from graphql_schemas.mutations.create_provider import CreateProvider
from graphql_schemas.mutations.create_provider import CreateHealthPlan
from graphql_schemas.mutations.create_exam import CreateExam


class CreateLocation(graphene.Mutation):
    class Arguments:
        description = graphene.String(required=True)

    location = graphene.Field(lambda: LocationObject)

    @jwt_required
    def mutate(self, info, **args):
        current_user = User.find_by_email(get_jwt_identity())
        location = Location(description=args.get("description"), organization=current_user.organization)
        location.save()
        return CreateLocation(location=location)


class CreateExamType(graphene.Mutation):
    class Arguments:
        description = graphene.String(required=True)

    examType = graphene.Field(lambda: ExamTypeObject)

    @jwt_required
    def mutate(self, info, **args):
        current_user = User.find_by_email(get_jwt_identity())
        examType = ExamType(description=args.get("description"), organization=current_user.organization)
        examType.save()
        return CreateExamType(examType=examType)


class CreateUser(graphene.Mutation):
    class Arguments:
        cpf = graphene.String(required=True)
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        fullname = graphene.String(required=True)

    user = graphene.Field(lambda: UserObject)

    @jwt_required
    def mutate(self, info, **args):
        user = User(
            cpf=args.get("cpf"),
            email=args.get("email"),
            username=args.get("username"),
            password=args.get("password"),
            fullname=args.get("fullname"),
        )

        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_location = CreateLocation.Field()
    create_exam_type = CreateExamType.Field()
    create_provider = CreateProvider.Field()
    create_health_plan = CreateHealthPlan.Field()
    create_exam = CreateExam.Field()
