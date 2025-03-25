# agents/supervisor.py

import importlib.util

# ---- Load all 3 agents dynamically ----

# Troubleshooter Agent
spec_ts = importlib.util.spec_from_file_location(
    "troubleshooter_agent", 
    "/content/drive/My Drive/AI_Agent_4/agents/troubleshooter_agent.py"
)
troubleshooter_agent = importlib.util.module_from_spec(spec_ts)
spec_ts.loader.exec_module(troubleshooter_agent)

# Order Lookup Agent
spec_order = importlib.util.spec_from_file_location(
    "order_lookup_agent", 
    "/content/drive/My Drive/AI_Agent_4/agents/order_lookup_agent.py"
)
order_lookup_agent = importlib.util.module_from_spec(spec_order)
spec_order.loader.exec_module(order_lookup_agent)

# Parts Dispatch Agent
spec_dispatch = importlib.util.spec_from_file_location(
    "parts_dispatch_agent", 
    "/content/drive/My Drive/AI_Agent_4/agents/parts_dispatch_agent.py"
)
parts_dispatch_agent = importlib.util.module_from_spec(spec_dispatch)
spec_dispatch.loader.exec_module(parts_dispatch_agent)

# ---- Supervisor Routing Logic ----

def route_query(user_input):
    user_input_lower = user_input.lower()

    if "delivery" in user_input_lower or "dispatch" in user_input_lower or "track" in user_input_lower:
        return parts_dispatch_agent.handle_dispatch_request(user_input)

    elif "order" in user_input_lower or "status" in user_input_lower:
        return order_lookup_agent.handle_order_status(user_input)

    else:
        return troubleshooter_agent.find_answer(user_input)
