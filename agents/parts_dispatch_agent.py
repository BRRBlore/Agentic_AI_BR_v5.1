import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.dispatch_api import track_delivery
from tools.gpt_fallback import gpt_fallback_response
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge

def extract_delivery_id(text):
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory=None) -> str:
    delivery_id = extract_delivery_id(query)

    if not delivery_id and memory:
        past_messages = memory.chat_memory.messages[::-1]
        for msg in past_messages:
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    if not delivery_id:
        return gpt_fallback_response(query)

    response = track_delivery(delivery_id)

    if memory:
        memory.save_context({"input": query}, {"output": response})
        extract_and_store_facts(query, response, memory)

    return response
