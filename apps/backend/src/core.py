import os
import shared
from fastapi import FastAPI
from shared import hello
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

# If a FRONTEND_ORIGIN environment variable is set, add it to the list of allowed origins
frontend_origin = os.getenv("FRONTEND_ORIGIN")
if frontend_origin:
    origins.append(frontend_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_shared_is_compiled = shared.__file__ is not None and not shared.__file__.endswith(
    ".py"
)


@app.get("/")
def read_root():
    return {"message": hello()}


@app.get("/debug/shared")
def debug_shared():
    return {
        "file": shared.__file__,
        "compiled": _shared_is_compiled,
    }


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

class Hobby(BaseModel):
    name: str
    id: str


class CreateHobbyBody(BaseModel):
    new_hobbies: list[Hobby]


class CreateHobbyResponse(BaseModel):
    hobbies: list[Hobby]


@app.post("/{person_id}/hobbies")
def create_hobbies(person_id: str, body: CreateHobbyBody) -> CreateHobbyResponse:
    new_hobbies = body.new_hobbies
    # In a real app, you would save the new hobbies to a database here
    return {"hobbies": new_hobbies}
