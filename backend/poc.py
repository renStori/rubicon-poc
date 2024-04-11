import rule_engine
from helpers import load_json, request_user_data

flow = load_json(filename="../flow-to-demo.jsonc")


def get_step(index):
    print("Rubicon: Get Step")
    return [step for step in flow if step["index"] == index][0]


async def calculate_next_step(index=None):
    print(f"Rubicon: Calculate Next Step for index {index}")
    current_step, current_step_response = None, None
    next_step, next_step_response = None, None
    if index is None:
        next_step = get_step(0)
    else:
        current_step = get_step(index)
        current_step_response = {
            "index": current_step["index"],
            "name": current_step["name"],
            "process": current_step["process"],
            "environment": current_step["environment"],
            "finished": False,
        }
        branches = current_step["branches"]
        rules = [rule_engine.Rule(branch["rule"]) for branch in branches]
        data = await request_user_data()
        for r, rule in enumerate(rules):
            try:
                if rule.matches(data):
                    output = branches[r]["output"]
                    next_step = get_step(output)
                    current_step_response["finished"] = True
            except:
                pass
    if next_step:
        next_step_response = {
            "index": next_step["index"],
            "name": next_step["name"],
            "process": next_step["process"],
            "environment": next_step["environment"],
        }
    return {
        "current_step": current_step_response,
        "next_step": next_step_response,
    }


async def calculate_current_step():
    current_step = None
    print("Rubicon: Calculate Current Step")
    start = flow[0]
    step = await calculate_next_step(start["index"])
    if not step["current_step"]["finished"]:
        current_step = step
    else:
        found = False
        last_index = step["next_step"]["index"]
        while not found:
            step_ = await calculate_next_step(last_index)
            current_, next_ = step_["current_step"], step_["next_step"]
            if current_["finished"]:
                last_index = next_["index"]
            if not current_["finished"]:
                current_step = step_
                found = True
        print(current_step)
    return current_step
