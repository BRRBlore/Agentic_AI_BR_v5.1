from ..tools.order_db import lookup_order
from ..tools.session_knowledge import extract_and_store_facts, check_session_knowledge
from ..tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory=None) -> str:
    try:
        session_answer = check_session_knowledge(query)
        if session_answer:
            return f"🧠 {session_answer}"

        order_data = lookup_order(query)
        if order_data:
            extract_and_store_facts(query, order_data)
            return f"📦 {order_data}"
        else:
            fallback = gpt_fallback_response(query)
            return f"🤖 (Fallback GPT-3.5) {fallback}"

    except Exception as e:
        return f"❌ Order Lookup Agent Error: {str(e)}"
