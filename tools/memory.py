# tools/memory.py

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"  # ✅ Required for LangChain ConversationalRetrievalChain
)
