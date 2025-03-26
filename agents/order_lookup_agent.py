# agents/order_lookup_agent.py

from tools.order_db import lookup_order
from langchain.memory.chat_memory import BaseChatMemory

# No caching needed for this agent, since lookup is fast

def handle(query: str, memory=None) -> str:
    order_id = extract_order_id_from_query(query)

    # ✅ Fallback to memory if not found in current query
    if not order_id and isinstance(memory, BaseChatMemory):
        history = memory.chat_memory.messages[::-1]  # Reverse chronological
        for msg in history:
            if msg.type == "human" and "order" in msg.content.lower():
                order_id = extract_order_id_from_query(msg.content)
                if order_id:
                    break

    if not order_id:
        return "❌ Please provide a valid order ID."

    return lookup_order(order_id)

# ✅ Helper function for extracting order ID
def extract_order_id_from_query(text: str) -> str:
    for word in text.split():
        if len(word) >= 6 and any(char.isdigit() for char in word):
            return word
    return None
