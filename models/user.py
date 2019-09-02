import bcrypt
import json
import time
from datetime import datetime

from database import db, Base
from libs.cpf import CPFValidator

from models.organization import Organization

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(256), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    username = db.Column(db.String(256), index=True, unique=True)

    fullname = db.Column(db.String(256))
    password = db.Column(db.String(256))

    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    fk_organizations_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    organization = db.relationship("Organization", foreign_keys="User.fk_organizations_id")

    def __init__(self, *args, **kwargs):
        self.id = None
        self.cpf = kwargs.get("cpf", None)
        self.email = kwargs.get("email", None)
        self.fullname = kwargs.get("fullname", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reset_password_key = None
        self.reset_password_key_validity = None

        if self.cpf is None:
            raise Exception("Informe o CPF!")
        elif self.email is None:
            raise Exception("Informe o Email!")
        elif self.fullname is None:
            raise Exception("Informe o Nome Completo!")
        elif self.password is None:
            raise Exception("Informe uma Senha!")

    def json(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "email": self.email,
            "fullname": self.fullname,
            "username": self.username,
            "created_at": time.mktime(self.created_at.timetuple()) * 1e3
            + self.created_at.microsecond / 1e3,
            "updated_at": time.mktime(self.updated_at.timetuple()) * 1e3
            + self.updated_at.microsecond / 1e3,
        }

    @classmethod
    def check_cpf(cls, cpf):
        return CPFValidator(cpf).valid()

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    @classmethod
    def check_password(cls, password, hash):
        return bcrypt.checkpw(password.encode("utf8"), hash.encode("utf8"))

    def register(self):
        cpf_check = True  # User.check_cpf(self.cpf)

        if cpf_check:
            self.password = User.hash_password(self.password)

            organization = Organization(cpf_cnpj=self.cpf, description=self.fullname)
            organization.save()
            self.organization = organization
            self.fk_organizations_id = organization.id

            # creates an User.
            db.session.add(self)
            db.session.commit()

        else:
            raise Exception("CPF Inválido!")

    def save(self):
        cpf_check = User.check_cpf(self.cpf)

        if cpf_check:
            self.password = User.hash_password(self.password)

            organization = Organization(cpf_cnpj=self.cpf, description=self.fullname)
            organization.save()

            # creates an User.
            db.session.add(self)
            db.session.commit()

        else:
            raise Exception("CPF Inválido!")

    # ---------------------------------------------------------------------------------------------
    # Queries.
    # ---------------------------------------------------------------------------------------------
    @classmethod
    def find_by_cpf(cls, cpf):
        return db.session.query(User).filter(User.cpf == cpf).first()

    @classmethod
    def find_by_email(cls, email):
        return db.session.query(User).filter(User.email == email).first()

    # ---------------------------------------------------------------------------------------------
    # GraphQL Resolvers.
    # ---------------------------------------------------------------------------------------------
    @classmethod
    def resolve_user(cls, authorized_user, **kwargs):
        query = db.session.query(User)
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)
        uuid = kwargs.get("uuid")
        return query.get(uuid)

    @classmethod
    def resolve_users(cls, authorized_user, **kwargs):
        user_query = db.session.query(User)
        id, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)
        if id is not None:
            user_query = user_query.filter(User.id == id)
        return user_query.offset(page_index * page_size).limit(page_size)
