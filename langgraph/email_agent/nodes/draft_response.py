from state.email_state import EmailState
from models.llm import llm


def extract_name(email_address: str):
    """
    Extract name from email like john.smith@example.com -> John Smith
    """
    name_part = email_address.split("@")[0]
    name_part = name_part.replace(".", " ").replace("_", " ")
    return name_part.title()


def draft_response(state: EmailState):

    email = state["email"]

    sender_email = email["sender"]

    recipient_name = extract_name(sender_email)

    prompt = f"""
Write a polite professional reply to this email.

Recipient Name: {recipient_name}

Email Body:
{email['body']}

Rules:
- Start with "Dear {recipient_name},"
- Keep the response professional As you are replying as an Organization person to a Job Application, Client Query or any other email.
- End with this exact signature:

Best regards,
Bhavesh Negi
9313198316
https://portfolio-main-tau-lime.vercel.app/
"""

    response = llm.invoke(prompt)

    return {
        "email_draft": response.content
    }