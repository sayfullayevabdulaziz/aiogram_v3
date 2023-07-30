from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from infrastructure.database.models.user import User
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.data.callback_data import LanguageCallback
from tgbot.keyboards.inline.language import get_lang_fab

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, repo: RequestsRepo):
    user = await repo.user.get_by_where(User.user_id == message.from_user.id)
    if user is None:
        await message.answer(
            text='Assalomu Alaykum! Kerakli tilni tanlang\n'
                 'Здравствуйте! Выберите необходимый язык',
            reply_markup=get_lang_fab()
        )
    else:
        await message.answer(
            text=_('Asosiy menu')
        )


@user_router.callback_query(LanguageCallback.filter())
async def user_save_from_fab(query: CallbackQuery, callback_data: LanguageCallback, repo: RequestsRepo):
    language_code = callback_data.language_code
    user = await repo.user.get_by_where(User.user_id == query.from_user.id)
    if user is None:
        await repo.user.new(
            user_id=query.from_user.id,
            language=language_code,
            username=query.from_user.username,
            name=query.from_user.full_name
        )

    else:
        await repo.user.update_language(
            user_id=query.from_user.id,
            language=language_code
        )
    await query.message.edit_text(
        text=_('Asosiy menu', locale=language_code)
    )