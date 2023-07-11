import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.i18n import I18n

# from aiogram_dialog import setup_dialogs

from infrastructure.database.setup import create_engine, create_session_pool
from tgbot.config import load_config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.language import BaseI18nMiddleware
from tgbot.services import broadcaster

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config, i18n, session_pool=None):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.outer_middleware(DatabaseMiddleware(session_pool))
    dp.callback_query.outer_middleware(DatabaseMiddleware(session_pool))

    dp.message.outer_middleware(BaseI18nMiddleware(i18n=i18n))
    dp.callback_query.outer_middleware(BaseI18nMiddleware(i18n=i18n))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    if config.tg_bot.use_redis:
        storage = RedisStorage.from_url(config.redis.dsn(),
                                        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True))
    else:
        storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)
    i18n = I18n(path="tgbot/locales", default_locale="uz", domain="messages")

    dp.include_routers(*routers_list)

    # aiogram_dialog register
    # dp.include_router(bg_dialog)
    # dp.include_router(dialog)
    # setup_dialogs(dp)

    register_global_middlewares(
        dp,
        config,
        i18n,
        session_pool=session_pool,
    )

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
