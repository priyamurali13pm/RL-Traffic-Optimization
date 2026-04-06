from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Action(BaseModel):
    action: int

# Support BOTH GET and POST
@app.api_route("/reset", methods=["GET", "POST"])
def reset():
    return {
        "observation": [0, 0, 0, 0],
        "info": {}
    }

# Support BOTH GET and POST
@app.api_route("/step", methods=["GET", "POST"])
def step(action: Action = None):
    return {
        "observation": [1, 2, 3, 4],
        "reward": 1.0,
        "terminated": False,
        "truncated": False,
        "info": {}
    }