from state.email_state import EmailState

def route_email(state: EmailState):

    if state["is_spam"]:
        return "spam"

    return "legit"