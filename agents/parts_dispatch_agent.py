# agents/parts_dispatch_agent.py

import re
from tools.dispatch_api import track_delivery
from langchain.memory.chat_memory import BaseChatMemory

# ✅ Helper to extract delivery ID
def extract_delivery_id(text: str) -> str:
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'  # Matches format like VCV00014744/082021
    match = re.search(pattern, text)
    return match.group(0) if match else None

# ✅ Main handler
def handle(query: str, memory=None) -> str:
    delivery_id = extract_delivery_id(query)

    # ✅ Fallback to memory if no delivery ID in query
    if not delivery_id and isinstance(memory, BaseChatMemory):
        for msg in memory.chat_memory.messages[::-1]:  # Reverse chronological
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    print(f"🔎 DEBUG: Looking for delivery ID -> {delivery_id}")

    # ✅ If still not found
    if not delivery_id:
        response = "❌ Please provide a valid delivery ID."
    else:
        response = track_delivery(delivery_id)

    # ✅ Save context if memory is active
    if isinstance(memory, BaseChatMemory):
        memory.save_context({"input": query}, {"output": response})

    return response
