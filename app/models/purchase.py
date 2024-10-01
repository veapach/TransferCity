from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Кто купил
    amount = Column(Integer, nullable=False)  # Сколько поинтов куплено
    currency_type = Column(
        String(20), nullable=False
    )  # Тип валюты ('points', 'rating_points', 'premium')
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Время покупки

    user = relationship("User")
