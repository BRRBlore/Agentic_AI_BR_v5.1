# agents/parts_dispatch_agent.py

import re
from tools.dispatch_api import track_delivery
from tools.gpt_fallback import get_fallback_response  # ✅ GPT fallback
from langchain.memory.chat_memory import BaseChatMemory

def extract_delivery_id(text):
    """ Extracts delivery ID using regex pattern """
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'  # e.g., VCV00014744/082021
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory=None) -> str:
    # Step 1: Try to extract delivery ID from query
    delivery_id = extract_delivery_id(query)

    # Step 2: Try memory if not found
    if not delivery_id and isinstance(memory, BaseChatMemory):
        for msg in reversed(memory.chat_memory.messages):
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    # Step 3: If no ID, fallback
    if not delivery_id:
        fallback = get_fallback_response(query)
        return f"❌ Please provide a valid delivery ID.\n\n{fallback}"

    # Step 4: Try to get delivery status
    response = track_delivery(delivery_id)

    # Step 5: If not found, fallback
    if "not found" in response.lower():
        fallback = get_fallback_response(query)
        return f"{response}\n\n{fallback}"

    # Step 6: Save to memory
    if memory:
        memory.save_context({"input": query}, {"output": response})

    return response
