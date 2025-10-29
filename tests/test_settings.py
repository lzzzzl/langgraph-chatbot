"""
测试 settings.py 中的配置类
"""
import pytest
from config.settings import (
    LLMSettings,
    RedisSettings,
    DatabaseSettings,
    CheckpointerSettings,
    VectorStoreSettings,
    APISettings,
    LogSettings,
    MonitoringSettings,
    Settings,
)


class TestLLMSettings:
    """测试 LLM 配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = LLMSettings()
        assert settings.default_llm_provider == "openrouter"
        assert settings.openai_model == "gpt-4o"
        assert settings.anthropic_model == "claude-3-5-sonnet-20241022"
        assert settings.openrouter_model == "anthropic/claude-3.5-sonnet"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 4096
        assert settings.timeout == 60
        assert settings.max_retries == 3

    def test_custom_values(self):
        """测试自定义值"""
        settings = LLMSettings(
            default_llm_provider="openai",
            openai_api_key="test-key",
            temperature=0.5,
            max_tokens=2048,
        )
        assert settings.default_llm_provider == "openai"
        assert settings.openai_api_key == "test-key"
        assert settings.temperature == 0.5
        assert settings.max_tokens == 2048

    def test_temperature_validation(self):
        """测试温度参数验证"""
        # 有效范围
        settings = LLMSettings(temperature=0.0)
        assert settings.temperature == 0.0
        
        settings = LLMSettings(temperature=2.0)
        assert settings.temperature == 2.0

        # 无效范围应该抛出验证错误
        with pytest.raises(Exception):  # pydantic ValidationError
            LLMSettings(temperature=-0.1)
        
        with pytest.raises(Exception):
            LLMSettings(temperature=2.1)

    def test_env_prefix(self, monkeypatch):
        """测试环境变量前缀"""
        monkeypatch.setenv("LLM_OPENAI_API_KEY", "env-test-key")
        monkeypatch.setenv("LLM_TEMPERATURE", "0.9")
        
        settings = LLMSettings()
        assert settings.openai_api_key == "env-test-key"
        assert settings.temperature == 0.9


class TestRedisSettings:
    """测试 Redis 配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = RedisSettings()
        assert settings.host == "localhost"
        assert settings.port == 6379
        assert settings.db == 0
        assert settings.password is not None
        assert settings.max_connections == 10
        assert settings.socket_timeout == 5
        assert settings.session_ttl == 3600
        assert settings.cache_ttl == 300

    def test_custom_values(self):
        """测试自定义值"""
        settings = RedisSettings(
            host="redis.example.com",
            port=6380,
            db=1,
            password="secret",
            max_connections=20,
        )
        assert settings.host == "redis.example.com"
        assert settings.port == 6380
        assert settings.db == 1
        assert settings.password == "secret"
        assert settings.max_connections == 20


class TestDatabaseSettings:
    """测试数据库配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = DatabaseSettings()
        assert settings.db_type == "sqlite"
        assert settings.sqlite_path == "data/chatbot.db"
        assert settings.pool_size == 5
        assert settings.max_overflow == 10
        assert settings.echo is False

    def test_sqlite_database_url(self):
        """测试 SQLite 数据库 URL 生成"""
        settings = DatabaseSettings(db_type="sqlite", sqlite_path="test.db")
        assert settings.database_url == "sqlite+aiosqlite:///test.db"

    def test_postgresql_database_url(self):
        """测试 PostgreSQL 数据库 URL 生成"""
        settings = DatabaseSettings(
            db_type="postgresql",
            host="localhost",
            port=5432,
            username="user",
            password="pass",
            database="testdb",
        )
        expected = "postgresql+asyncpg://user:pass@localhost:5432/testdb"
        assert settings.database_url == expected

    def test_mysql_database_url(self):
        """测试 MySQL 数据库 URL 生成"""
        settings = DatabaseSettings(
            db_type="mysql",
            host="localhost",
            port=3306,
            username="user",
            password="pass",
            database="testdb",
        )
        expected = "mysql+aiomysql://user:pass@localhost:3306/testdb"
        assert settings.database_url == expected

    def test_invalid_db_type(self):
        """测试无效的数据库类型"""
        with pytest.raises(Exception):  # pydantic ValidationError
            DatabaseSettings(db_type="mongodb")  # type: ignore

    def test_port_validation(self):
        """测试端口号验证"""
        # 有效端口
        settings = DatabaseSettings(port=1)
        assert settings.port == 1
        
        settings = DatabaseSettings(port=65535)
        assert settings.port == 65535

        # 无效端口
        with pytest.raises(Exception):
            DatabaseSettings(port=0)
        
        with pytest.raises(Exception):
            DatabaseSettings(port=65536)


class TestCheckpointerSettings:
    """测试检查点配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = CheckpointerSettings()
        assert settings.checkpointer_type == "sqlite"
        assert settings.sqlite_path == "data/checkpoints/checkpoints.db"
        assert settings.save_interval == 1
        assert settings.max_checkpoints == 10

    def test_custom_values(self):
        """测试自定义值"""
        settings = CheckpointerSettings(
            checkpointer_type="redis",
            save_interval=5,
            max_checkpoints=20,
        )
        assert settings.checkpointer_type == "redis"
        assert settings.save_interval == 5
        assert settings.max_checkpoints == 20


