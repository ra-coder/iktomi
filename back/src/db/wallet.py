from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.connect import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, nullable=False)
    is_confirmed = Column(Boolean, nullable=False, server_default="False")
