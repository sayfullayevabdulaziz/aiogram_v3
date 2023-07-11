from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.data.callback_data import LanguageCallback

languages = {
    "ru": "🇷🇺 Русский",
    "uz": "🇺🇿 O'zbek"
}


def get_lang_fab():
    builder = InlineKeyboardBuilder()
    for language_code, language_name in languages.items():
        builder.row(
            InlineKeyboardButton(
                text=language_name,
                callback_data=LanguageCallback(language_code=language_code).pack()
            ))
    return builder.as_markup()
