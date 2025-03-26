# agents/troubleshooter_agent.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

def handle(query, memory=None):
    try:
        # ✅ Absolute path to FAISS index in Google Drive
        index_path = "/content/drive/My Drive/AI_Agent_4/faiss_index"
        
        # Load embedding model
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Load FAISS vectorstore
        vectorstore = FAISS.load_local(
            index_path, 
            embedding_model, 
            allow_dangerous_deserialization=True
        )

        # Create retriever from vectorstore
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        # Load OpenAI LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

        # Setup RAG chain with context-aware memory
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory
        )

        # ✅ Replaces deprecated `.run()` with `.invoke()`
        result = qa_chain.invoke({"question": query})
        
        return f"💡 {result}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
