from fastapi import FastAPI, Request

app = FastAPI()

# Root (important for health check)
@app.get("/")
def root():
    return {"status": "ok"}

# RESET endpoint (must accept ANYTHING)
@app.post("/reset")
async def reset(request: Request):
    return {
        "observation": [0, 0, 0, 0],
        "info": {}
    }

# ALSO support GET (backup)
@app.get("/reset")
def reset_get():
    return {
        "observation": [0, 0, 0, 0],
        "info": {}
    }

# STEP endpoint
@app.post("/step")
async def step(request: Request):
    return {
        "observation": [1, 2, 3, 4],
        "reward": 1.0,
        "terminated": False,
        "truncated": False,
        "info": {}
    }

# ALSO support GET
@app.get("/step")
def step_get():
    return {
        "observation": [1, 2, 3, 4],
        "reward": 1.0,
        "terminated": False,
        "truncated": False,
        "info": {}
    }