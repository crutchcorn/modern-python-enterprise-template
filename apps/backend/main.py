import logging

import shared
from fastapi import FastAPI
from shared import hello

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

_shared_is_compiled = shared.__file__ is not None and not shared.__file__.endswith(".py")
logger.info("shared module loaded from: %s (compiled=%s)", shared.__file__, _shared_is_compiled)


@app.get("/")
def read_root():
    return {"message": hello()}


@app.get("/debug/shared")
def debug_shared():
    return {
        "file": shared.__file__,
        "compiled": _shared_is_compiled,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}