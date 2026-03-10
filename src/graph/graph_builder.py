from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from src.chains.chatbot_chain import ChatState, chat_node

checkpointer = InMemorySaver()

def builder_graph():

    graph = StateGraph(ChatState)

    graph.add_node('chat_node', chat_node)

    graph.add_edge(START, 'chat_node')
    graph.add_edge('chat_node', END)

    chatbot = graph.compile(checkpointer=checkpointer)

    return chatbot


