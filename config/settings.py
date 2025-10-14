from dataclasses import Field
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LLM 相关配置"""

    # 默认 LLM 提供商
    default_llm_provider: Literal["openai", "anthropic", "openrouter"] = Field(
        default="openrouter",
        description="默认 LLM 提供商",
    )

    pass
