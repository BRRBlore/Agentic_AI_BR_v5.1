# agents/troubleshooter_agent.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

def handle(query, memory=None):
    try:
        # ✅ Use relative path for compatibility with Streamlit Cloud
        index_path = os.path.join("faiss_index")

        # ✅ Load embeddings and FAISS vector store
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        # ✅ Set up LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # ✅ RAG Chain with context-aware memory
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory
        )

        # ✅ Updated to use `.invoke()` as per LangChain >= 0.1
        result = qa_chain.invoke({"question": query})
        return f"💡 {result['answer']}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
