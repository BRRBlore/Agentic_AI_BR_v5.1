from tools.dispatch_api import track_delivery
from langchain.memory.chat_memory import BaseChatMemory
import re
from agents.session_knowledge import extract_and_store_facts, check_session_facts
from tools.gpt_fallback import gpt_fallback_response

def extract_delivery_id(text: str) -> str:
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query: str, memory: BaseChatMemory = None) -> str:
    try:
        delivery_id = extract_delivery_id(query)

        if not delivery_id and memory:
            for msg in memory.chat_memory.messages[::-1]:
                if msg.type == "human":
                    delivery_id = extract_delivery_id(msg.content)
                    if delivery_id:
                        break

        if not delivery_id and memory:
            answer = check_session_facts(query, memory)
            if answer:
                return f"📦 {answer}"

        if not delivery_id:
            return "❌ Please provide a valid delivery ID."

        response = track_delivery(delivery_id)

        if memory:
            memory.save_context({"input": query}, {"output": response})
            extract_and_store_facts(query, response, memory)

        return response

    except Exception as e:
        return f"❌ Error in Parts Dispatch Agent: {str(e)}"
