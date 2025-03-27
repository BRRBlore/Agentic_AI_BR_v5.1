from ..tools.dispatch_api import get_delivery_status
from ..tools.session_knowledge import extract_and_store_facts, check_session_knowledge
from ..tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory=None) -> str:
    try:
        session_answer = check_session_knowledge(query)
        if session_answer:
            return f"🧠 {session_answer}"

        dispatch_info = get_delivery_status(query)
        if dispatch_info:
            extract_and_store_facts(query, dispatch_info)
            return f"🚚 {dispatch_info}"
        else:
            fallback = gpt_fallback_response(query)
            return f"🤖 (Fallback GPT-3.5) {fallback}"

    except Exception as e:
        return f"❌ Parts Dispatch Agent Error: {str(e)}"
