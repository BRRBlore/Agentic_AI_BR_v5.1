# tools/memory.py

from langchain.memory import ConversationBufferMemory

# Shared memory object for context-aware conversations
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)

# Function to access memory externally (e.g., in app.py)
def get_memory():
    return memory
