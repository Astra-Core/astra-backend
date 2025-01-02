from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    roles = relationship("Role", secondary="user_roles", back_populates="users")