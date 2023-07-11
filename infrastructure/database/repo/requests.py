from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.repo.users import UserRepo


class RequestsRepo:
    """
    Database class is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions
    """

    user: UserRepo
    """ User repository """

    session: AsyncSession

    def __init__(
            self, session: AsyncSession, user: UserRepo = None
    ):
        self.session = session
        self.user = user or UserRepo(session=session)
        # self.chat = chat or ChatRepo(session=session)

# def example_usage():
#     from infrastructure.database.setup import create_session_pool
#     from tgbot.config import load_config
#
#     config = load_config()
#     engine = create_engine(config.db)
#     session_pool = create_session_pool(engine)
#
#     async with session_pool() as session:
#         repo = RequestsRepo(session)
#         await repo.users.create_user()
#         ...
