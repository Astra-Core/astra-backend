from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")    