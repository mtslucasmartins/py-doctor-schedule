import bcrypt
from database import db


class ExamItem(db.Model):
    __tablename__ = "exam_items"

    id = db.Column(db.Integer, primary_key=True)

    procedure_code = db.Column(db.String(), nullable=True)

    cost = db.Column(db.Float(), nullable=True)

    fk_exams_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    exam = db.relationship("Exam", foreign_keys="ExamItem.fk_exams_id")

    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(ex)
            raise Exception("Ocorreu um erro ao inserir item do atendimento!")

    def delete(self):
        db.session.query(ExamItem.id == self.id).delete()
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
    def resolve_exam_items(cls, authorizedUser, **kwargs):
        query = db.session.query(cls)

        id, procedure_code, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("procedure_code"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )

        exam_id = kwargs.get("exam_id")

        # query = query.filter(cls.fk_users_id == authorizedUser.id)

        if id is not None:
            query = query.filter(cls.id == id)

        if exam_id is not None:
            query = query.filter(cls.fk_exams_id == exam_id)

        if procedure_code is not None:
            query = query.filter(cls.procedure_code.like(f"%{procedure_code}%"))

        return query.offset(page_index * page_size).limit(page_size)

    @classmethod
    def resolve_exam_item(cls, authorizedUser, **kwargs):
        query = db.session.query(cls)
        # query = query.filter(cls.fk_users_id == authorizedUser.id)
        id = kwargs.get("id")
        return query.filter(cls.id == id).first()
