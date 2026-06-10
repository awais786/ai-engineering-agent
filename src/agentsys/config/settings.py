from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

AgentName = str  # "pm" | "dev" | "reviewer" | "fixer"


class LLMSettings(BaseModel):
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-6"
    temperature: float = 0.0


class AgentModelOverride(BaseModel):
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    # secrets / connections
    github_token: str = ""
    github_repo: str = "owner/repo"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    postgres_dsn: str = "postgresql://agentsys:agentsys@localhost:5432/agentsys"
    chroma_host: str = "localhost"
    chroma_port: int = 8000

    # llm
    llm: LLMSettings = LLMSettings()
    agent_pm: AgentModelOverride = Field(default_factory=AgentModelOverride)
    agent_dev: AgentModelOverride = Field(default_factory=AgentModelOverride)
    agent_reviewer: AgentModelOverride = Field(default_factory=AgentModelOverride)
    agent_fixer: AgentModelOverride = Field(default_factory=AgentModelOverride)

    # scheduler
    board_scan_interval_seconds: int = 300
    board_scan_enabled: bool = False

    # langfuse (env-gated)
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"

    # logging
    log_level: str = "INFO"

    def model_for(self, agent: AgentName) -> LLMSettings:
        override: AgentModelOverride = getattr(self, f"agent_{agent}")
        return LLMSettings(
            provider=override.provider or self.llm.provider,
            model=override.model or self.llm.model,
            temperature=(
                override.temperature
                if override.temperature is not None
                else self.llm.temperature
            ),
        )
