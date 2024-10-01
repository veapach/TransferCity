# app/utils/scheduler.py

import aioschedule
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import engine
from ..handlers.rewards import award_daily_rewards


async def run_daily_rewards():
    # Эта функция вызывает функцию начисления ежедневных наград
    async with engine.connect() as conn:
        async with AsyncSession(conn) as session:
            await award_daily_rewards(session)


async def run_scheduler():
    # Планируем выполнение функции run_daily_rewards каждый день в 00:00
    aioschedule.every().day.at("00:00").do(run_daily_rewards)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
