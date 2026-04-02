from prompt import INTENT_PROMPT
from llm import call_llm

def detect_intent(query):
    prompt = INTENT_PROMPT.format(query=query)
    intent = call_llm(prompt)
    return intent.strip().lower()


if __name__ == "__main__":
    print(detect_intent("Where is my order 101?"))
    print(detect_intent("Cancel my order"))
    print(detect_intent("What is your return policy?"))