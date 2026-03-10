from state.email_state import EmailState
from models.llm import llm


def classify_email(state: EmailState):

    email = state["email"]

    prompt = f"""
Classify the following email.

Email:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}

Respond with ONLY one word:

SPAM
or
LEGITIMATE
"""

    response = llm.invoke(prompt)

    text = response.content.strip().lower()

    print("MODEL OUTPUT:", text)

    is_spam = text == "spam"

    return {
        "is_spam": is_spam,
        "email_category": None
    }