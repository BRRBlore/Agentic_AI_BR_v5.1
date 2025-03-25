# app.py
import streamlit as st
import importlib.util
import os

# --- Load supervisor.py dynamically ---
def load_supervisor_module():
    file_path = os.path.join("agents", "supervisor.py")
    spec = importlib.util.spec_from_file_location("supervisor", file_path)
    supervisor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(supervisor)
    return supervisor

supervisor = load_supervisor_module()

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Tech Support Chat Agent BR v5.1")

st.markdown("""
    <h1 style='text-align: center;'>🤖 Tech Support Chat Agent BR<br>v5.1</h1>
    <p style='text-align: center;'>Ask your computer, server, order, or delivery questions below.</p>
""", unsafe_allow_html=True)

# --- Chat Memory ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Input Form ---
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("Ask a question:", key="input_field")
    submitted = st.form_submit_button("Send")

if submitted and user_query:
    st.session_state.chat_history.append(("user", user_query))
    ai_response = supervisor.route_query(user_query)
    st.session_state.chat_history.append(("assistant", ai_response))

# --- Display Chat ---
for speaker, message in st.session_state.chat_history:
    if speaker == "user":
        st.markdown(f"👤 <b>User:</b> {message}", unsafe_allow_html=True)
    else:
        st.markdown(f"🤖 <b>Assistant:</b> {message}", unsafe_allow_html=True)

# --- Reset Chat ---
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = []
    st.rerun()  # ✅ Replaces deprecated experimental_rerun
