from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rarity = Column(String, default="common")
    base_hp = Column(Integer, default=10)
    base_attack = Column(Integer, default=5)
    base_defense = Column(Integer, default=5)
    created_at = Column(DateTime, server_default=func.now())

class UserMonster(Base):
    __tablename__ = "user_monsters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    monster_id = Column(Integer, ForeignKey("monsters.id"), nullable=False)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    obtained_at = Column(DateTime, server_default=func.now())
