from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os

from src.chains.chatbot_chain import ChatState, chat_node

# =========================
# Database Setup
# =========================

DB_PATH = os.path.join(os.getcwd(), "NeurohatAIDb.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)


# =========================
# Graph Builder
# =========================

def builder_graph():

    graph = StateGraph(ChatState)

    graph.add_node('chat_node', chat_node)

    graph.add_edge(START, 'chat_node')
    graph.add_edge('chat_node', END)

    chatbot = graph.compile(checkpointer=checkpointer)

    return chatbot


# =========================
# Retrieve Threads (FIXED)
# =========================

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)