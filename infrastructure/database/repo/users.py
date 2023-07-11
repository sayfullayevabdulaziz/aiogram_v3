""" User repository file """
from typing import Optional

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models.user import User
from infrastructure.database.repo.base import Repository


class UserRepo(Repository[User]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository as for all users or only for one user
        """
        super().__init__(type_model=User, session=session)

    async def new(
            self,
            user_id: int,
            language: str,
            username: Optional[str] = None,
            name: Optional[str] = None,
    ) -> None:
        sql = insert(User).values(user_id=user_id, name=name, language=language)
        await self.session.execute(sql)
        await self.session.commit()

    async def get_by_language(self, user_id: int) -> User.language:
        sql = select(User.language).filter(User.user_id == user_id)
        request = await self.session.execute(sql)
        return request.scalar()

    async def update_language(self, user_id: int, language: str):
        sql = update(User).where(User.user_id == user_id).values({'language': language})
        await self.session.execute(sql)
        await self.session.commit()
