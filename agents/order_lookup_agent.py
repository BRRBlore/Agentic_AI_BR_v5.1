# agents/order_lookup_agent.py

from tools.order_db import lookup_order
from tools.session_knowledge import extract_facts_and_store
from langchain.memory.chat_memory import BaseChatMemory


def handle(query: str, memory=None) -> str:
    try:
        # Step 1: Extract order ID from current query
        words = query.split()
        order_id = None
        for word in words:
            if len(word) >= 6 and any(char.isdigit() for char in word):
                order_id = word
                break

        # Step 2: Fallback to memory if not found
        if not order_id and isinstance(memory, BaseChatMemory):
            past_messages = memory.chat_memory.messages[::-1]
            for msg in past_messages:
                if msg.type == "human" and "order" in msg.content.lower():
                    for word in msg.content.split():
                        if len(word) >= 6 and any(char.isdigit() for char in word):
                            order_id = word
                            break
                if order_id:
                    break

        if not order_id:
            return "❌ Please provide a valid order ID."

        # Step 3: Retrieve order status
        response = lookup_order(order_id)

        # Step 4: Save to memory + session knowledge
        if memory:
            memory.save_context({"input": query}, {"output": response})
            extract_facts_and_store(response, memory=memory)

        return response

    except Exception as e:
        return f"❌ Error in Order Lookup Agent: {str(e)}"
