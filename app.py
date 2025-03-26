# app.py

import streamlit as st
import importlib.util
import os

# Load supervisor.py dynamically
def load_supervisor_module():
    file_path = os.path.join("agents", "supervisor.py")
    spec = importlib.util.spec_from_file_location("supervisor", file_path)
    supervisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(supervisor)
    return supervisor

supervisor = load_supervisor_module()

# ---------- UI Config ----------
st.set_page_config(page_title="Tech Support Chat Agent BR", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .title { text-align: center; font-size: 32px; font-weight: bold; color: #2c3e50; }
        .subtitle { text-align: center; font-size: 18px; color: #7f8c8d; margin-bottom: 30px; }
        .chat-box { border-radius: 10px; padding: 15px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🤖 Tech Support Chat Agent BR v5.1</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by LangChain | RAG | Multi-Agent | Context-Aware Memory</div>", unsafe_allow_html=True)

# ---------- Chat History Memory ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Input Form ----------
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("💬 Ask your technical, order, or delivery question:", key="input_field")
    submitted = st.form_submit_button("Send")

if submitted and user_query:
    st.session_state.chat_history.append(("user", user_query))
    ai_response = supervisor.route_query(user_query)
    st.session_state.chat_history.append(("assistant", ai_response))

# ---------- Chat Output ----------
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.markdown(f"<div class='chat-box' style='background-color:#dff9fb'><b>👤 You:</b><br>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box' style='background-color:#fef9e7'><b>🤖 Assistant:</b><br>{message}</div>", unsafe_allow_html=True)

# ---------- Reset Chat Button ----------
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = []
    st.rerun()

# ---------- Executive Sidebar ----------
with st.sidebar:
    st.markdown("### 🧠 Agent Overview")
    st.markdown("- 🔧 **Troubleshooter Agent** (RAG + Memory)")
    st.markdown("- 📦 **Order Lookup Agent** (Excel DB)")
    st.markdown("- 🚚 **Parts Dispatch Agent** (Logistics Sheet)")

    st.markdown("### 💾 Context Memory")
    st.markdown("- Retains multi-turn chat")
    st.markdown("- Understands follow-up queries")

    st.markdown("### ⚙️ Built With")
    st.markdown("- LangChain + OpenAI")
    st.markdown("- FAISS for RAG")
    st.markdown("- Streamlit UI")

    st.markdown("---")
    st.markdown("📌 Version: **v5.1**")
