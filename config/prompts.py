from typing import Dict, Any
from string import Template


class PromptTemplates:
	"""提示词模板管理类"""

	# ==================== 意图识别相关 ====================
    
	INTENT_CLASSIFICATION = """
      你是一个智能助手，需要识别用户的意图。

		用户输入：{user_input}

		请判断用户的意图，从以下类别中选择一个：
		1. chitchat - 闲聊对话（问候、闲谈等）
		2. query - 信息查询（搜索、查找信息）
		3. calculation - 计算任务（数学计算、数据分析）
		4. tool_call - 需要使用工具（天气查询、数据库操作等）
		5. complex_task - 复杂任务（需要多步推理和工具调用）

		仅返回意图类别，不要其他解释。
	"""

	ENTITY_EXTRACTION = """
		从用户输入中提取关键实体信息。

		用户输入：{user_input}
		意图类型：{intent}

		请提取相关实体，以 JSON 格式返回，例如：
		{{
			"location": "北京",
			"time": "明天",
			"keyword": "天气"
		}}

		如果没有实体，返回空 JSON 对象 {{}}。
	"""

	# ==================== Agent 推理相关 ====================
	
	REACT_AGENT_SYSTEM = """
		你是一个智能助手，可以使用工具来帮助用户解决问题。

		你可以使用以下工具：
		{tools_description}

		使用 ReAct 模式进行推理：
		1. Thought（思考）：分析当前情况，决定下一步行动
		2. Action（行动）：选择一个工具并指定输入
		3. Observation（观察）：观察工具返回的结果
		4. 重复以上步骤，直到得出最终答案

		格式示例：
		Thought: 我需要先查询天气信息
		Action: weather_tool
		Action Input: {{"location": "北京"}}
		Observation: [工具返回结果]
		Thought: 现在我有了天气信息，可以回答用户了
		Final Answer: 北京明天多云，温度18-25度

		对话历史：
		{chat_history}

		用户问题：{user_input}

		现在开始推理：
	"""

	AGENT_FOLLOWUP = """
		基于之前的对话和工具调用结果，继续推理。

		之前的推理过程：
		{previous_thoughts}

		最新的工具调用结果：
		{tool_results}

		请继续推理，决定下一步行动或给出最终答案。
	"""

	# ==================== 工具调用相关 ====================
    
	TOOL_SELECTION = """
		选择合适的工具来完成任务。

		可用工具：
		{available_tools}

		用户任务：{task}
		提取的实体：{entities}

		请选择最合适的工具，并生成调用参数。返回 JSON 格式：
		{{
			"tool_name": "工具名称",
			"arguments": {{
				"arg1": "value1",
				"arg2": "value2"
			}}
		}}
	"""

	TOOL_ERROR_HANDLER = """
		工具调用失败，请生成友好的错误提示。

		工具名称：{tool_name}
		错误信息：{error_message}
		用户原始请求：{user_input}

		请生成一个友好的错误提示，解释发生了什么问题，并建议用户如何操作。
	"""

	# ==================== 响应生成相关 ====================
    
	RESPONSE_GENERATION = """
		基于对话历史和工具结果，生成自然友好的回复。

		对话历史：
		{chat_history}

		工具调用结果：
		{tool_results}

		用户问题：{user_input}

		要求：
		1. 回复要自然、友好、符合上下文
		2. 充分利用工具返回的信息
		3. 如果信息不完整，诚实告知
		4. 保持简洁，避免冗余

		你的回复：
	"""

	CHITCHAT_RESPONSE = """
		进行轻松自然的闲聊对话。

		对话历史：
		{chat_history}

		用户说：{user_input}

		请进行友好、自然的对话。可以：
		- 回应问候
		- 进行轻松的交谈
		- 适当表现出个性
		- 必要时询问用户需要什么帮助

		你的回复：
	"""

	# ==================== 记忆和总结相关 ====================
    
	CONVERSATION_SUMMARY = """
		总结以下对话的关键信息。

		对话内容：
		{conversation}

		请总结：
		1. 讨论的主要话题
		2. 重要的决定或结论
		3. 待办事项或后续行动
		4. 用户的偏好或特殊需求

		保持简洁，突出重点。
	"""

	CONTEXT_COMPRESSION = """
		压缩对话上下文，保留关键信息。

		完整对话：
		{full_conversation}

		当前对话轮次：{turn_count}

		请将对话压缩为摘要形式，保留：
		- 关键事实和信息
		- 重要的上下文
		- 用户的核心需求

		删除：
		- 冗余的寒暄
		- 不重要的细节
		- 已解决的临时问题
	"""

	# ==================== RAG 相关 ====================
    
	RAG_QUERY_GENERATION = """
		将用户问题转换为更适合向量检索的查询。

		用户问题：{user_question}

		生成 1-3 个检索查询，能够找到回答该问题所需的信息。
		以 JSON 数组格式返回：
		["查询1", "查询2", "查询3"]
	"""

	RAG_ANSWER_WITH_CONTEXT = """
		基于检索到的上下文回答问题。

		用户问题：{question}

		检索到的相关信息：
		{retrieved_context}

		要求：
		1. 基于提供的上下文回答问题
		2. 如果上下文中没有答案，诚实说明
		3. 引用具体信息时保持准确
		4. 不要编造上下文中没有的信息

		你的回答：
	"""

	# ==================== 错误处理相关 ====================
    
	ERROR_RECOVERY = """
		发生错误，尝试恢复对话。

		错误类型：{error_type}
		错误信息：{error_message}
		用户原始输入：{user_input}
		对话状态：{conversation_state}

		请：
		1. 向用户解释发生了什么
		2. 提供可能的解决方案
		3. 询问用户是否需要换一种方式尝试

		保持友好和专业。
	"""

	FALLBACK_RESPONSE = """
		无法理解用户意图或处理请求。

		用户输入：{user_input}
		尝试的意图识别：{attempted_intent}

		请生成友好的回复：
		1. 礼貌地说明无法完全理解
		2. 询问用户能否换一种方式表达
		3. 提供一些可能的操作建议
		4. 保持乐于助人的态度
	"""


class PromptBuilder:
	"""提示词构建器，提供便捷的模板填充方法"""
    
	def __init__(self):
		self.templates = PromptTemplates

	def build(self, template_name: str, **kwargs) -> str:
		"""
        构建提示词
        
        Args:
            template_name: 模板名称（PromptTemplates 中的属性名）
            **kwargs: 模板变量
            
        Returns:
            填充后的提示词
        """
		template = getattr(self.templates, template_name, None)
		if template is None:
			raise ValueError(f"未找到模版: {template_name}")
		
		try:
			return template.format(**kwargs)
		except KeyError as e:
			raise ValueError(f"模板 {template_name} 中缺少必要的变量: {e}")

	def build_with_defaults(self, template_name: str, defaults: Dict[str, Any] = None, **kwargs) -> str:
		"""
        使用默认值构建提示词
        
        Args:
            template_name: 模板名称
            defaults: 默认值字典
            **kwargs: 覆盖默认值的变量
            
        Returns:
            填充后的提示词
        """
		params = defaults.copy() if defaults else {}
		params.update(kwargs)
		return self.build(template_name, **params)


# 全局提示此构建器实例
prompt_builder = PromptBuilder()