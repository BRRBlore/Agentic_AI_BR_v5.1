from tools.dispatch_api import track_delivery
from tools.gpt_fallback import gpt_fallback  # ✅ Fallback import
import re

def extract_delivery_id(text):
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory=None) -> str:
    try:
        delivery_id = extract_delivery_id(query)

        if not delivery_id and memory:
            past_messages = memory.chat_memory.messages[::-1]
            for msg in past_messages:
                if msg.type == "human":
                    delivery_id = extract_delivery_id(msg.content)
                    if delivery_id:
                        break

        if not delivery_id:
            return "❌ Please provide a valid delivery ID."

        response = track_delivery(delivery_id)

        if memory is not None:
            memory.save_context({"input": query}, {"output": response})

        return response

    except Exception:
        return gpt_fallback(query)