class TestVectorStoreSettings:
    """测试向量存储配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = VectorStoreSettings()
        assert settings.vector_store_type == "chroma"
        assert settings.chroma_persist_dir == "data/chroma"
        assert settings.embedding_provider == "openai"
        assert settings.embedding_model == "text-embedding-3-small"
        assert settings.top_k == 5
        assert settings.score_threshold == 0.7

    def test_score_threshold_validation(self):
        """测试相似度阈值验证"""
        # 有效范围
        settings = VectorStoreSettings(score_threshold=0.0)
        assert settings.score_threshold == 0.0
        
        settings = VectorStoreSettings(score_threshold=1.0)
        assert settings.score_threshold == 1.0

        # 无效范围
        with pytest.raises(Exception):
            VectorStoreSettings(score_threshold=-0.1)
        
        with pytest.raises(Exception):
            VectorStoreSettings(score_threshold=1.1)


class TestAPISettings:
    """测试 API 配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = APISettings()
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000
        assert settings.workers == 1
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30
        assert settings.cors_origins == ["*"]
        assert settings.max_request_size == 10 * 1024 * 1024
        assert settings.request_timeout == 300

    def test_port_validation(self):
        """测试端口号验证"""
        settings = APISettings(port=8080)
        assert settings.port == 8080

        with pytest.raises(Exception):
            APISettings(port=0)
        
        with pytest.raises(Exception):
            APISettings(port=70000)


class TestLogSettings:
    """测试日志配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = LogSettings()
        assert settings.level == "INFO"
        assert settings.log_to_file is True
        assert settings.log_dir == "data/logs"
        assert settings.log_file_name == "chatbot.log"
        assert settings.rotation == "1 day"
        assert settings.retention == "30 days"

    def test_custom_log_level(self):
        """测试自定义日志级别"""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            settings = LogSettings(level=level)  # type: ignore
            assert settings.level == level


class TestMonitoringSettings:
    """测试监控配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = MonitoringSettings()
        assert settings.enable_langsmith is False
        assert settings.langsmith_api_key is not None
        assert settings.langsmith_project == "langgraph-chatbot"
        assert settings.enable_prometheus is False
        assert settings.prometheus_port == 9090

    def test_custom_values(self):
        """测试自定义值"""
        settings = MonitoringSettings(
            enable_langsmith=True,
            langsmith_api_key="test-key",
            enable_prometheus=True,
            prometheus_port=9091,
        )
        assert settings.enable_langsmith is True
        assert settings.langsmith_api_key == "test-key"
        assert settings.enable_prometheus is True
        assert settings.prometheus_port == 9091


class TestSettings:
    """测试全局配置"""

    def test_default_values(self):
        """测试默认值"""
        settings = Settings()
        assert settings.app_name == "LangGraph Chatbot"
        assert settings.app_version == "0.1.0"
        assert settings.environment == "development"
        assert settings.debug is True

    def test_nested_settings(self):
        """测试嵌套配置"""
        settings = Settings()
        
        # 验证所有子配置都已初始化
        assert isinstance(settings.llm, LLMSettings)
        assert isinstance(settings.redis, RedisSettings)
        assert isinstance(settings.database, DatabaseSettings)
        assert isinstance(settings.checkpointer, CheckpointerSettings)
        assert isinstance(settings.vector_store, VectorStoreSettings)
        assert isinstance(settings.api, APISettings)
        assert isinstance(settings.log, LogSettings)
        assert isinstance(settings.monitoring, MonitoringSettings)

    def test_custom_nested_settings(self):
        """测试自定义嵌套配置"""
        settings = Settings(
            app_name="Test Bot",
            llm=LLMSettings(temperature=0.5),
            redis=RedisSettings(host="redis.test.com"),
        )
        assert settings.app_name == "Test Bot"
        assert settings.llm.temperature == 0.5
        assert settings.redis.host == "redis.test.com"

    def test_environment_values(self):
        """测试环境变量"""
        for env in ["development", "staging", "production"]:
            settings = Settings(environment=env)  # type: ignore
            assert settings.environment == env


class TestSettingsSingleton:
    """测试全局配置单例"""

    def test_settings_instance_exists(self):
        """测试全局实例存在"""
        from config.settings import settings
        
        assert settings is not None
        assert isinstance(settings, Settings)

    def test_settings_properties(self):
        """测试全局实例属性"""
        from config.settings import settings
        
        # 确保可以访问所有子配置
        assert hasattr(settings, "llm")
        assert hasattr(settings, "redis")
        assert hasattr(settings, "database")
        assert hasattr(settings, "checkpointer")
        assert hasattr(settings, "vector_store")
        assert hasattr(settings, "api")
        assert hasattr(settings, "log")
        assert hasattr(settings, "monitoring")