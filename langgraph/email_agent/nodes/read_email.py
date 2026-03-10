from state.email_state import EmailState

def read_email(state: EmailState):

    email = state["email"]

    print("\n📨 Reading Email")
    print(f"From: {email['sender']}")
    print(f"Subject: {email['subject']}")

    return {}