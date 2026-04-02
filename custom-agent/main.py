from agent import run_agent

while True:
    query = input("\nUser: ")
    
    if query.lower() in ["exit", "quit"]:
        break

    response = run_agent(query)
    print("Bot:", response)