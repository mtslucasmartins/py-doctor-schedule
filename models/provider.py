import bcrypt
from database import db


class Provider(db.Model):
    __tablename__ = "providers"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    fk_users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", foreign_keys="Provider.fk_users_id")

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(ex)
            raise Exception("Ocorreu um erro ao inserir local de atendimento!")

    def delete(self):
        db.session.query(Provider.id == self.id).delete()
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

    @classmethod
    def resolve_provider(cls, **kwargs):
        query = db.session.query(Provider)
        id = kwargs.get("id")
        return query.filter(Provider.id == id).first()

    @classmethod
    def resolve_providers(cls, **kwargs):
        query = db.session.query(Provider)
        id, description, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("l_description"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
        if id is not None:
            query = query.filter(Provider.id == id)
        if description is not None:
            query = query.filter(Provider.description.like(f"%{description}%"))

        return query.offset(page_index * page_size).limit(page_size)

