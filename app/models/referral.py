from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )  # Кто пригласил
    referee_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )  # Кого пригласили
    level = Column(Integer, default=1)  # Уровень реферала

    referrer = relationship(
        "User", back_populates="referrals", foreign_keys=[referrer_id]
    )
    referee = relationship("User", back_populates="referees", foreign_keys=[referee_id])
