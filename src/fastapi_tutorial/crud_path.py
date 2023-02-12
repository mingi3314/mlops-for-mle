from fastapi import FastAPI, HTTPException

app = FastAPI()

FAKE_USER_DB = {}


@app.post("/users/name/{name}/nickname/{nickname}")
async def create_user(name: str, nickname: str) -> dict[str, str]:
    if name in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name already exists")

    FAKE_USER_DB.update({name: nickname})
    return {"status": "success"}


@app.get("/users/user/{name}")
async def read_user(name: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name not found")

    return {"nickname": FAKE_USER_DB[name]}


@app.put("/users/name/{name}/nickname/{nickname}")
async def update_user(name: str, nickname: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name not found")

    FAKE_USER_DB.update({name: nickname})
    return {"status": "success"}


@app.delete("/users/user/{name}")
async def delete_user(name: str) -> dict[str, str]:
    if name not in FAKE_USER_DB:
        raise HTTPException(status_code=400, detail="Name not found")

    FAKE_USER_DB.pop(name)
    return {"status": "success"}
