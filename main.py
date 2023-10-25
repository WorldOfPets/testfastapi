from typing import List
from fastapi import FastAPI
from schemas import Trade, User
from testdata import *
from exec import CustomExec

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)
CustomExec(app)



@app.get("/users/{user_id}", response_model=List[User])
def hello(user_id: int):
    # u_array = []
    # for user in fake_users:
    #     if user_id == user.get("role"):
    #         u_array.append(user)
    # return u_array
    return [user for user in fake_users if user_id == user.get("id")]

@app.get("/trades", response_model=Trade)
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]

@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data":current_user}

@app.post("/trades")
def add_trades(trades: Trade):
    fake_trades.append(trades)
    return {"status":200, "data":fake_trades}