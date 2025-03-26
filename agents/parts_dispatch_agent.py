import re
from tools.dispatch_api import track_delivery
from tools.gpt_fallback import gpt_fallback_response  # ✅ Fallback

def extract_delivery_id(text):
    pattern = r'\b[A-Z]*\d{5,}/\d{4,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def handle(query, memory=None):
    delivery_id = extract_delivery_id(query)

    # 🔁 Try to get from memory
    if not delivery_id and memory:
        for msg in memory.chat_memory.messages[::-1]:
            if msg.type == "human":
                delivery_id = extract_delivery_id(msg.content)
                if delivery_id:
                    break

    # ⚠️ Fallback if delivery ID not found
    if not delivery_id:
        return gpt_fallback_response("User is asking about a delivery but did not provide a valid delivery ID.")

    response = track_delivery(delivery_id)

    # ✅ Trigger fallback if the response is unhelpful
    fallback_phrases = ["i'm not sure", "please rephrase", "i don't know"]
    if any(phrase in response.lower() for phrase in fallback_phrases):
        return gpt_fallback_response(query)

    if memory:
        memory.save_context({"input": query}, {"output": response})

    return response
