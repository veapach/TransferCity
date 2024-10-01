# app/handlers/referrals.py

from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..models.referral import Referral
from ..database import get_db
from aiogram.types import Message


async def cmd_referrals(message: Message, session: AsyncSession):
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

    # Получаем список рефералов
    result = await session.execute(
        select(Referral).where(Referral.referrer_id == user.id)
    )
    referrals = result.scalars().all()

    if not referrals:
        await message.answer("У вас пока нет рефералов.")
        return

    referral_info = "Ваши рефералы:\n"
    for ref in referrals:
        referee = await session.get(User, ref.referee_id)
        if referee:
            referral_info += f"- {referee.telegram_id} (Уровень: {ref.level})\n"

    await message.answer(referral_info)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_referrals, Command(commands=["referrals"]))
