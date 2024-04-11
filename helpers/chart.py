from graphviz import Digraph
import commentjson

FILENAME = "../rubicon.jsonc"

flow_json = commentjson.load(open(FILENAME, encoding="utf-8"))


def create_flow_diagram(flow_json):
    dot = Digraph(
        engine="dot",
        comment="App Flow",
        graph_attr={
            "bgcolor": "#2D2D2D",
            "fontcolor": "white",
            "dpi": "100",
        },
        node_attr={
            "style": "filled",
            "color": "white",
            "fontcolor": "white",
            "fontsize": "12",
        },
        edge_attr={
            "color": "#848484",
            "fontcolor": "white",
        },
    )
    environment_colors = {"dap": "#117A65", "native": "#1B4F72"}
    special_nodes = {
        0: "#FF5733",
        -1: "#C70039",
        -9999: "#900C3F",
    }
    for step in flow_json:
        fillcolor = environment_colors.get(step["environment"], "#566573")
        if step["index"] == -9999:
            dot.node(
                str(step["index"]),
                f'{step["name"]} ({step["index"]})',
                fillcolor=special_nodes[step["index"]],
                fontcolor="white",
            )
        elif step["index"] == -1:
            dot.node(
                str(step["index"]),
                step["name"],
                shape="house",
                fillcolor=special_nodes[step["index"]],
                fontcolor="white",
            )
        else:
            dot.node(
                str(step["index"]),
                f'{step["name"]} ({step["index"]})',
                fillcolor=fillcolor,
            )
        for branch in step["branches"]:
            target_node_name = str(branch["output"])
            if branch["output"] == -9999:
                target_node_name = "Error/End"
                dot.node(
                    target_node_name,
                    "Error/End",
                    shape="doublecircle",
                    fillcolor=special_nodes[branch["output"]],
                    fontcolor="white",
                )
            elif branch["output"] == -1:
                target_node_name = str(branch["output"])

            dot.edge(str(step["index"]), target_node_name, label=branch.get("rule", ""))
    return dot


diagram = create_flow_diagram(flow_json)
diagram.render("../app_flow_diagram", format="png", cleanup=True)
