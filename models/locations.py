import bcrypt
from database import db


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    fk_organizations_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id"), nullable=False
    )
    organization = db.relationship(
        "Organization", foreign_keys="Location.fk_organizations_id"
    )

    def __init__(self, *args, **kwargs):
        self.id = None
        self.description = kwargs.get("description", None)
        self.organization = kwargs.get("organization", None)

        if self.description is None:
            raise Exception("Informe a descrição do local!")

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(ex)
            raise Exception("Ocorreu um erro ao inserir local de atendimento!")

    def delete(self):
        db.session.query(Location.id == self.id).delete()
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
    def resolve_locations(cls, authorized_user, **kwargs):
        query = db.session.query(Location)
        id, description, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("l_description"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)
        if id is not None:
            query = query.filter(Location.id == id)
        if description is not None:
            query = query.filter(Location.description.like(f"%{description}%"))
        return query.offset(page_index * page_size).limit(page_size)

    @classmethod
    def resolve_location(cls, authorized_user, **kwargs):
        query = db.session.query(Location)
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)
        id = kwargs.get("id")
        return query.filter(Location.id == id).first()
