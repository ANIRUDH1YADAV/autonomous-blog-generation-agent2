from langchain_groq import ChatGroq

from core.config import (
    GROQ_API_KEY,
    GROQ_MODEL
)


class LLMService:

    @staticmethod
    def get_llm(
        temperature: float = 0.2
    ):

        return ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=temperature,
        )