"""
测试 config 模块的整体导入和导出
"""


class TestConfigModuleImports:
    """测试 config 模块的导入"""

    def test_import_settings_classes(self):
        """测试可以导入所有 Settings 类"""
        from config import (
            Settings,
            LLMSettings,
            RedisSettings,
            DatabaseSettings,
            CheckpointerSettings,
            VectorStoreSettings,
            APISettings,
            LogSettings,
            MonitoringSettings,
        )
        
        # 验证都是类
        assert isinstance(Settings, type)
        assert isinstance(LLMSettings, type)
        assert isinstance(RedisSettings, type)
        assert isinstance(DatabaseSettings, type)
        assert isinstance(CheckpointerSettings, type)
        assert isinstance(VectorStoreSettings, type)
        assert isinstance(APISettings, type)
        assert isinstance(LogSettings, type)
        assert isinstance(MonitoringSettings, type)

    def test_import_settings_instance(self):
        """测试可以导入全局 settings 实例"""
        from config import settings
        
        assert settings is not None
        # 验证类型
        from config import Settings
        assert isinstance(settings, Settings)

    def test_import_prompt_classes(self):
        """测试可以导入提示词相关类"""
        from config import PromptTemplates, PromptBuilder
        
        assert isinstance(PromptTemplates, type)
        assert isinstance(PromptBuilder, type)

    def test_import_prompt_builder_instance(self):
        """测试可以导入全局 prompt_builder 实例"""
        from config import prompt_builder
        
        assert prompt_builder is not None
        from config import PromptBuilder
        assert isinstance(prompt_builder, PromptBuilder)

    def test_all_exports(self):
        """测试 __all__ 中的所有导出都可用"""
        import config
        
        expected_exports = [
            "Settings",
            "LLMSettings",
            "RedisSettings",
            "DatabaseSettings",
            "CheckpointerSettings",
            "VectorStoreSettings",
            "APISettings",
            "LogSettings",
            "MonitoringSettings",
            "settings",
            "PromptTemplates",
            "PromptBuilder",
            "prompt_builder",
        ]
        
        for export_name in expected_exports:
            assert hasattr(config, export_name), f"Missing export: {export_name}"

    def test_star_import(self):
        """测试 from config import * 只导入 __all__ 中的内容"""
        import config
        
        # 获取 __all__ 列表
        all_exports = config.__all__
        
        # 验证长度
        assert len(all_exports) == 13
        
        # 验证包含预期的导出
        assert "settings" in all_exports
        assert "prompt_builder" in all_exports


class TestConfigModuleUsage:
    """测试 config 模块的实际使用场景"""

    def test_access_nested_settings(self):
        """测试访问嵌套配置"""
        from config import settings
        
        # 访问 LLM 配置
        assert hasattr(settings, "llm")
        assert settings.llm.default_llm_provider in ["openai", "anthropic", "openrouter"]
        
        # 访问数据库配置
        assert hasattr(settings, "database")
        assert settings.database.db_type in ["sqlite", "postgresql", "mysql"]

    def test_build_prompt_from_config(self):
        """测试使用 config 中的 prompt_builder"""
        from config import prompt_builder
        
        result = prompt_builder.build(
            "INTENT_CLASSIFICATION",
            user_input="集成测试"
        )
        
        assert "集成测试" in result

    def test_modify_settings_instance(self):
        """测试修改配置实例（注意：这会影响其他测试）"""
        from config import settings
        
        # 保存原始值
        original_app_name = settings.app_name
        
        try:
            # 修改值
            settings.app_name = "Modified App"
            assert settings.app_name == "Modified App"
        finally:
            # 恢复原始值
            settings.app_name = original_app_name

    def test_create_custom_settings(self):
        """测试创建自定义配置实例"""
        from config import Settings, LLMSettings
        
        custom_settings = Settings(
            app_name="Custom Bot",
            environment="production",
            debug=False,
            llm=LLMSettings(temperature=0.3),
        )
        
        assert custom_settings.app_name == "Custom Bot"
        assert custom_settings.environment == "production"
        assert custom_settings.debug is False
        assert custom_settings.llm.temperature == 0.3


class TestConfigModuleDocumentation:
    """测试模块文档"""

    def test_module_has_docstring(self):
        """测试模块有文档字符串"""
        import config
        
        assert config.__doc__ is not None
        assert len(config.__doc__.strip()) > 0
        assert "配置管理模块" in config.__doc__