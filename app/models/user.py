from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String(50), unique=True, nullable=False)
    balance = Column(Integer, default=100)  # Баланс поинтов
    rating_points = Column(Integer, default=100)  # Рейтинговые очки
    global_rank = Column(Integer, default=0)  # Место в рейтинге
    referrer_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )  # Кто пригласил
    is_premium = Column(Boolean, default=False)  # Премиум статус
    last_daily_reward = Column(
        DateTime, default=datetime.datetime.utcnow
    )  # Последняя награда

    referrals = relationship(
        "Referral", back_populates="referrer", foreign_keys="Referral.referrer_id"
    )
    referees = relationship(
        "Referral", back_populates="referee", foreign_keys="Referral.referee_id"
    )
