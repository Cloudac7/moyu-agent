from langchain.prompts import ChatPromptTemplate
from moyu.article_agent import llm


write_system_prompt = """
你是一名非常出色的公众号写手。请严格按照提供的【文章大纲】进行写作，并充分运用【调研报告】中的事实和数据。

写作要求：
1. 语言：{style}，亲切自然，适合{audience}阅读。
2. 字数：约{word_count}字。
3. 确保逻辑流畅，段落清晰，案例生动。
4. 在文章合适的地方自然地插入数据和支持，增强说服力。
5. 输出完整的文章正文，使用Markdown格式进行简单的排版（如加粗、列表）。
"""

write_prompt_template = ChatPromptTemplate.from_messages([
    ("system", write_system_prompt),
    ("human", "请根据以下大纲和调研报告撰写文章：\n文章大纲：{article_outline}\n调研报告：{research_report}")
])

write_chain = write_prompt_template | llm

def write_article(article_outline, research_report, style="轻松有洞见", audience="白领人群", word_count="2000"):
    write_response = write_chain.invoke({
        "article_outline": article_outline,
        "research_report": research_report,
        "style": style,
        "audience": audience,
        "word_count": word_count
    })
    return write_response.content
