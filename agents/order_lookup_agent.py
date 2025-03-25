# agents/order_lookup_agent.py

from tools.order_db import lookup_order

def handle(query: str) -> str:
    # Extract order ID from query
    words = query.split()
    order_id = None
    for word in words:
        if len(word) >= 6 and any(char.isdigit() for char in word):
            order_id = word
            break

    if not order_id:
        return "❌ Please provide a valid order ID."

    return lookup_order(order_id)
