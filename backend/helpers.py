from types import SimpleNamespace
import commentjson
import httpx

bff = "http://127.0.0.1:8002/"


def load_json(filename=None):
    if not filename:
        filename = "../rubicon.jsonc"
    return commentjson.load(open(filename, encoding="utf-8"))


async def request_user_data():
    print("Rubicon: Request user data")
    async with httpx.AsyncClient() as client:
        response = await client.get(bff + "data")
        r = response.json()
    return r


class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)
