"""
测试 prompts.py 中的提示词模板和构建器
"""
import pytest
from config.prompts import PromptTemplates, PromptBuilder, prompt_builder


class TestPromptTemplates:
    """测试提示词模板"""

    def test_templates_exist(self):
        """测试所有模板都存在"""
        templates = [
            "INTENT_CLASSIFICATION",
            "ENTITY_EXTRACTION",
            "REACT_AGENT_SYSTEM",
            "AGENT_FOLLOWUP",
            "TOOL_SELECTION",
            "TOOL_ERROR_HANDLER",
            "RESPONSE_GENERATION",
            "CHITCHAT_RESPONSE",
            "CONVERSATION_SUMMARY",
            "CONTEXT_COMPRESSION",
            "RAG_QUERY_GENERATION",
            "RAG_ANSWER_WITH_CONTEXT",
            "ERROR_RECOVERY",
            "FALLBACK_RESPONSE",
        ]
        
        for template_name in templates:
            assert hasattr(PromptTemplates, template_name)
            template = getattr(PromptTemplates, template_name)
            assert isinstance(template, str)
            assert len(template) > 0

    def test_template_placeholders(self):
        """测试模板包含正确的占位符"""
        # INTENT_CLASSIFICATION 应该包含 {user_input}
        assert "{user_input}" in PromptTemplates.INTENT_CLASSIFICATION
        
        # ENTITY_EXTRACTION 应该包含 {user_input} 和 {intent}
        assert "{user_input}" in PromptTemplates.ENTITY_EXTRACTION
        assert "{intent}" in PromptTemplates.ENTITY_EXTRACTION
        
        # REACT_AGENT_SYSTEM 应该包含必要的占位符
        assert "{tools_description}" in PromptTemplates.REACT_AGENT_SYSTEM
        assert "{chat_history}" in PromptTemplates.REACT_AGENT_SYSTEM
        assert "{user_input}" in PromptTemplates.REACT_AGENT_SYSTEM


class TestPromptBuilder:
    """测试提示词构建器"""

    def test_initialization(self):
        """测试初始化"""
        builder = PromptBuilder()
        assert builder.templates == PromptTemplates

    def test_build_simple_template(self):
        """测试构建简单模板"""
        builder = PromptBuilder()
        result = builder.build(
            "INTENT_CLASSIFICATION",
            user_input="今天天气怎么样？"
        )
        
        assert "今天天气怎么样？" in result
        assert "{user_input}" not in result  # 占位符应该被替换

    def test_build_complex_template(self):
        """测试构建复杂模板"""
        builder = PromptBuilder()
        result = builder.build(
            "REACT_AGENT_SYSTEM",
            tools_description="天气查询工具、计算器",
            chat_history="用户: 你好\n助手: 你好！",
            user_input="北京天气如何？"
        )
        
        assert "天气查询工具、计算器" in result
        assert "用户: 你好" in result
        assert "北京天气如何？" in result

    def test_build_with_missing_variable(self):
        """测试缺少必要变量时抛出错误"""
        builder = PromptBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build("INTENT_CLASSIFICATION")  # 缺少 user_input
        
        assert "缺少必要的变量" in str(exc_info.value)

    def test_build_with_nonexistent_template(self):
        """测试不存在的模板"""
        builder = PromptBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build("NONEXISTENT_TEMPLATE", param="value")
        
        assert "未找到模版" in str(exc_info.value)

    def test_build_with_defaults(self):
        """测试使用默认值构建"""
        builder = PromptBuilder()
        defaults = {
            "user_input": "默认问题",
            "intent": "query"
        }
        
        result = builder.build_with_defaults(
            "ENTITY_EXTRACTION",
            defaults=defaults
        )
        
        assert "默认问题" in result
        assert "query" in result

    def test_build_with_defaults_override(self):
        """测试默认值被覆盖"""
        builder = PromptBuilder()
        defaults = {
            "user_input": "默认问题",
            "intent": "query"
        }
        
        result = builder.build_with_defaults(
            "ENTITY_EXTRACTION",
            defaults=defaults,
            user_input="覆盖的问题"
        )
        
        assert "覆盖的问题" in result
        assert "默认问题" not in result
        assert "query" in result  # intent 保持默认值

    def test_build_with_empty_defaults(self):
        """测试空默认值"""
        builder = PromptBuilder()
        
        result = builder.build_with_defaults(
            "INTENT_CLASSIFICATION",
            defaults=None,
            user_input="测试问题"
        )
        
        assert "测试问题" in result

    def test_all_templates_buildable(self):
        """测试所有模板都可以被构建（提供足够的参数）"""
        builder = PromptBuilder()
        
        test_cases = {
            "INTENT_CLASSIFICATION": {"user_input": "测试"},
            "ENTITY_EXTRACTION": {"user_input": "测试", "intent": "query"},
            "REACT_AGENT_SYSTEM": {
                "tools_description": "工具",
                "chat_history": "历史",
                "user_input": "输入"
            },
            "AGENT_FOLLOWUP": {
                "previous_thoughts": "思考",
                "tool_results": "结果"
            },
            "TOOL_SELECTION": {
                "available_tools": "工具列表",
                "task": "任务",
                "entities": "实体"
            },
            "TOOL_ERROR_HANDLER": {
                "tool_name": "工具名",
                "error_message": "错误",
                "user_input": "输入"
            },
            "RESPONSE_GENERATION": {
                "chat_history": "历史",
                "tool_results": "结果",
                "user_input": "输入"
            },
            "CHITCHAT_RESPONSE": {
                "chat_history": "历史",
                "user_input": "输入"
            },
            "CONVERSATION_SUMMARY": {"conversation": "对话内容"},
            "CONTEXT_COMPRESSION": {
                "full_conversation": "完整对话",
                "turn_count": "10"
            },
            "RAG_QUERY_GENERATION": {"user_question": "问题"},
            "RAG_ANSWER_WITH_CONTEXT": {
                "question": "问题",
                "retrieved_context": "上下文"
            },
            "ERROR_RECOVERY": {
                "error_type": "类型",
                "error_message": "消息",
                "user_input": "输入",
                "conversation_state": "状态"
            },
            "FALLBACK_RESPONSE": {
                "user_input": "输入",
                "attempted_intent": "意图"
            },
        }
        
        for template_name, params in test_cases.items():
            result = builder.build(template_name, **params)
            assert isinstance(result, str)
            assert len(result) > 0
            # 确保所有占位符都被替换
            for param_value in params.values():
                assert param_value in result


class TestGlobalPromptBuilder:
    """测试全局提示词构建器实例"""

    def test_global_instance_exists(self):
        """测试全局实例存在"""
        assert prompt_builder is not None
        assert isinstance(prompt_builder, PromptBuilder)

    def test_global_instance_works(self):
        """测试全局实例可以正常工作"""
        result = prompt_builder.build(
            "INTENT_CLASSIFICATION",
            user_input="测试全局实例"
        )
        
        assert "测试全局实例" in result

    def test_global_instance_is_singleton(self):
        """测试全局实例是单例"""
        from config.prompts import prompt_builder as pb1
        from config import prompt_builder as pb2
        
        # 应该是同一个实例
        assert pb1 is pb2