from poc import calculate_next_step, calculate_current_step
from fastapi import FastAPI
from typing import Union

app = FastAPI()


@app.get("/")
async def get_next_step():
    """Calculate next step for user"""
    print("Rubicon: Root Request")
    summary_steps = await calculate_current_step()
    return summary_steps


@app.get("/{index}")
async def get_next_flow(index: Union[None, int]):
    """Calculate next flow for user"""
    summary_steps = await calculate_next_step(index)
    return summary_steps
