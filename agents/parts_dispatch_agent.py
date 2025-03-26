# agents/parts_dispatch_agent.py

from tools.dispatch_api import track_delivery
import re

def extract_delivery_id(text):
    """ Extracts delivery ID using regex pattern """
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'  # Matches format like VCV00014744/082021
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory=None) -> str:
    # Step 1: Try to extract delivery ID from the current query
    delivery_id = extract_delivery_id(query)

    # Step 2: If not found, search memory
    if not delivery_id and memory:
        past_messages = memory.chat_memory.messages[::-1]  # Most recent first
        for msg in past_messages:
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    # Step 3: Log what we're trying to find
    print(f"🔎 DEBUG: Looking for delivery ID -> {delivery_id}")

    # Step 4: Respond appropriately
    if not delivery_id:
        response = "❌ Please provide a valid delivery ID."
    else:
        response = track_delivery(delivery_id)

    # Step 5: Save context
    if memory is not None:
        memory.save_context({"input": query}, {"output": response})

    return response
