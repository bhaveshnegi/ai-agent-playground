from state.email_state import EmailState

def notify_user(state: EmailState):

    print("\n📩 Draft Reply Generated:\n")

    print(state["email_draft"])

    return {}