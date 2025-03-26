# agents/troubleshooter_agent.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory
from tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory=None) -> str:
    try:
        # Load FAISS index
        index_path = "faiss_index"
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

        # Build RAG chain with memory if available
        chain_args = {"llm": llm, "retriever": retriever}
        if isinstance(memory, BaseChatMemory):
            chain_args["memory"] = memory

        qa_chain = ConversationalRetrievalChain.from_llm(**chain_args)

        # Run query
        result = qa_chain.invoke(query if memory else {"question": query, "chat_history": []})
        answer = result.get("answer") if isinstance(result, dict) else str(result)

        # Fallback to GPT-3.5 if response is too generic
        if not answer or answer.strip().lower() in ["i don't know", "i'm not sure how to help with that"]:
            answer = gpt_fallback_response(query)

        # Save context
        if memory:
            memory.save_context({"input": query}, {"output": answer})

        return f"💡 {answer}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
