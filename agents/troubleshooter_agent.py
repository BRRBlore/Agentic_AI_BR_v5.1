import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory
from agents.session_knowledge import extract_and_store_facts, check_session_facts
from tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory: BaseChatMemory = None) -> str:
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

        if memory:
            response = qa_chain.invoke({"question": query, "chat_history": memory.chat_memory.messages})
        else:
            response = qa_chain.invoke({"question": query, "chat_history": []})

        answer = response.get("answer", "").strip()

        if not answer or answer.lower() in ["i don't know.", "i’m not sure how to help with that."]:
            answer = gpt_fallback_response(query)

        if memory:
            memory.save_context({"input": query}, {"output": answer})
            extract_and_store_facts(query, answer, memory)

        return f"💡 {answer}"
    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
