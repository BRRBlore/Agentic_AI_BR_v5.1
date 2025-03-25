import streamlit as st
import importlib.util

# ---- Load Supervisor Agent ----
sup_path = "/content/drive/My Drive/AI_Agent_4/agents/supervisor.py"
spec = importlib.util.spec_from_file_location("supervisor", sup_path)
supervisor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(supervisor)

# ---- Streamlit App UI ----
st.set_page_config(page_title="Tech Support Chat Agent BR v4.0")
st.title("🤖 Tech Support Chat Agent BR v4.0")
st.markdown("Ask your computer, server, order, or delivery questions below.")

# Initialize chat history if not already in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    role, content = msg["role"], msg["content"]
    icon = "🧑‍💻" if role == "user" else "🤖"
    st.markdown(f"{icon} **{role.capitalize()}:** {content}", unsafe_allow_html=True)

# Input box and Send button
st.markdown("**Ask a question:**")
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", key="user_input", label_visibility="collapsed")
with col2:
    send_clicked = st.button("Send", use_container_width=True)

# Handle input
if send_clicked and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = supervisor.route_query(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Reset Chat
if st.button("🔁 Reset Chat"):
    st.session_state.messages = []
    st.rerun()
