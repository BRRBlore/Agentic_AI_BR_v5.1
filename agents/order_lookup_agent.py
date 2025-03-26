# agents/order_lookup_agent.py

from tools.order_db import lookup_order

def handle(query: str, memory=None) -> str:
    # Try to extract order ID from the current query
    words = query.split()
    order_id = None
    for word in words:
        if len(word) >= 6 and any(char.isdigit() for char in word):
            order_id = word
            break

    # If not found, fallback to memory (last known Order ID)
    if not order_id and memory:
        history = memory.chat_memory.messages[::-1]  # Reverse chronological
        for msg in history:
            if msg.type == "human" and "order id" in msg.content.lower():
                # Try to extract from previous message
                for word in msg.content.split():
                    if len(word) >= 6 and any(char.isdigit() for char in word):
                        order_id = word
                        break
            if order_id:
                break

    if not order_id:
        return "❌ Please provide a valid order ID."

    return lookup_order(order_id)
