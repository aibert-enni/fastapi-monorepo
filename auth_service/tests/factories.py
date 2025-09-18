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

    @classmethod
    async def create(cls, session, **kwargs):
        cls._meta.sqlalchemy_session = session
        instance = await super().create(**kwargs)
        # one commit per build to avoid share the same connection
        await session.commit()
        return instance

    @factory.lazy_attribute
    def hashed_password(self):
        raw_password = "1234qwer"
        return hash_password(raw_password)
