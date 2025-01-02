from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String, DateTime
import uuid
from datetime import datetime

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    old_password = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)

    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.now())
    
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")    
    

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID, ForeignKey("roles.id"), primary_key=True)

