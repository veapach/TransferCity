# app/handlers/registration.py

from asyncio.log import logger
from aiogram import types, Dispatcher
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..models.referral import Referral
from ..database import SessionLocal
from aiogram.types import Message


async def cmd_start(message: Message):
    telegram_id = str(message.from_user.id)

    async with SessionLocal() as session:
        # Проверяем, зарегистрирован ли пользователь
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if user:
            await message.answer("Вы уже зарегистрированы!")
            return

        # Проверяем, есть ли реферальный код
        referrer_id = None
        parts = message.text.split()
        if len(parts) > 1:
            ref_code = parts[1]
            # Предполагаем, что реферальный код — это Telegram ID реферера
            ref_result = await session.execute(
                select(User).where(User.telegram_id == ref_code)
            )
            referrer = ref_result.scalars().first()
            if referrer:
                referrer_id = referrer.id
                # Начисляем бонус рефереру
                referrer.balance += 1000  # Базовый бонус
                logger.info(
                    f"Пользователь {referrer.telegram_id} получил бонус за реферала."
                )

        # Создаем нового пользователя
        new_user = User(
            telegram_id=telegram_id,
            balance=100,
            rating_points=100,
            referrer_id=referrer_id,
        )
        session.add(new_user)
        await session.commit()

        # Если есть реферер, создаем запись о реферале
        if referrer_id:
            # Получаем только что созданного пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            new_user = result.scalars().first()
            new_referral = Referral(
                referrer_id=referrer_id, referee_id=new_user.id, level=1
            )
            session.add(new_referral)
            await session.commit()

        await message.answer("Регистрация прошла успешно! Ваш баланс: 100 поинтов.")


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
