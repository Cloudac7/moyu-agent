from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

from moyu.article_agent import llm

# 调研汇总Agent的提示词
synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    你是一名首席编辑。你的任务是将多位研究员提交的关于同一主题不同侧面的报告，整合成一份统一、连贯、全面的主调研报告。

    要求：
    1. 保持报告的结构清晰。可以按逻辑主题分块，而不是按来源分块。
    2. 消除不同报告之间的重复信息。
    3. 如果不同报告间存在矛盾的信息，请予以注明。
    4. 确保所有重要的数据、案例和观点都被涵盖。
    5. 最终报告应使用中文撰写，行文专业且流畅。
    6. 在报告结尾列出所有参考信息的来源，格式为：标题 - 来源链接。
    """),
    ("human", """
    原始选题：{topic}
    
    以下是需要你整合的各部分研究报告：
    {worker_reports}
    
    请开始撰写最终的综合调研报告：
    """)
])

synthesis_chain = synthesis_prompt | llm | StrOutputParser()

def synthesize_reports(topic, worker_results):
    """
    将子Agent的结果汇总成一份最终报告。
    """
    # 将子Agent的结果格式化为一个字符串，便于汇总Agent阅读
    reports_text = "\n\n".join([
        f"## 研究子任务: {item['query']}\n{item['result']}\n ## 实际使用的搜索查询: {item['search_query_used']}"
        for item in worker_results
    ])
    
    final_report = synthesis_chain.invoke({
        "topic": topic,
        "worker_reports": reports_text
    })
    return final_report
