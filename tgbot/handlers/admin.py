from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("help"))
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")
