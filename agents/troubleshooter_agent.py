import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory

def handle(query, memory=None):
    try:
        # ✅ Relative path to FAISS index (for Streamlit deployment)
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

        # ✅ Create chain with or without memory
        kwargs = {"llm": llm, "retriever": retriever}
        has_memory = isinstance(memory, BaseChatMemory)
        if has_memory:
            kwargs["memory"] = memory

        qa_chain = ConversationalRetrievalChain.from_llm(**kwargs)

        # ✅ If memory is provided, don't pass chat_history manually
        if has_memory:
            result = qa_chain.invoke({"question": query})
        else:
            result = qa_chain.invoke({
                "question": query,
                "chat_history": []  # fallback
            })

        return f"💡 {result['answer']}" if isinstance(result, dict) else f"💡 {result}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
