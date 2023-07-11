from typing import Dict, Any, Optional

from aiogram.types import TelegramObject, User
from aiogram.utils.i18n import I18nMiddleware, I18n

from infrastructure.database.repo.requests import RequestsRepo


class BaseI18nMiddleware(I18nMiddleware):
    def __init__(
            self,
            i18n: I18n,
            i18n_key: Optional[str] = "i18n",
            middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)

        repo: RequestsRepo = data.get("repo")
        language_db = await repo.user.get_by_language(user_id=event_from_user.id)
        if language_db:
            return language_db
        return self.i18n.default_locale
