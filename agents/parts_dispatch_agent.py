import os
from tools.dispatch_api import check_delivery_status
from langchain.memory.chat_memory import BaseChatMemory
from tools.gpt_fallback import gpt_fallback_response
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge

def handle(query: str, memory: BaseChatMemory = None) -> str:
    try:
        session_answer = check_session_knowledge(query)
        if session_answer:
            return f"🧠 {session_answer}"

        delivery_id = None
        if memory:
            history = memory.load_memory_variables({}).get("chat_history", "")
            if "Delivery ID:" in history:
                delivery_id = history.split("Delivery ID:")[-1].split()[0].strip()

        response = check_delivery_status(query, memory=memory, previous_delivery_id=delivery_id)

        if not response or "not sure" in response.lower():
            response = gpt_fallback_response(query)

        extract_and_store_facts(query, response)

        if memory:
            memory.save_context({"input": query}, {"output": response})

        return f"🚚 {response}"

    except Exception as e:
        return f"❌ Parts Dispatch Agent Error: {str(e)}"
