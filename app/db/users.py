from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String, DateTime
import uuid
from datetime import datetime
import os

from app.utils.jwt import get_password_hash
from .base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    old_password = Column(String)
    password_salt = Column(String(32))  # Store salt as hex

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)

    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.now())
    account_created = Column(DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        self.password_salt = os.urandom(16).hex()
        super(User, self).__init__(**kwargs)
        # Hash the plain password with salt
        self.hashed_password = get_password_hash(kwargs.get('hashed_password'), self.password_salt)

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")    
    

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID, ForeignKey("roles.id"), primary_key=True)

