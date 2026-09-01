from langchain_openai import ChatOpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL


def create_llm() -> ChatOpenAI:

    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0,
        api_key=OPENAI_API_KEY,
    )