import bcrypt
from database import db


class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    
    description = db.Column(db.String(), nullable=False)

    photo_url = db.Column(db.String(), nullable=False)

    procedure_code = db.Column(db.String(), nullable=True)

    date_for_receipt = db.Column(db.Date())

    cut_off_date = db.Column(db.Date())

    fk_exam_types_id = db.Column(db.Integer, db.ForeignKey("exam_types.id"), nullable=False)
    exam_type = db.relationship("ExamType", foreign_keys="Exam.fk_exam_types_id")

    fk_locations_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    location = db.relationship("Location", foreign_keys="Exam.fk_locations_id")

    fk_providers_id = db.Column(db.Integer, db.ForeignKey("providers.id"), nullable=False)
    provider = db.relationship("Provider", foreign_keys="Exam.fk_providers_id")

    fk_health_plans_id = db.Column(db.Integer, db.ForeignKey("health_plans.id"), nullable=False)
    health_plan = db.relationship("HealthPlan", foreign_keys="Exam.fk_health_plans_id")
    
    fk_users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", foreign_keys="Exam.fk_users_id")

    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(ex)
            raise Exception("Ocorreu um erro ao inserir local de atendimento!")

    def delete(self):
        db.session.query(Exam.id == self.id).delete()
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "address": self.address,
            "city": self.city,
            "state": self.state,
        }

    # -----------------------------------------------------
    # GRAPHQL
    # -----------------------------------------------------
    @classmethod
    def resolve_exams(cls, authorizedUser, **kwargs):
        query = db.session.query(Exam)

        id, description, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("l_description"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )

        provider_id = kwargs.get("provider_id");
        location_id = kwargs.get("location_id");
        exam_type_id = kwargs.get("exam_type_id");

        begin = kwargs.get("begin");
        end = kwargs.get("end");

        query = query.filter(cls.fk_users_id == authorizedUser.id)

        if id is not None:
            query = query.filter(Exam.id == id)

        if provider_id is not None:
            query = query.filter(cls.fk_providers_id == id)

        if location_id is not None:
            query = query.filter(cls.fk_locations_id == id)

        if exam_type_id is not None:
            query = query.filter(cls.fk_exam_types_id == id)

        
        if begin is not None:
            query = query.filter(cls.created_at >= begin)

        
        if end is not None:
            query = query.filter(cls.created_at <= end)


        if description is not None:
            query = query.filter(Exam.description.like(f"%{description}%"))

        return query.offset(page_index * page_size).limit(page_size)

    @classmethod
    def resolve_exam(cls, authorizedUser, **kwargs):
        query = db.session.query(Exam)
        query = query.filter(cls.fk_users_id == authorizedUser.id)
        id = kwargs.get("id")
        return query.filter(Exam.id == id).first()
