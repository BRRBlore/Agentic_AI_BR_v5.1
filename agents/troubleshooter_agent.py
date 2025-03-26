import os
import re
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory
from tools.gpt_fallback import gpt_fallback_response  # ✅ Correct fallback import

def handle(query, memory=None):
    try:
        index_path = "faiss_index"
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

        chain_args = {"llm": llm, "retriever": retriever}
        if isinstance(memory, BaseChatMemory):
            chain_args["memory"] = memory

        qa_chain = ConversationalRetrievalChain.from_llm(**chain_args)

        result = qa_chain.invoke(query if memory else {"question": query, "chat_history": []})

        answer = result['answer'] if isinstance(result, dict) else result
        if "I don't know" in answer or "not sure" in answer:
            return gpt_fallback_response(query)
        return f"💡 {answer}"

    except Exception as e:
        return gpt_fallback_response(query)
