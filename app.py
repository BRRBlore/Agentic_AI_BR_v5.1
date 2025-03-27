import streamlit as st
import importlib.util
import os
from tools.memory import get_memory  # ✅ Import memory utility
memory = get_memory()

# --- Load supervisor.py dynamically ---
def load_supervisor_module():
    file_path = os.path.join("agents", "supervisor.py")
    spec = importlib.util.spec_from_file_location("supervisor", file_path)
    supervisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(supervisor)
    return supervisor

supervisor = load_supervisor_module()

# --- Streamlit Config ---
st.set_page_config(page_title="Tech Support Chat Agent BR v5.1 🚀", layout="wide")


# --- Header ---
st.markdown("""
    <div style='text-align: center; padding: 10px 0'>
        <h1 style='color:#2c3e50;'>🤖 Tech Support Chat Agent BR v5.1</h1>
        <h4 style='color:gray;'>Powered by LangChain | RAG | Multi-Agent | Context-Aware Memory</h4>
        <hr style='border: 1px solid #ddd;'/>
    </div>
""", unsafe_allow_html=True)

# --- Memory Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- User Input ---
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("💬 Ask your technical, order, or delivery question:", key="input_field")
    submitted = st.form_submit_button("Send")

# --- Handle Query ---
if submitted and user_query:
    # Step 1: Store user message in Streamlit history
    st.session_state.chat_history.append(("user", user_query))

    # Step 2: Add user message to LangChain memory
    memory.chat_memory.add_user_message(user_query)

    # Step 3: Route query and get AI response
    ai_response = supervisor.route_query(user_query, memory=memory)

    # Step 4: Store AI response in Streamlit UI
    st.session_state.chat_history.append(("assistant", ai_response))

    # Step 5: Add AI response to LangChain memory
    memory.chat_memory.add_ai_message(ai_response)

# --- Display Chat ---
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.markdown(f"**👤 You:** {message}")
    else:
        st.markdown(f"**🤖 Assistant:** {message}", unsafe_allow_html=True)

# --- Reset Button ---
st.markdown("---")
if st.button("🔁 Reset Chat"):
    st.session_state.chat_history = []
    memory.clear()  # ✅ Clear LangChain memory too
    st.rerun()
