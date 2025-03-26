from tools.order_db import lookup_order
from tools.gpt_fallback import gpt_fallback_response  # ✅ Correct fallback import

def handle(query: str, memory=None) -> str:
    words = query.split()
    order_id = None
    for word in words:
        if len(word) >= 6 and any(char.isdigit() for char in word):
            order_id = word
            break

    if not order_id and memory:
        history = memory.chat_memory.messages[::-1]
        for msg in history:
            if msg.type == "human" and "order id" in msg.content.lower():
                for word in msg.content.split():
                    if len(word) >= 6 and any(char.isdigit() for char in word):
                        order_id = word
                        break
            if order_id:
                break

    if not order_id:
        return gpt_fallback_response(query)

    response = lookup_order(order_id)
    if "not found" in response.lower():
        return gpt_fallback_response(query)
    return response
