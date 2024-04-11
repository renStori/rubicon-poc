import commentjson

"""WIP. This needs to get better parsing of composite rules"""


def generate_ui_mockups(item):
    ui_elements = []
    if "branches" in item:
        for branch in item["branches"]:
            source, ui_id, context = branch["rule"].split(".")
            value = branch["rule"].split("'")[1]
            text = value.capitalize()
            ui_element = {
                "id": ui_id,
                "source": source,
                "context": context,
                "type": "button",
                "text": text,
                "value": value,
            }
            ui_elements.append(ui_element)
    return ui_elements


filename = "../flow-to-demo.jsonc"
flow = commentjson.load(open(filename, encoding="utf-8"))


for node in flow:
    ui_mockup = generate_ui_mockups(node)
    file_name = f"screens/{node['process']}.json"
    with open(file_name, "w") as file:
        commentjson.dump(ui_mockup, file, indent=2)
