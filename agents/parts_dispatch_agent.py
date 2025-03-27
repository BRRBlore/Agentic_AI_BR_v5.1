from tools.dispatch_api import track_delivery
import re
from langchain.memory.chat_memory import BaseChatMemory
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge
from tools.gpt_fallback import gpt_fallback_response

def extract_delivery_id(text):
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory: BaseChatMemory = None) -> str:
    # Phase 2: Check session knowledge
    session_answer = check_session_knowledge(query)
    if session_answer:
        return f"🧠 {session_answer}"

    # Extract delivery ID
    delivery_id = extract_delivery_id(query)
    if not delivery_id and memory:
        for msg in memory.chat_memory.messages[::-1]:
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    if not delivery_id:
        return gpt_fallback_response(query)

    response = track_delivery(delivery_id)

    # Phase 1: Store facts
    extract_and_store_facts(query, response)

    # Save memory
    if memory:
        memory.save_context({"input": query}, {"output": response})

    return response
