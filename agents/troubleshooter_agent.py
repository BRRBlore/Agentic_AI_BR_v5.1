import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_memory import BaseChatMemory
from tools.gpt_fallback import gpt_fallback_response
from tools.session_knowledge import extract_and_store_facts, check_session_knowledge

def handle(query, memory=None):
    try:
        # ✅ Load FAISS index
        index_path = "faiss_index"
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        # ✅ Setup LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

        # ✅ Build QA Chain
        chain_args = {"llm": llm, "retriever": retriever}
        if isinstance(memory, BaseChatMemory):
            chain_args["memory"] = memory
        qa_chain = ConversationalRetrievalChain.from_llm(**chain_args)

        # ✅ Run query (with or without memory)
        result = qa_chain.invoke(query if memory else {"question": query, "chat_history": []})
        answer = result["answer"] if isinstance(result, dict) else result

        # ✅ If answer is vague, fallback to GPT
        fallback_trigger_phrases = [
            "I'm not sure", "try a different question", "don't know", "not able to help"
        ]
        if any(phrase in answer.lower() for phrase in fallback_trigger_phrases):
            # Check session knowledge first
            session_answer = check_session_knowledge(query)
            if session_answer:
                return f"💡 (Session Memory) {session_answer}"

            # If not found, fallback to GPT
            return gpt_fallback_response(query)

        # ✅ Store facts into session knowledge
        extract_and_store_facts(query, answer)

        return f"💡 {answer}"

    except Exception as e:
        return f"❌ Error in Troubleshooter Agent: {str(e)}"
