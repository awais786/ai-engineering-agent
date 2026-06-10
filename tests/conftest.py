from __future__ import annotations

import pytest
from langchain_core.messages import AIMessage

from agentsys.clients.github import Issue
from agentsys.config.settings import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(github_token="test-token", anthropic_api_key="test-key")


@pytest.fixture
def fake_github():
    class FakeGitHub:
        def __init__(self) -> None:
            self.posted: tuple[str, str] | None = None

        async def get_issue(self, item_id: str) -> Issue:
            return Issue(number=int(item_id), title="Title", body="Body")

        async def post_comment(self, item_id: str, body: str) -> str:
            self.posted = (item_id, body)
            return "https://gh/comment/1"

    return FakeGitHub()


@pytest.fixture
def fake_model():
    class FakeModel:
        def bind_tools(self, tools):
            return self

        async def ainvoke(self, messages, **kwargs) -> AIMessage:
            return AIMessage(content="## Spec\n- item")

    return FakeModel()
