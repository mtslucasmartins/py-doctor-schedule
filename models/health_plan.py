import bcrypt
from database import db


class HealthPlan(db.Model):
    __tablename__ = "health_plans"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    
    # dias para recebimento
    days_for_receipt = db.Column(db.Integer(), nullable=True)

    # data/dia de corte
    cut_off_day = db.Column(db.Integer(), nullable=True)

    fk_providers_id = db.Column(db.Integer, db.ForeignKey("providers.id"), nullable=False)
    provider = db.relationship("Provider", foreign_keys="HealthPlan.fk_providers_id")
    
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
        db.session.query(HealthPlan.id == self.id).delete()
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
    def resolve_health_plan(cls, authorized_user, **kwargs):
        query = db.session.query(cls)
        id = kwargs.get("id")
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)
        return query.filter(cls.id == id).first()

    @classmethod
    def resolve_health_plans(cls, authorized_user, **kwargs):
        query = db.session.query(cls)

    

        id, description, provider_id, page_index, page_size = (
            kwargs.get("id"),
            kwargs.get("l_description"),
            kwargs.get("provider_id"),
            kwargs.get("page_index", 0),
            kwargs.get("page_size", 10),
        )
        
        query = query.filter(cls.fk_organizations_id == authorized_user.fk_organizations_id)

        if id is not None:
            query = query.filter(cls.id == id)
            
        if provider_id is not None:
            query = query.filter(cls.fk_providers_id == provider_id)

        if description is not None:
            query = query.filter(cls.description.like(f"%{description}%"))

        return query.offset(page_index * page_size).limit(page_size)

