# app/handlers/admin.py

from aiogram import types, Dispatcher
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..database import get_db
from ..config import Config
from aiogram.types import Message


async def cmd_admin_panel(message: Message, session: AsyncSession):
    # Проверяем, является ли пользователь администратором
    if message.from_user.id != Config.ADMIN_TELEGRAM_ID:
        await message.answer("У вас нет доступа к этой команде.")
        return

    # Получаем список всех пользователей
    result = await session.execute(select(User))
    users = result.scalars().all()

    user_count = len(users)
    total_balance = sum(user.balance for user in users)
    total_rating = sum(user.rating_points for user in users)

    admin_info = (
        f"📊 Админ-панель:\n\n"
        f"👥 Всего пользователей: {user_count}\n"
        f"💰 Общий баланс поинтов: {total_balance}\n"
        f"⭐ Общие рейтинговые очки: {total_rating}\n"
    )

    await message.answer(admin_info)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_admin_panel, Command(commands=["admin"]))
