# agents/parts_dispatch_agent.py

import re
import importlib.util

# Dynamically load dispatch_api tool
module_path = '/content/drive/My Drive/AI_Agent_4/tools/dispatch_api.py'
spec = importlib.util.spec_from_file_location("dispatch_api", module_path)
dispatch_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dispatch_api)

def handle_dispatch_request(user_input):
    # Try to extract delivery ID using regex
    match = re.search(r'(VCV\d+/\d{6}|MVCV\d+/\d{6})', user_input, re.IGNORECASE)
    
    if match:
        delivery_id = match.group(1)
        return dispatch_api.track_delivery(delivery_id)
    else:
        return "🤖 Please provide a valid delivery ID like 'VCV00014744/082021' to check dispatch status."
