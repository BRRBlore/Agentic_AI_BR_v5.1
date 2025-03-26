# agents/order_lookup_agent.py

from tools.order_db import lookup_order
from tools.gpt_fallback import gpt_fallback_response

def extract_order_id(text: str) -> str:
    words = text.split()
    for word in words:
        if len(word) >= 6 and any(char.isdigit() for char in word):
            return word
    return None

def handle(query: str, memory=None) -> str:
    order_id = extract_order_id(query)

    # 🔁 Search memory if order ID not found in current query
    if not order_id and memory:
        for msg in reversed(memory.chat_memory.messages):
            if msg.type == "human" and "order" in msg.content.lower():
                possible_id = extract_order_id(msg.content)
                if possible_id:
                    order_id = possible_id
                    break

    # 🧠 If still no ID, fallback to GPT
    if not order_id:
        response = gpt_fallback_response(query)
    else:
        response = lookup_order(order_id)

    # 💾 Save to memory
    if memory:
        memory.save_context({"input": query}, {"output": response})

    return response
