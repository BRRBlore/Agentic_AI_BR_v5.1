# agents/supervisor.py

import json
from agents import troubleshooter_agent, order_lookup_agent, parts_dispatch_agent

# Load agent config
with open("config/agents_config.json", "r") as f:
    config = json.load(f)

AGENT_KEYWORDS = {
    agent["name"]: agent["keywords"]
    for agent in config["agents"]
}

def route_query(query):
    query_lower = query.lower()

    if any(keyword in query_lower for keyword in AGENT_KEYWORDS["troubleshooter_agent"]):
        return troubleshooter_agent.handle(query)

    elif any(keyword in query_lower for keyword in AGENT_KEYWORDS["order_lookup_agent"]):
        return order_lookup_agent.handle(query)

    elif any(keyword in query_lower for keyword in AGENT_KEYWORDS["parts_dispatch_agent"]):
        return parts_dispatch_agent.handle(query)

    else:
        return "🤖 I'm not sure how to help with that. Please rephrase or try a different question."
