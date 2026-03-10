# langgraph-chatbot
# 1. conda create -p venv python==3.12.0 -y

chatbot-project/
│
├── app.py                  # Main Streamlit app (entry point)
├── requirements.txt        # Production dependencies
├── README.md               # Project documentation
├── .env.example            # Example environment variables
├── .gitignore              # Files to ignore in Git
│
├── src/                    # Core application code
│   │
│   ├── graph/              # LangGraph workflow
│   │   └── graph_builder.py
│   │
│   ├── chains/             # LangChain chains or prompts
│   │   └── chatbot_chain.py
│   │
│   ├── models/             # LLM configuration
│   │   └── llm.py
│   │
│   └── utils/              # Helper functions
│       └── helpers.py
│
├── data/                   # Optional: documents or datasets
│   └── sample_docs/
│
├── assets/                 # Images, icons, UI assets
│
└── tests/                  # Optional unit tests
    └── test_graph.py


Add