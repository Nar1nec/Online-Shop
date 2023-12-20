from datetime import datetime

from sqlalchemy.orm import DeclarativeMeta, declarative_base, relationship

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, TIMESTAMP, Column, Boolean

from db import Base

# Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    registered_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    cart = relationship("Cart", uselist=False, back_populates="user",lazy='selectin')
