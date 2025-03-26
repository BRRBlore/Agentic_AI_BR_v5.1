# agents/troubleshooter_agent.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory  # for type check

def handle(query, memory=None):
    try:
        # ✅ Use relative path for Streamlit Cloud / GitHub
        index_path = "faiss_index"  # ← This should match the GitHub folder

        # Load vector store
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(
            folder_path=index_path,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )

        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        # Set up LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

        # Conditional memory inclusion
        kwargs = {
            "llm": llm,
            "retriever": retriever
        }
        if isinstance(memory, BaseChatMemory):
            kwargs["memory"] = memory

        # Build chain and get result
        qa_chain = ConversationalRetrievalChain.from_llm(**kwargs)
        result = qa_chain.invoke({"question": query})

        return f"💡 {result['answer']}" if isinstance(result, dict) else f"💡 {result}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
