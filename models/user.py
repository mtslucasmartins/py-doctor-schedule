import bcrypt
import json
from datetime import datetime

from database import db, Base
from libs.cpf import CPFValidator

from models.organization import Organization
from models.users_organizations import UserOrganization
from models.locations import Location


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(256), index=True, unique=True)
    email = db.Column(db.String(256), index=True, unique=True)
    username = db.Column(db.String(256), index=True, unique=True)
    username2 = db.Column(db.String(256), index=True, unique=True)

    fullname = db.Column(db.String(256))
    password = db.Column(db.String(256))

    created_at = db.Column(db.Date())
    updated_at = db.Column(db.Date())

    reset_password_key = db.Column(db.String(256))
    reset_password_key_validity = db.Column(db.Date())

    organizations = db.relationship(
        "Organization", secondary="users_organizations", uselist=True, backref="user"
    )

    locations = db.relationship("Location", uselist=True)
    providers = db.relationship("Provider", uselist=True)
    exam_types = db.relationship("ExamType", uselist=True)

    def __init__(self, *args, **kwargs):
        self.id = None
        self.cpf = kwargs.get("cpf", None)
        self.email = kwargs.get("email", None)
        self.fullname = kwargs.get("fullname", None)
        self.username = kwargs.get("username", None)
        self.username2 = kwargs.get("username2", None)
        self.password = kwargs.get("password", None)
        self.created_at = kwargs.get("created_at", datetime.now())
        self.updated_at = kwargs.get("updated_at", datetime.now())
        self.organizations = kwargs.get("organizations", [])
        self.locations = kwargs.get("locations", [])
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
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

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

    @classmethod
    def find_by_email(cls, email):
        return db.session.query(User).filter(User.email == email).first()

    @classmethod
    def check_cpf(cls, cpf):
        return CPFValidator(cpf).valid()

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    @classmethod
    def check_password(cls, password, hash):
        return bcrypt.checkpw(password.encode("utf8"), hash.encode("utf8"))

    @classmethod
    def resolve_users(cls, **kwargs):
        user_query = db.session.query(User)
        id, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
        if id is not None:
            user_query = user_query.filter(User.id == id)
        return user_query.offset(page_index * page_size).limit(page_size)

    @classmethod
    def resolve_user(cls, **kwargs):
        query = db.session.query(User)
        uuid = kwargs.get("uuid")
        return query.get(uuid)

