# LangGraph Chatbot with Streamlit

An interactive **AI chatbot** built using **LangGraph**, **LangChain**, **Groq LLM**, and **Streamlit**.

This project demonstrates how to build a **modular AI application** with a clean architecture that separates:

* LLM configuration
* Chat logic (chains)
* Graph workflow (LangGraph)
* UI (Streamlit)

The chatbot uses **LangGraph** to manage conversation state and **Streamlit** to provide a real-time chat interface with streaming responses.

---

# Features

* AI chatbot powered by Groq LLM
* LangGraph-based conversational workflow
* Streaming responses in Streamlit
* Clean and scalable project architecture
* Environment variable configuration for API keys
* Conversation memory using LangGraph checkpointers
* Easy to extend with RAG, tools, or agents

---

# Project Architecture

```
User
  │
  ▼
Streamlit UI (app.py)
  │
  ▼
LangGraph Workflow
(graph_builder.py)
  │
  ▼
Chat Node
(chatbot_chain.py)
  │
  ▼
LLM
(Groq - llama-3.1-8b-instant)
```

LangGraph manages the **conversation state**, while the **LLM generates responses based on message history**.

---

# Project Structure

```
langgraph-chatbot/
│
├── app.py                     # Streamlit UI
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .env.example               # Example environment variables
├── .gitignore
│
├── src/
│   │
│   ├── config/
│   │   └── settings.py        # Model configuration
│   │
│   ├── graph/
│   │   └── graph_builder.py   # LangGraph workflow
│   │
│   ├── chains/
│   │   └── chatbot_chain.py   # Chat node logic
│   │
│   ├── models/
│   │   └── llm.py             # LLM initialization
│   │
│   └── utils/
│       └── helpers.py         # Utility functions
│
├── data/
│   └── sample_docs/
│
├── assets/
│
└── tests/
    └── test_graph.py
```

This structure keeps the project **modular, maintainable, and scalable**.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/debsandipagt/langgraph-chatbot.git
cd langgraph-chatbot
```

---

## 2. Create virtual environment

```bash
conda create -p venv python=3.12 -y
```

Activate the environment.

### Windows

```bash
conda activate ./venv
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

Do **not push your `.env` file** to GitHub.

---

# Running the Application

Start the Streamlit application.

```bash
streamlit run app.py
```

The app will run at:

```
http://localhost:8501
```

---

# Step-by-Step Code Implementation

This section explains how the chatbot was implemented step by step.

---

# 1. Configure the Model

The model configuration is stored in a **settings file** so it can be easily modified.

File:

```
src/config/settings.py
```

Example:

```python
# Initializing model
CHAT_MODEL = "llama-3.1-8b-instant"
```

Keeping model configuration separate helps maintain a **clean and flexible architecture**.

---

# 2. Initialize the LLM

The LLM is initialized using the configuration defined in the settings file.

File:

```
src/models/llm.py
```

Example:

```python
from langchain_groq import ChatGroq
from src.config.settings import CHAT_MODEL

def get_llm():
    return ChatGroq(model=CHAT_MODEL)
```

This separation allows the model to be easily switched without modifying the main application logic.

---

# 3. Define the Conversation State

LangGraph requires a **state schema** to manage conversation history.

File:

```
src/chains/chatbot_chain.py
```

Example:

```python
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

The `messages` field stores the entire chat history between the user and the AI.

---

# 4. Create the Chat Node

The chat node sends conversation messages to the LLM and returns the response.

File:

```
src/chains/chatbot_chain.py
```

Example:

```python
from src.models.llm import get_llm

llm = get_llm()

def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)

    return {"messages": [response]}
```

Workflow:

```
User Messages → LLM → AI Response
```

LangGraph automatically updates the state with the new response.

---

# 5. Build the LangGraph Workflow

LangGraph is used to define the conversational workflow.

File:

```
src/graph/graph_builder.py
```

Example:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from src.chains.chatbot_chain import ChatState, chat_node

def build_graph():

    checkpointer = InMemorySaver()

    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)

    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile(checkpointer=checkpointer)
```

Graph flow:

```
START → chat_node → END
```

---

# 6. Conversation Memory

The project uses:

```
InMemorySaver
```

This acts as a **LangGraph checkpointer** that stores conversation state during a session.

Characteristics:

* Stores chat history in memory
* Enables context-aware responses
* Suitable for prototype applications

In production systems, this can be replaced with:

* Redis
* PostgreSQL
* MongoDB

---

# 7. Streamlit UI

The user interface is built using Streamlit.

File:

```
app.py
```

Main components:

```
st.chat_input()
st.chat_message()
st.write_stream()
```

These components allow:

* capturing user input
* displaying conversation history
* streaming AI responses in real time

---

# Streaming Responses

The chatbot streams responses using:

```
chatbot.stream()
```

This allows the user to see the response **token by token**, creating a real-time chat experience.

---

# Deployment

The application can be deployed using:

* Streamlit Cloud
* Docker
* AWS / GCP
* HuggingFace Spaces

### Deploy on Streamlit Cloud

1. Push the repository to GitHub
2. Go to Streamlit Cloud
3. Connect your GitHub repository
4. Select `app.py` as the entry file
5. Add environment variables (`GROQ_API_KEY`)

---

# Future Improvements

Possible extensions for this project:

* RAG (Retrieval Augmented Generation)
* Vector database integration
* Multi-agent workflows
* Tool calling (search, calculator, APIs)
* Persistent memory storage
* Authentication system
* Conversation analytics

---

# Technologies Used

* Python
* LangChain
* LangGraph
* Groq LLM
* Streamlit

---

# License

This project is licensed under the **Apache 2.0 License**.

---

# Author

**Sandip Deb**
Email: [debsandip.agt@gmail.com](mailto:debsandip.agt@gmail.com)

If you found this project helpful, feel free to ⭐ the repository.

## Live app
https://langgraph-chatbot-support.streamlit.app/
