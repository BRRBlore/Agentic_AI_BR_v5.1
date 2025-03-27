
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge
from tools.gpt_fallback import gpt_fallback_response

def handle(query: str, memory: BaseChatMemory = None) -> str:
    try:
        session_answer = check_session_knowledge(query)
        if session_answer:
            return f"🧠 {session_answer}"
        index_path = "faiss_index"
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get("OPENAI_API_KEY"))
        chain_args = {"llm": llm, "retriever": retriever}
        if memory and isinstance(memory, BaseChatMemory):
            chain_args["memory"] = memory
        qa_chain = ConversationalRetrievalChain.from_llm(**chain_args)
        result = qa_chain.invoke(query if memory is None else {"question": query, "chat_history": []})
        answer = result["answer"] if isinstance(result, dict) else result
        if not answer or answer.strip().lower() in ["i don't know", "not sure", ""]:
            answer = gpt_fallback_response(query)
        extract_and_store_facts(query, answer)
        if memory:
            memory.save_context({"input": query}, {"output": answer})
        return f"💡 {answer}"
    except Exception as e:
        return f"❌ Troubleshooter Agent Error: {str(e)}"