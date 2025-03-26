import os
from langchain.chat_models import ChatOpenAI

def gpt_fallback_response(query: str) -> str:
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )
        response = llm.predict(query)
        return f"🤖 (Fallback GPT-3.5) {response}"
    except Exception as e:
        return f"❌ GPT-3.5 fallback failed: {str(e)}"
