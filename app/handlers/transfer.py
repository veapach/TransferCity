# app/handlers/transfer.py

from aiogram import types, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from ..models.transfer import Transfer
from ..database import get_db
from aiogram.types import Message


class TransferStates(StatesGroup):
    waiting_for_receiver = State()
    waiting_for_amount = State()


async def cmd_transfer(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer("Введите Telegram ID получателя:")
    await state.set_state(TransferStates.waiting_for_receiver)


async def process_receiver(message: Message, state: FSMContext, session: AsyncSession):
    receiver_telegram_id = message.text.strip()

    # Проверяем, существует ли получатель
    result = await session.execute(
        select(User).where(User.telegram_id == receiver_telegram_id)
    )
    receiver = result.scalars().first()

    if not receiver:
        await message.answer("Пользователь не найден. Попробуйте еще раз.")
        return

    # Сохраняем ID получателя в состоянии
    await state.update_data(receiver_id=receiver.id)

    await message.answer(
        "Введите количество поинтов для передачи (минимум 10, максимум 100):"
    )
    await state.set_state(TransferStates.waiting_for_amount)


async def process_amount(message: Message, state: FSMContext, session: AsyncSession):
    try:
        amount = int(message.text.strip())
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    if amount < 10 or amount > 100:
        await message.answer(
            "Минимальная сумма перевода — 10 поинтов, максимальная — 100."
        )
        return

    user_telegram_id = str(message.from_user.id)

    # Получаем отправителя
    result = await session.execute(
        select(User).where(User.telegram_id == user_telegram_id)
    )
    sender = result.scalars().first()

    if not sender:
        await message.answer(
            "Вы не зарегистрированы. Используйте /start для регистрации."
        )
        await state.clear()
        return

    # Получаем данные из состояния
    data = await state.get_data()
    receiver_id = data.get("receiver_id")

    # Получаем получателя
    receiver = await session.get(User, receiver_id)

    if not receiver:
        await message.answer("Получатель не найден.")
        await state.clear()
        return

    # Рассчитываем комиссию
    commission = int(amount * 0.05)
    total_deduction = amount + commission

    if sender.balance < total_deduction:
        await message.answer("Недостаточно поинтов для передачи (включая комиссию).")
        await state.clear()
        return

    # Обновляем балансы
    sender.balance -= total_deduction
    receiver.balance += amount

    # Обновляем рейтинговые очки отправителя
    sender.rating_points += int(amount / 10)

    # Создаем запись о переводе
    new_transfer = Transfer(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=amount,
        commission=commission,
    )
    session.add(new_transfer)
    await session.commit()

    await message.answer(
        f"Вы успешно передали {amount} поинтов пользователю {receiver.telegram_id}. Комиссия: {commission} поинтов."
    )
    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_transfer, Command(commands=["transfer"]))
    dp.message.register(process_receiver)
    dp.message.register(process_amount)
