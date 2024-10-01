# app/handlers/buy_points.py

from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..models.purchase import Purchase
from ..database import get_db
from aiogram.types import Message


class BuyPointsStates(StatesGroup):
    waiting_for_choice = State()


async def cmd_buy_points(message: Message, state: FSMContext, session: AsyncSession):
    # Показываем варианты покупки
    buy_options = (
        "Выберите пакет поинтов:\n"
        "1. 100 поинтов за 50 руб.\n"
        "2. 600 поинтов за 250 руб.\n"
        "3. 1500 поинтов за 500 руб.\n"
    )
    await message.answer(buy_options)
    await state.set_state(BuyPointsStates.waiting_for_choice)


async def process_buy_choice(
    message: Message, state: FSMContext, session: AsyncSession
):
    choice = message.text.strip()

    # Определяем пакет по выбору пользователя
    packages = {
        "1": {"points": 100, "price": 50},
        "2": {"points": 600, "price": 250},
        "3": {"points": 1500, "price": 500},
    }

    package = packages.get(choice)

    if not package:
        await message.answer("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
        return

    # Здесь должна быть интеграция с платежной системой.
    # Для простоты, будем считать, что оплата прошла успешно.

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
        await state.clear()
        return

    # Начисляем поинты
    user.balance += package["points"]

    # Создаем запись о покупке
    new_purchase = Purchase(
        user_id=user.id, amount=package["points"], currency_type="points"
    )
    session.add(new_purchase)
    await session.commit()

    await message.answer(
        f"🎉 Вы успешно купили {package['points']} поинтов за {package['price']} руб."
    )
    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_buy_points, Command(commands=["buy_points"]))
    dp.message.register(process_buy_choice)
