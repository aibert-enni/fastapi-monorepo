from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory.faker import Faker

from app.models.user import UserOrm


class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = UserOrm

    first_name = Faker("first_name")
    last_name = Faker("last_name")
