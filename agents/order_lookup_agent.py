from tools.order_db import lookup_order_status
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge
from tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory=None):
    try:
        session_answer = check_session_knowledge(query)
        if session_answer:
            return f"🧠 {session_answer}"
        answer = lookup_order_status(query)
        if not answer or "Order Status" not in answer:
            answer = gpt_fallback_response(query)
        extract_and_store_facts(query, answer)
        if memory:
            memory.save_context({"input": query}, {"output": answer})
        return answer
    except Exception as e:
        return f"❌ Order Lookup Agent Error: {str(e)}"