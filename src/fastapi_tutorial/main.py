from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: int | None = None) -> dict[str, int | None]:
    return {"item_id": item_id, "q": q}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None
) -> dict[str, int | str | None]:
    return {"user_id": user_id, "item_id": item_id, "q": q}
