from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models import Monster

router = APIRouter()

# Pydanticスキーマ
class MonsterCreate(BaseModel):
    name: str
    rarity: Optional[str] = "common"
    base_hp: Optional[int] = 10
    base_attack: Optional[int] = 5
    base_defense: Optional[int] = 5

class MonsterRead(BaseModel):
    id: int
    name: str
    rarity: str
    base_hp: int
    base_attack: int
    base_defense: int

    class Config:
        orm_mode = True

# CREATE (モンスター種の登録)
@router.post("/", response_model=MonsterRead)
def create_monster(monster_data: MonsterCreate, db: Session = Depends(get_db)):
    new_monster = Monster(
        name=monster_data.name,
        rarity=monster_data.rarity,
        base_hp=monster_data.base_hp,
        base_attack=monster_data.base_attack,
        base_defense=monster_data.base_defense,
    )
    db.add(new_monster)
    db.commit()
    db.refresh(new_monster)
    return new_monster

# READ (全モンスター種の一覧取得)
@router.get("/", response_model=list[MonsterRead])
def get_all_monsters(db: Session = Depends(get_db)):
    monsters = db.query(Monster).all()
    return monsters

# READ by ID
@router.get("/{monster_id}", response_model=MonsterRead)
def get_monster_by_id(monster_id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == monster_id).first()
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    return monster

# DELETE
@router.delete("/{monster_id}")
def delete_monster(monster_id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == monster_id).first()
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    db.delete(monster)
    db.commit()
    return {"detail": "Monster deleted"}
