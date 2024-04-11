import json
from fastapi import FastAPI

app = FastAPI()

path = "screens"


@app.get("/{process_id}")
async def get_data(process_id):
    """Get specific process"""
    filename = f"{path}/{process_id}.json"
    content = json.load(open(filename, encoding="utf-8"))
    return content
