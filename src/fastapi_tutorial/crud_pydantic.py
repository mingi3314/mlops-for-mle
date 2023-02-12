from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

FAKE_USER_DB = {}

NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not found")


class CreateIn(BaseModel):
    name: str
    nickname: str


class CreateOut(BaseModel):
    status: str
    id: int


@app.post("/users", response_model=CreateOut)
async def create_user(user: CreateIn) -> CreateOut:
    if user.name in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name already exists")

    FAKE_USER_DB.update({user.name: user.nickname})
    return CreateOut(status="success", id=len(FAKE_USER_DB))


@app.get("/users")
async def read_user(name: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise NAME_NOT_FOUND

    return {"nickname": FAKE_USER_DB[name]}


@app.put("/users")
async def update_user(name: str, nickname: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise NAME_NOT_FOUND

    FAKE_USER_DB.update({name: nickname})
    return {"status": "success"}


@app.delete("/users")
async def delete_user(name: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise NAME_NOT_FOUND

    FAKE_USER_DB.pop(name)
    return {"status": "success"}
