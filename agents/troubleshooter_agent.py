# agents/troubleshooter_agent.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory

# ✅ Cache the chain globally
qa_chain = None

def handle(query, memory=None):
    global qa_chain
    try:
        if qa_chain is None:
            # ✅ Load FAISS index and build retriever
            index_path = "faiss_index"
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
            retriever = vectorstore.as_retriever(search_type="similarity", k=3)

            # ✅ Initialize OpenAI LLM
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                openai_api_key=os.environ.get("OPENAI_API_KEY")
            )

            # ✅ Build Conversational RAG chain with memory if available
            kwargs = {"llm": llm, "retriever": retriever}
            if isinstance(memory, BaseChatMemory):
                kwargs["memory"] = memory

            qa_chain = ConversationalRetrievalChain.from_llm(**kwargs)

        # ✅ Ask the question (no need to pass chat_history manually)
        result = qa_chain.invoke({"question": query})

        return f"💡 {result['answer']}" if isinstance(result, dict) else f"💡 {result}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
