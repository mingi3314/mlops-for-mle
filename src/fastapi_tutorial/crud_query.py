from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    nickname: str


FAKE_USER_DB = {}


@app.post("/users")
async def create_user(user: User) -> dict[str, str]:
    if user.name in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name already exists")

    FAKE_USER_DB.update({user.name: user.nickname})
    return {"status": "success"}


@app.get("/users")
async def read_user(name: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name not found")

    return {"nickname": FAKE_USER_DB[name]}


@app.put("/users")
async def update_user(user: User) -> dict[str, str]:
    if user.name not in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name not found")

    FAKE_USER_DB.update({user.name: user.nickname})
    return {"status": "success"}


@app.delete("/users")
async def delete_user(name: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name not found")

    FAKE_USER_DB.pop(name)
    return {"status": "success"}
