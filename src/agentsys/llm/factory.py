from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from agentsys.config.settings import LLMSettings


def get_chat_model(llm: LLMSettings, *, api_key: str) -> BaseChatModel:
    if llm.provider == "anthropic":
        return ChatAnthropic(
            model=llm.model, temperature=llm.temperature, api_key=api_key
        )
    if llm.provider == "openai":
        return ChatOpenAI(
            model=llm.model, temperature=llm.temperature, api_key=api_key
        )
    raise ValueError(f"Unknown LLM provider: {llm.provider}")
