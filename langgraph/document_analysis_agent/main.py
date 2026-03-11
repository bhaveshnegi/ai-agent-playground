from langchain_core.messages import HumanMessage
from graph.workflow import build_graph


def main():

    app = build_graph()

    messages = [
        HumanMessage(content="Divide 6790 by 5")
    ]

    result = app.invoke({
        "messages": messages,
        "input_file": None
    })

    for m in result["messages"]:
        m.pretty_print()


if __name__ == "__main__":
    main()