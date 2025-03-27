from tools.order_db import lookup_order
from langchain.memory.chat_memory import BaseChatMemory
from agents.session_knowledge import extract_and_store_facts, check_session_knowledge
from tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory: BaseChatMemory = None) -> str:
    # Phase 2: Check existing session knowledge
    session_answer = check_session_knowledge(query)
    if session_answer:
        return f"🧠 {session_answer}"

    # Extract order ID from query or memory
    words = query.split()
    order_id = next((w for w in words if len(w) >= 6 and any(c.isdigit() for c in w)), None)

    if not order_id and memory:
        history = memory.chat_memory.messages[::-1]
        for msg in history:
            if msg.type == "human" and "order" in msg.content.lower():
                order_id = next((w for w in msg.content.split() if len(w) >= 6 and any(c.isdigit() for c in w)), None)
                if order_id:
                    break

    if not order_id:
        return gpt_fallback_response(query)

    response = lookup_order(order_id)

    # Phase 1: Extract and store facts
    extract_and_store_facts(query, response)

    # Save memory context
    if memory:
        memory.save_context({"input": query}, {"output": response})

    return response
