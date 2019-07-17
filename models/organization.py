import bcrypt
import json
from datetime import datetime

from database import db

class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(256), index=True, unique=True)
    description = db.Column(db.String(256))

    created_at = db.Column(db.Date())
    updated_at = db.Column(db.Date())

    users = db.relationship("User", 
                                secondary="users_organizations", backref='organization')
    
    def __init__(self, *args, **kwargs):
        self.id          = None
        self.cpf_cnpj    = kwargs.get('cpf_cnpj', None)
        self.description = kwargs.get('description', None)
        self.created_at  = kwargs.get('created_at', datetime.now())
        self.updated_at  = kwargs.get('updated_at', datetime.now())

        if self.cpf_cnpj is None:
            raise Exception('Informe o CPF ou CNPJ!')
        elif self.description is None:
            raise Exception('Informe a descrição!')

    def json(self):
        return {
            "id": self.id,
            "cpf_cnpj": self.cpf_cnpj,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def save(self):
        print('Saving Organization')
        db.session.add(self)
        db.session.commit()
    
    
    @classmethod
    def resolve_organizations(cls, **kwargs):
        query = db.session.query(Organization)
        id, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
        if id is not None:
            query = query.filter(Organization.id == id)

        return query.offset(page_index * page_size).limit(page_size)

    @classmethod
    def resolve_organization(cls, **kwargs):
        query = db.session.query(Organization)
        id = kwargs.get("id")
        return query.filter(Organization.id == id).first()
