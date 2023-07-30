from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tgbot.config import Config


def create_engine(db_config: Config, echo=False):
    engine = create_async_engine(
        db_config.POSTGRES_DSN,
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
    )
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
