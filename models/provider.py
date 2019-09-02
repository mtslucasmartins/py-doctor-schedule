import bcrypt
from database import db


class Provider(db.Model):
    __tablename__ = "providers"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    fk_organizations_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    organization = db.relationship("Organization", foreign_keys="Provider.fk_organizations_id")

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
    def find_by_id(cls, id):
        return db.session.query(cls).filter(cls.id == id).first()


    @classmethod
    def resolve_provider(cls, authorized_user, **kwargs):
        query = db.session.query(Provider)
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)
        id = kwargs.get("id")
        return query.filter(Provider.id == id).first()

    @classmethod
    def resolve_providers(cls, authorized_user, **kwargs):
        query = db.session.query(Provider)
        id, description, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("l_description"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
    
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)

        if id is not None:
            query = query.filter(Provider.id == id)
        if description is not None:
            query = query.filter(Provider.description.like(f"%{description}%"))

        return query.offset(page_index * page_size).limit(page_size)

