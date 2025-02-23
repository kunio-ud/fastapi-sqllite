import random
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Monster, UserMonster
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# レア度ごとの確率 (例)
RARITY_PROB = {
    "common": 0.7,
    "rare": 0.25,
    "legendary": 0.05
}

class GachaResult(BaseModel):
    user_id: int
    monster_id: int
    monster_name: str
    monster_rarity: str
    message: str

@router.post("/", response_model=GachaResult)
def pull_gacha(
    user_id: int = Query(..., description="ガチャを引くユーザーID"),
    db: Session = Depends(get_db)
):
    """
    ユーザーがガチャを引いて、ランダムにモンスターを入手するエンドポイント。
    """

    # 1. ユーザーの存在確認
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. レア度を抽選 (random.choicesで確率的に選択)
    rarities = list(RARITY_PROB.keys())   # ["common", "rare", "legendary"]
    probs = list(RARITY_PROB.values())   # [0.7, 0.25, 0.05]
    chosen_rarity = random.choices(rarities, probs)[0]

    # 3. 選ばれたレア度に該当するモンスター一覧を取得
    monsters = db.query(Monster).filter(Monster.rarity == chosen_rarity).all()
    if not monsters:
        raise HTTPException(status_code=500, detail="No monsters found for this rarity")

    # 4. 一覧の中からランダムで1体ピック
    chosen_monster = random.choice(monsters)

    # 5. user_monstersに所有記録を追加
    new_owned = UserMonster(
        user_id=user_id,
        monster_id=chosen_monster.id,
        level=1,
        exp=0
    )
    db.add(new_owned)
    db.commit()
    db.refresh(new_owned)

    # 6. 結果を返却
    return GachaResult(
        user_id=user_id,
        monster_id=chosen_monster.id,
        monster_name=chosen_monster.name,
        monster_rarity=chosen_monster.rarity,
        message=f"You got a {chosen_monster.name}!"
    )
