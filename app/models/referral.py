from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Кто пригласил
    referree_id = Column(
        Integer, ForeignKey("user.id"), nullable=False
    )  # Кого пригласили
    level = Column(Integer, default=1)  # Уровень реферала

    referrer = relationship(
        "User", back_populates="referrals", foreign_keys=[referrer_id]
    )
    referee = relationship(
        "User", back_populates="referees", foreign_keys=[referree_id]
    )
