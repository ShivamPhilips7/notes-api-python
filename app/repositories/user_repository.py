import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

logger = logging.getLogger(__name__)

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        logger.info(f"Fetching user with username: {username}")

        result = await self.db.execute(
            select(User).where(
                User.username == username
            )
        )

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        logger.info(f"Fetching user with email: {email}")

        result = await self.db.execute(
            select(User).where(
                User.email == email
            )
        )

        return result.scalar_one_or_none()

    async def create_user(
        self,
        user: User,
    ) -> User:
        logger.info(f"Creating user: {user.username}")

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user