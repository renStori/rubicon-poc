import pickle
from get_offer import generate_offer

filename = "user_data.pkl"


def reset_data():
    data = {
        "in_progress": False,
        "answers": {},
        "response": {},
        "offer": generate_offer(),
        "common": {
            "credit_card_products": ["green", "black", "shein"],
            "loan_products": ["luna"],
        },
    }
    write_data(data)
    return data


def write_data(data):
    serialized = pickle.dumps(data)
    with open(filename, "wb") as file_object:
        file_object.write(serialized)


def read_data():
    print("BFF: Read Data")
    try:
        with open(filename, "rb") as file_object:
            raw_data = file_object.read()
            if len(raw_data):
                data = pickle.loads(raw_data)
    except:
        data = reset_data()
    return data


def process_action(action):
    data = read_data()
    if not data["in_progress"]:
        data["in_progress"] = True
    for key in action.keys():
        data[key] = {**data[key], **action[key]}
    write_data(data)
    return data
