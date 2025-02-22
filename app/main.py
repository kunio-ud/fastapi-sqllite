from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import monsters, users

app = FastAPI()

# ルーターの登録
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(monsters.router, prefix="/monsters", tags=["monsters"])

# テーブルが存在しない場合は自動作成
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Monster Game API"}