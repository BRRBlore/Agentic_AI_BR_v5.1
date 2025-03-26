# agents/parts_dispatch_agent.py

import re
from tools.dispatch_api import track_delivery
from tools.gpt_fallback import gpt_fallback_response
from langchain.memory.chat_memory import BaseChatMemory

def extract_delivery_id(text: str) -> str:
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory=None) -> str:
    delivery_id = extract_delivery_id(query)

    # Fallback to memory if delivery ID not found in current query
    if not delivery_id and isinstance(memory, BaseChatMemory):
        for msg in reversed(memory.chat_memory.messages):
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    if delivery_id:
        response = track_delivery(delivery_id)
    else:
        response = gpt_fallback_response(query)

    # Save context to memory
    if memory:
        memory.save_context({"input": query}, {"output": response})

    return f"📦 {response}"
