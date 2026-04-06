from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "OpenEnv running"}

# Reset endpoint (NO body required)
@app.api_route("/reset", methods=["GET", "POST"])
def reset():
    return {
        "observation": [0, 0, 0, 0],
        "info": {}
    }

# Step endpoint (no strict schema)
@app.api_route("/step", methods=["GET", "POST"])
async def step(request: Request):
    return {
        "observation": [1, 2, 3, 4],
        "reward": 1.0,
        "terminated": False,
        "truncated": False,
        "info": {}
    }