# agents/order_lookup_agent.py

import re
import importlib.util

# Dynamically load the order_db tool
module_path = "/content/drive/My Drive/AI_Agent_4/tools/order_db.py"
spec = importlib.util.spec_from_file_location("order_db", module_path)
order_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(order_db)

def handle_order_status(user_input):
    # Extract possible order ID (any alphanumeric pattern of 8+ characters)
    match = re.search(r"\b[A-Za-z0-9]{8,}\b", user_input)
    
    if match:
        order_id = match.group(0)
        return order_db.lookup_order(order_id)
    else:
        return "🤖 Please provide a valid order ID so I can check its status."
