# agents/parts_dispatch_agent.py

from tools.dispatch_api import track_delivery

def handle(query: str) -> str:
    # Extract delivery ID from query
    words = query.split()
    delivery_id = None
    for word in words:
        if "/" in word or (word.isalnum() and len(word) > 6):
            delivery_id = word
            break

    if not delivery_id:
        return "❌ Please provide a valid delivery ID."

    return track_delivery(delivery_id)
