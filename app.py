import streamlit as st
import uuid

from src.graph.graph_builder import builder_graph, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage

# Initialize chatbot
chatbot = builder_graph()

# =========================
# Utility Functions
# =========================

def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):
    if not isinstance(st.session_state.get('chat_threads'), list):
        st.session_state['chat_threads'] = []

    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []


def load_conversation(thread_id):
    try:
        state = chatbot.get_state(
            config={'configurable': {'thread_id': thread_id}}
        )
        return state.values.get('messages', [])
    except Exception as e:
        st.error(f"Error loading conversation: {e}")
        return []


# =========================
# Session Setup
# =========================

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    threads = retrieve_all_threads()
    st.session_state['chat_threads'] = threads if isinstance(threads, list) else []

add_thread(st.session_state['thread_id'])


# =========================
# Sidebar UI
# =========================

st.sidebar.title('💬 NeuroChat AI')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# Debug (optional)
# st.sidebar.write("Threads from DB:", st.session_state['chat_threads'])

for thread_id in st.session_state['chat_threads'][::-1]:

    if st.sidebar.button(thread_id):
        st.session_state['thread_id'] = thread_id

        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            elif isinstance(msg, AIMessage):
                role = 'assistant'
            else:
                continue

            temp_messages.append({
                'role': role,
                'content': msg.content
            })

        st.session_state['message_history'] = temp_messages


# =========================
# Main Chat UI
# =========================

#st.title("💬 NeuroChat AI")

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type here...')

if user_input:

    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    full_response = ""

    with st.chat_message('assistant'):
        response_container = st.empty()

        for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            if isinstance(message_chunk, AIMessage):
                full_response += message_chunk.content
                response_container.markdown(full_response)

    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': full_response
    })