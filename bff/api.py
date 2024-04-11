import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from persistency import process_action, read_data, reset_data

rubicon = "http://127.0.0.1:8000/"
dap = "http://127.0.0.1:8001/"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    rubicon,
    dap,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    print("BFF: Root Request")
    async with httpx.AsyncClient() as client:
        r = await client.get(rubicon)
        r = r.json()
    if r["current_step"]["finished"]:
        step = r["next_step"]
    else:
        step = r["current_step"]
    name = step["name"]
    process = step["process"]
    index = step["index"]
    async with httpx.AsyncClient() as client:
        content = await client.get(dap + process)
        content = content.json()
    return {
        "id": f"flow{index}",
        "name": name,
        "process": process,
        "content": content,
    }


@app.get("/data")
async def get_data():
    """Get current user data"""
    print("BFF: Get Data")
    return read_data()


@app.post("/action")
async def post_user_action(action: dict):
    """Store new user action"""
    return process_action(action)


@app.post("/reset")
async def post_reset_data():
    """Reset user actions"""
    return reset_data()
