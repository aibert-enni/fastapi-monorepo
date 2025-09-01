import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from app.models.auth import AuthOrm
from app.utils.password import hash_password


class AuthFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = AuthOrm

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    is_active = True
    is_superuser = False

    @factory.lazy_attribute
    def hashed_password(self):
        raw_password = "1234qwer"
        return hash_password(raw_password)
