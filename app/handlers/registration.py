from aiogram import types, Dispatcher
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..models.referral import Referral
from ..database import get_db
from aiogram.types import Message


async def cmd_start(message: Message, session: AsyncSession):
    telegram_id = str(message.from_user.id)

    # Проверка зарегистрирован ли пользователь
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()

    if user:
        await message.answer("Вы уже зарегистрированы!")
        return

    # Проверка есть ли реферальный код
    referrer_id = None
    parts = message.text.split()
    if len(parts) > 1:
        ref_code = parts[1]
        # Реферальный код - ТГ id реферера
        ref_result = await session.execute(
            select(User).where(User.telegram_id == ref_code)
        )
        referrer = ref_result.scalars().first()
        if referrer:
            referrer_id = referrer.id
            # Добавляем запись о реферале
            new_referral = Referral(
                referrer_id=referrer.id, referee_id=0
            )  # Пока 0, обновление будет позже
            session.add(new_referral)
            # Начисляем бонус рефереру
            referrer.balance += 1000  # Базовый бонус
            print(f"Пользователь {referrer.telegram_id} получил бонус за реферала.")

    # Создаем нового пользователя
    new_user = User(
        telegram_id=telegram_id, balance=100, rating_points=100, referrer_id=referrer_id
    )
    session.add(new_user)
    await session.commit()

    # Обновление referee_id в рефералах
    if referrer_id:
        # Получаем последнюю рефералку
        result = await session.execute(
            select(Referral)
            .where(Referral.referee_id == referrer_id)
            .order_by(Referral.id.desc())
        )
        referral = result.scalars().first()
        if referral:
            referral.referee_id = new_user.id
            await session.commit()

    await message.answer("Регистрация прошла успешно! Ваш баланс: 100 понитов")


def register_handler(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
