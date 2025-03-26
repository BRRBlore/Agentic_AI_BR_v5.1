# test_troubleshooter_agent.py
from agents.troubleshooter_agent import handle_troubleshooting_query

queries = [
    "My laptop won’t power on",
    "No display on monitor",
    "Blue screen error",
    "My screen is flickering",
    "How do I run diagnostics?"
]

print("🧪 Troubleshooter Agent Test Results:\n")
for q in queries:
    print(f"🔎 Query: {q}")
    print(f"💡 Response: {handle_troubleshooting_query(q)}\n")
