# GraphQL
from graphene import Mutation, Field, String, Int, Date
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_schemas.objects import ExamObject

# Authentication
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from models.user import User
from models.exam_type import ExamType
from models.locations import Location
from models.provider import Provider
from models.provider import Provider
from models.health_plan import HealthPlan
from models.exam import Exam


class CreateExam(Mutation):
    """ GraphQL Mutation for creating a Provider. """

    class Arguments:
        description = String(required=True)

        photo_url = String(required=True)
        procedure_code = String(required=False)
        date_for_receipt = Date(required=False)
        cut_off_date = Date(required=False)

        exam_type_id = Int(required=True)
        location_id = Int(required=True)
        provider_id = Int(required=True)
        health_plan_id = Int(required=True)

    exam = Field(lambda: ExamObject)

    @jwt_required
    def mutate(self, info, **args):
        current_user = User.find_by_email(get_jwt_identity())

        description = args.get("description")
        photo_url = args.get("photo_url")
        procedure_code = args.get("procedure_code")
        date_for_receipt = args.get("date_for_receipt")
        cut_off_date = args.get("cut_off_date")

        exam_type = ExamType.find_by_id(args.get("exam_type_id"))
        location = Location.find_by_id(args.get("location_id"))
        provider = Provider.find_by_id(args.get("provider_id"))
        health_plan = HealthPlan.find_by_id(args.get("health_plan_id"))

        exam = Exam(
            description=args.get("description"),
            #
            photo_url=photo_url,
            procedure_code=procedure_code,
            date_for_receipt=date_for_receipt,
            cut_off_date=cut_off_date,
            #
            exam_type=exam_type,
            location=location,
            provider=provider,
            health_plan=health_plan,
            #
            user=current_user,
        )
        exam.save()

        return CreateExam(exam=exam)

