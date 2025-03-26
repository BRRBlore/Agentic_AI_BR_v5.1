from tools.order_db import lookup_order
from langchain.memory.chat_memory import BaseChatMemory
from agents.session_knowledge import extract_and_store_facts, check_session_facts
from tools.gpt_fallback import gpt_fallback_response

def extract_order_id(query: str) -> str:
    for word in query.split():
        if len(word) >= 6 and any(char.isdigit() for char in word):
            return word
    return None

def handle(query: str, memory: BaseChatMemory = None) -> str:
    try:
        order_id = extract_order_id(query)

        if not order_id and memory:
            history = memory.chat_memory.messages[::-1]
            for msg in history:
                if msg.type == "human" and "order" in msg.content.lower():
                    order_id = extract_order_id(msg.content)
                    if order_id:
                        break

        if not order_id and memory:
            answer = check_session_facts(query, memory)
            if answer:
                return f"📦 {answer}"

        if not order_id:
            return "❌ Please provide a valid order ID."

        response = lookup_order(order_id)

        if memory:
            memory.save_context({"input": query}, {"output": response})
            extract_and_store_facts(query, response, memory)

        return response

    except Exception as e:
        return f"❌ Error in Order Lookup Agent: {str(e)}"
