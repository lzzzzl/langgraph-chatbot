from dataclasses import Field
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LLM 相关配置"""

    # 默认 LLM 提供商
    default_llm_provider: Literal["openai", "anthropic", "openrouter"] = Field(
        default="openrouter",
        description="默认 LLM 提供商",
    )

    # OpenAI 配置
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API Key")
    openai_model: str = Field(default="gpt-4o", description="OpenAI 模型名称")
    openai_base_url: Optional[str] = Field(default=None, description="OpenAI API Base URL")

    # Anthropic 配置
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API Key")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", description="Anthropic 模型名称")

    # OpenRouter 配置
    openrouter_api_key: Optional[str] = Field(default=None, description="OpenRouter API Key")
    openrouter_model: str = Field(
        default="anthropic/claude-3.5-sonnet",
        description="OpenRouter 模型名称"
    )
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API Base URL"
    )

    # 通用 LLM 参数
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: int = Field(default=4096, gt=0, description="最大生成 token 数")
    timeout: int = Field(default=60, gt=0, description="API 请求超时时间（秒）")
    max_retries: int = Field(default=3, ge=0, description="最大重试次数")
    
    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class RedisSettings(BaseSettings):
    """Redis 配置"""

    host: str = Field(default="localhost", description="Redis 主机")
    port: int = Field(default=6379, description="Redis 端口")
    db: int = Field(default=0, description="Redis 数据库")
    password: Optional[str] = Field(default=None, description="Redis 密码")

    # 连接池配置
    max_connections: int = Field(default=10, gt=0, description="最大连接数")
    socket_timeout: int = Field(default=5, gt=0, description="Socket 超时时间（秒）")
    socket_connect_timeout: int = Field(default=5, gt=0, description="连接超时时间（秒）")

    # 会话配置
    session_ttl: int = Field(default=3600, gt=0, description="会话过期时间（秒）")
    cache_ttl: int = Field(default=300, gt=0, description="缓存过期时间（秒）")

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class DatabaseSettings(BaseSettings):
    """数据库配置"""

    # 数据库类型
    db_type: Literal["sqlite", "postgresql", "mysql"] = Field(
        default="sqlite",
        description="数据库类型"
    )

    # SQLite 配置
    sqlite_path: str = Field(
        default="data/chatbot.db",
        description="SQLite 数据库文件路径"
    )

    # PostgreSQL/MySQL 配置
    host: str = Field(default="localhost", description="数据库主机")
    port: int = Field(default=5432, ge=1, le=65535, description="数据库端口")
    username: str = Field(default="postgres", description="数据库用户名")
    password: str = Field(default="", description="数据库密码")
    database: str = Field(default="chatbot", description="数据库名称")

    # 连接池配置
    pool_size: int = Field(default=5, gt=0, description="连接池大小")
    max_overflow: int = Field(default=10, ge=0, description="最大溢出连接数")
    pool_timeout: int = Field(default=30, gt=0, description="连接池超时时间（秒）")
    pool_recycle: int = Field(default=3600, gt=0, description="连接回收时间（秒）")

    # 其他选项
    echo: bool = Field(default=False, description="是否打印 SQL 语句")

    @property
    def database_url(self) -> str:
        """生成数据库连接 URL"""
        if self.db_type == "sqlite":
            return f"sqlite+aiosqlite:///{self.sqlite_path}"
        elif self.db_type == "postgresql":
            return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == "mysql":
            return f"mysql+aiomysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError(f"不支持的数据库类型: {self.db_type}")
        
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class CheckpointerSettings(BaseSettings):
    """检查点配置"""
    
    # 检查点类型
    checkpointer_type: Literal["memory", "sqlite", "postgresql", "redis"] = Field(
        default="sqlite",
        description="检查点存储类型"
    )
    
    # SQLite 检查点配置
    sqlite_path: str = Field(
        default="data/checkpoints/checkpoints.db",
        description="SQLite 检查点文件路径"
    )
    
    # 检查点保存策略
    save_interval: int = Field(default=1, gt=0, description="检查点保存间隔（步数）")
    max_checkpoints: int = Field(default=10, gt=0, description="每个会话最大检查点数量")
    
    model_config = SettingsConfigDict(
        env_prefix="CHECKPOINT_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class VectorStoreSettings(BaseSettings):
    """向量存储配置(用于 RAG)"""
    
    # 向量存储类型
    vector_store_type: Literal["chroma", "faiss", "pinecone", "none"] = Field(
        default="chroma",
        description="向量存储类型"
    )
    
    # ChromaDB 配置
    chroma_persist_dir: str = Field(
        default="data/chroma",
        description="ChromaDB 持久化目录"
    )
    
    # Embedding 模型配置
    embedding_provider: Literal["openai", "huggingface"] = Field(
        default="openai",
        description="Embedding 提供商"
    )
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="Embedding 模型名称"
    )
    
    # 检索配置
    top_k: int = Field(default=5, gt=0, description="检索返回的 top-k 结果数")
    score_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="相似度阈值")
    
    model_config = SettingsConfigDict(
        env_prefix="VECTOR_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class APISettings(BaseSettings):
    """API 服务配置"""
    
    # 服务配置
    host: str = Field(default="0.0.0.0", description="服务监听地址")
    port: int = Field(default=8000, ge=1, le=65535, description="服务端口")
    workers: int = Field(default=1, gt=0, description="Worker 进程数")
    
    # 安全配置
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT 密钥"
    )
    algorithm: str = Field(default="HS256", description="JWT 算法")
    access_token_expire_minutes: int = Field(
        default=30,
        gt=0,
        description="访问令牌过期时间（分钟）"
    )
    
    # CORS 配置
    cors_origins: list[str] = Field(
        default=["*"],
        description="允许的 CORS 源"
    )
    
    # 请求限制
    max_request_size: int = Field(default=10 * 1024 * 1024, description="最大请求大小（字节）")
    request_timeout: int = Field(default=300, gt=0, description="请求超时时间（秒）")
    
    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class LogSettings(BaseSettings):
    """日志配置"""
    
    # 日志级别
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="日志级别"
    )
    
    # 日志输出
    log_to_file: bool = Field(default=True, description="是否输出到文件")
    log_dir: str = Field(default="data/logs", description="日志目录")
    log_file_name: str = Field(default="chatbot.log", description="日志文件名")
    
    # 日志格式
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式"
    )
    
    # 日志轮转
    rotation: str = Field(default="1 day", description="日志轮转周期")
    retention: str = Field(default="30 days", description="日志保留时间")
    
    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class MonitoringSettings(BaseSettings):
    """监控配置"""
    
    # LangSmith 配置
    enable_langsmith: bool = Field(default=False, description="是否启用 LangSmith")
    langsmith_api_key: Optional[str] = Field(default=None, description="LangSmith API Key")
    langsmith_project: str = Field(default="langgraph-chatbot", description="LangSmith 项目名")
    
    # Prometheus 配置
    enable_prometheus: bool = Field(default=False, description="是否启用 Prometheus")
    prometheus_port: int = Field(default=9090, ge=1, le=65535, description="Prometheus 端口")
    
    model_config = SettingsConfigDict(
        env_prefix="MONITORING_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class Settings(BaseSettings):
    """全局配置"""
    
    # 应用信息
    app_name: str = Field(default="LangGraph Chatbot", description="应用名称")
    app_version: str = Field(default="0.1.0", description="应用版本")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="运行环境"
    )
    debug: bool = Field(default=True, description="调试模式")
    
    # 子配置
    llm: LLMSettings = Field(default_factory=LLMSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    checkpointer: CheckpointerSettings = Field(default_factory=CheckpointerSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)
    api: APISettings = Field(default_factory=APISettings)
    log: LogSettings = Field(default_factory=LogSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# 全局配置实例（单例）
settings = Settings()