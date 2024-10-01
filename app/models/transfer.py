from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Кто отправил
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Кто получил
    amount = Column(Integer, nullable=False)  # Сколько отправлено
    comission = Column(Float, nullable=False)  # Комиссия
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Время транзакции

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
