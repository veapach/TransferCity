# app/handlers/rewards.py

# Этот файл не требует регистрации обработчиков, так как награды начисляются автоматически через планировщик.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..models.referral import Referral
import datetime


async def award_daily_rewards(session: AsyncSession):
    # Получаем всех пользователей, отсортированных по рейтинговым очкам
    result = await session.execute(select(User).order_by(User.rating_points.desc()))
    users = result.scalars().all()

    # Обновляем глобальные ранги
    for rank, user in enumerate(users, start=1):
        user.global_rank = rank

    await session.commit()

    # Начисляем ежедневные награды
    for user in users:
        daily_reward = user.global_rank * 5
        if user.is_premium:
            daily_reward = int(daily_reward * 1.4)  # 40% бонус для премиум
        user.balance += daily_reward
        user.last_daily_reward = datetime.datetime.utcnow()

        # Начисляем реферальные бонусы
        if user.referrer_id:
            referrer = await session.get(User, user.referrer_id)
            if referrer:
                referrer.balance += int(
                    daily_reward * 0.10
                )  # 10% от ежедневных наград реферала

    await session.commit()
