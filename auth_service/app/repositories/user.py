from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        query = await self.session.execute(select(User).where(User.email == email))
        return query.scalar_one_or_none()

    async def create(self, data: dict) -> User:
        user = User(**data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user