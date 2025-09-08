import logging
from langchain_core.prompts import ChatPromptTemplate
from moyu.article_agent import llm

# 获取当前模块的logger
logger = logging.getLogger(__name__)

# 定义系统提示词，明确角色和任务
outline_system_prompt = """
你是一名资深的公众号文章编辑和策略师。你的任务是根据用户提供的【选题】和【调研报告】，设计出吸引人的文章大纲。

要求：
1. 生成3个备选标题，要求吸引目标读者点击。
2. 设计完整的文章结构，包括：引人入胜的开头、逻辑清晰的正文分论点（至少二级标题H2）、有说服力的结尾。
3. 在结尾列出参考的主要文献或数据来源。
4. 文章风格应为：{style}，目标读者是：{audience}。
5. 输出必须是严格且清晰的Markdown格式。
"""

# 创建提示词模板
outline_prompt_template = ChatPromptTemplate.from_messages([
    ("system", outline_system_prompt),
    ("human", "请为以下选题和调研报告创建大纲：\n选题：{topic}\n调研报告：{research_report}")
])

# 创建LCEL链
outline_chain = outline_prompt_template | llm

def create_outline(topic, research_report, style="轻松有洞见", audience="白领人群"):
    outline_response = outline_chain.invoke({
        "topic": topic,
        "research_report": research_report,
        "style": style,
        "audience": audience
    })
    return outline_response.content