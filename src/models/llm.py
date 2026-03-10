from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.config.settings import CHAT_MODEL


def get_llm():

    return ChatGroq(model=CHAT_MODEL)