from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import InMemorySaver
import sqlite3

from src.chains.chatbot_chain import ChatState, chat_node

# Create sqlite datavase
conn = sqlite3.connect("NeurohatAIDb.db", check_same_thread=False)

cursor = conn.cursor()

# Create thread metadata table
cursor.execute("""
CREATE TABLE IF NOT EXISTS threads (
    thread_id TEXT PRIMARY KEY,
    thread_title TEXT
)
""")

conn.commit()

checkpointer = SqliteSaver(conn=conn)

def builder_graph():

    graph = StateGraph(ChatState)

    graph.add_node('chat_node', chat_node)

    graph.add_edge(START, 'chat_node')
    graph.add_edge('chat_node', END)

    chatbot = graph.compile(checkpointer=checkpointer)

    return chatbot

def retrieve_all_threads():
    all_threads = set()

    for checkpointer_obj in checkpointer.list(None):
        all_threads.add(checkpointer_obj.config['configurable']['thread_id'])


