import bcrypt
import json
from datetime import datetime

from database import db


class UserOrganization(db.Model):
    __tablename__ = 'users_organizations'

    fk_users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fk_organizations_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), primary_key=True)

    user = db.relationship('User', foreign_keys='UserOrganization.fk_users_id')
    organization = db.relationship('Organization', foreign_keys='UserOrganization.fk_organizations_id')