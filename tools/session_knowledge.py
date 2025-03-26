# tools/session_knowledge.py

import os
from langchain.chat_models import ChatOpenAI

# In-memory session fact store
session_facts = []

# OpenAI LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

def extract_facts(response: str) -> list:
    """
    Extract structured facts from a given agent response using GPT-3.5
    """
    try:
        system_prompt = (
            "You are an AI assistant. Extract key facts from the following answer. "
            "Return only a numbered list of short factual sentences. "
            "Avoid rephrasing. Don't repeat irrelevant lines. "
            "Example:\n"
            "Input: 'The delivery ID MVC0001 was dispatched on Jan 1 and delivered Jan 5. It was delayed due to rain.'\n"
            "Output:\n"
            "1. Delivery ID MVC0001 was dispatched on Jan 1.\n"
            "2. Delivery ID MVC0001 was delivered on Jan 5.\n"
            "3. Delivery was delayed due to rain."
        )

        prompt = f"Extract key facts from this response:\n\n{response}"

        result = llm.predict_messages([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ])

        facts = result.content.strip().split("\n")
        return [fact.strip() for fact in facts if fact.strip()]

    except Exception as e:
        print(f"❌ Fact Extraction Failed: {e}")
        return []

def save_facts_from_response(response: str):
    """
    Extract and save facts to session memory
    """
    facts = extract_facts(response)
    if facts:
        session_facts.extend(facts)

def get_session_facts():
    """
    Return all stored session facts as a single text block
    """
    return "\n".join(session_facts)

def reset_session_facts():
    """
    Clear all session facts
    """
    session_facts.clear()
