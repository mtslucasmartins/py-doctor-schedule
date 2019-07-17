import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from graphql_schemas.queries import Query
from graphql_schemas.mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
