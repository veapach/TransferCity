# app/handlers/balance.py

from aiogram import types, Dispatcher
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..database import get_db
from aiogram.types import Message


async def cmd_balance(message: Message, session: AsyncSession):
    user_telegram_id = str(message.from_user.id)

    # Получаем пользователя
    result = await session.execute(
        select(User).where(User.telegram_id == user_telegram_id)
    )
    user = result.scalars().first()

    if not user:
        await message.answer(
            "Вы не зарегистрированы. Используйте /start для регистрации."
        )
        return

    await message.answer(
        f"💰 Ваш баланс: {user.balance} поинтов\n⭐ Рейтинговые очки: {user.rating_points}\n📈 Место в рейтинге: {user.global_rank}"
    )


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_balance, Command(commands=["balance"]))
