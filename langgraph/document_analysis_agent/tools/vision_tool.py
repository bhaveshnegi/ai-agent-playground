import base64
from langchain_core.messages import HumanMessage
from models.llm import llm


def extract_text(img_path: str) -> str:

    with open(img_path, "rb") as image_file:
        image_bytes = image_file.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    message = [
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "Extract all text from this image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    },
                },
            ]
        )
    ]

    response = llm.invoke(message)

    return response.content