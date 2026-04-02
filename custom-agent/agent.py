from llm import call_llm
from prompt import INTENT_PROMPT
from tools import track_order, cancel_order, return_policy
from memory import Memory

import re

memory = Memory()

def extract_order_id(query):
    match = re.search(r'\d+', query)
    return match.group() if match else None

VALID_TOOLS = ["track_order", "cancel_order", "return_policy"]

def validate_decision(decision):
    if not isinstance(decision, dict):
        return False

    tool = decision.get("tool")
    args = decision.get("arguments")

    if tool not in VALID_TOOLS:
        return False

    if not isinstance(args, dict):
        return False

    return True

def fallback_decision(query):
    query = query.lower()

    if "cancel" in query:
        return {"tool": "cancel_order", "arguments": {}}

    elif "return" in query:
        return {"tool": "return_policy", "arguments": {}}

    else:
        return {"tool": "track_order", "arguments": {}}

def run_agent(query):
    prompt = INTENT_PROMPT.format(
        query=query,
        last_order_id=memory.get("last_order_id")
    )

    decision = call_llm(prompt)

    print("🔍 RAW DECISION:", decision)

    # ✅ VALIDATE FIRST
    if not validate_decision(decision):
        print("⚠️ Invalid LLM output, applying fallback...")
        decision = fallback_decision(query)

    print("🧠 FINAL DECISION:", decision)

    tool = decision.get("tool")
    args = decision.get("arguments", {})

    try:
        if tool == "track_order":
            order_id = args.get("order_id") or extract_order_id(query)

            if not order_id:
                order_id = memory.get("last_order_id")

            if not order_id:
                return "Please provide an order ID."

            memory.set("last_order_id", order_id)
            return track_order(order_id)

        elif tool == "cancel_order":
            order_id = args.get("order_id") or extract_order_id(query)

            if not order_id:
                order_id = memory.get("last_order_id")

            if not order_id:
                return "Please provide an order ID."

            memory.set("last_order_id", order_id)
            return cancel_order(order_id)

        elif tool == "return_policy":
            return return_policy()

        else:
            return f"Invalid tool: {tool}"

    except Exception as e:
        return f"Execution error: {str(e)}"