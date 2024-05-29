from database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String, nullable=True)
    fullName = Column(String)
    email = Column(String)
    hashedPassword = Column(String)
    DoB = Column(String, nullable=True)
    gender = Column(String)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)



class Listing(Base):
    __tablename__ = 'Listing'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    availableNow = Column(Boolean, nullable=True, default=True)
    ownerId = Column(Integer, ForeignKey('User.id'))
    address = Column(String)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)




