import os
from tools.order_db import lookup_order
from langchain.memory.chat_memory import BaseChatMemory
from tools.gpt_fallback import gpt_fallback_response
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge

def handle(query: str, memory: BaseChatMemory = None) -> str:
    try:
        session_answer = check_session_knowledge(query)
        if session_answer:
            return f"🧠 {session_answer}"

        order_id = None
        if memory:
            history = memory.load_memory_variables({}).get("chat_history", "")
            if "Order ID:" in history:
                order_id = history.split("Order ID:")[-1].split()[0].strip()

        response = lookup_order(query, memory=memory, previous_order_id=order_id)

        if not response or "not sure" in response.lower():
            response = gpt_fallback_response(query)

        extract_and_store_facts(query, response)

        if memory:
            memory.save_context({"input": query}, {"output": response})

        return f"📦 {response}"

    except Exception as e:
        return f"❌ Order Lookup Agent Error: {str(e)}"
