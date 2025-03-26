# agents/order_lookup_agent.py

from tools.order_db import lookup_order
from tools.gpt_fallback import get_fallback_response  # ✅ Import fallback
from langchain.memory.chat_memory import BaseChatMemory

def handle(query: str, memory=None) -> str:
    # Step 1: Try to extract order ID from the query
    words = query.split()
    order_id = None
    for word in words:
        if len(word) >= 6 and any(char.isdigit() for char in word):
            order_id = word
            break

    # Step 2: Try memory fallback if not found
    if not order_id and isinstance(memory, BaseChatMemory):
        for msg in reversed(memory.chat_memory.messages):
            if msg.type == "human" and "order" in msg.content.lower():
                for word in msg.content.split():
                    if len(word) >= 6 and any(char.isdigit() for char in word):
                        order_id = word
                        break
            if order_id:
                break

    # Step 3: Respond accordingly
    if not order_id:
        fallback = get_fallback_response(query)
        return f"❌ Couldn't extract an Order ID.\n\n{fallback}"

    response = lookup_order(order_id)

    # Step 4: If response is not useful, fallback to GPT
    if "not found" in response.lower():
        fallback = get_fallback_response(query)
        return f"{response}\n\n{fallback}"

    return response
