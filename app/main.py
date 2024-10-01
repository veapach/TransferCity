import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from .config import Config
from .handlers import (
    registration,
    transfer,
    rewards,
    referrals,
    admin,
    balance,
    buy_points,
)
from .utils.scheduler import run_scheduler
from .database import engine, Base
from .models.user import User
from .models.referral import Referral
from aiogram import exceptions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_error(event, exception):
    print(f"Ошибка: {exception}")


async def on_startup(dispatcher: Dispatcher):
    # Если еще нет, то создаем таблицы в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована")

    # Запуск планировщика задач
    asyncio.create_task(run_scheduler())
    print("Планировщик задач запущен")


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await dispatcher.bot.close()
    print("Бот остановлен")


async def main():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Инициализация бота и диспетчера
    bot = Bot(
        token=Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация обработчиков
    dp.errors.register(on_error)
    registration.register_handlers(dp)
    transfer.register_handlers(dp)
    referrals.register_handlers(dp)
    admin.register_handlers(dp)
    balance.register_handlers(dp)
    buy_points.register_handlers(dp)

    # Запуск бота
    await dp.start_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    asyncio.run(main())
