import logging
from langchain.prompts import ChatPromptTemplate
from moyu.article_agent import llm

# 获取当前模块的logger
logger = logging.getLogger(__name__)

edit_system_prompt = """
你是一名苛刻的文案编辑。你的任务是对初稿进行最后的润色和优化。

请执行以下操作：
1. **纠正**所有语法、拼写和标点错误。
2. **优化**流畅度和可读性，将长句拆短，确保段落清晰。
3. **统一**文章风格，确保其符合{style}的要求。
4. **提升**吸引力：检查标题和开头是否足够吸引人，在关键结论部分尝试添加1-2句精辟的“金句”。
5. **添加**互动环节：在文章末尾添加一个与读者互动的问题。
6. **检查**所有引用的事实和数据来源，确保内容真实可靠。
7. 输出最终版的、可直接发布的文章。
"""

edit_prompt_template = ChatPromptTemplate.from_messages([
    ("system", edit_system_prompt),
    ("human", "请润色和优化以下文章：\n{draft_article}")
])

edit_chain = edit_prompt_template | llm

def edit_article(draft_article, style="轻松有洞见"):
    edit_response = edit_chain.invoke({
        "draft_article": draft_article,
        "style": style
    })
    return edit_response.content
