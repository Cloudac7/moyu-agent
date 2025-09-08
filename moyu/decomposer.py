from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

from moyu.article_agent import llm


# 主调研Agent的提示词
master_researcher_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    你是一名高级研究分析师。你的任务是将提供的【主题】分解成不超过6个具体的研究查询，以便进行深入调研。

    请遵循以下步骤：
    1. 仔细分析提供的【主题】。
    2. 识别出调研中需要涵盖的关键要点和方面，包括但不限于背景信息、最新数据、不同观点、案例研究等。
    3. 为每一个需要事实、数据或案例研究来支撑的要点，生成一个具体的、可搜索的查询。
    4. 你的输出必须是是一个纯粹的JSON数组，每个元素是一个字符串，即一个搜索查询。不要输出任何其他文字。

    示例输出：
    ["AI自动化取代工作岗位的统计数据 2025", "AI招聘工具市场占有率", "员工对AI监控工具的满意度调查", "GPT类工具提升白领生产力的案例"]
    """),
    ("human", "请分解以下主题：{topic}"),
])

# 创建主Agent链
master_researcher_chain = master_researcher_prompt | llm | StrOutputParser()

from datetime import datetime

def generate_research_queries_with_time(topic):
    """
    升级版的主调研Agent，它会为每个查询建议一个时间筛选策略。
    输出格式改为字典列表，包含查询和时间过滤指令。
    """
    master_researcher_prompt_temporal = ChatPromptTemplate.from_messages([
        ("system", """
        You are a senior research analyst. Please break down the provided topic into subtopics that require independent research, and determine the recency requirement for each subtopic.

        For each subtopic:
        1. **High recency requirement**: Needs the latest data, news, papers, trends, or statistical reports (e.g., market share, new policies, technology releases, cutting-edge research). Add a time filter for these queries.
        2. **Low recency requirement**: Basic concepts, historical background, classic theories, or long-standing viewpoints (e.g., definitions, fundamental principles, long-term impacts). These queries do not need a time filter.

        Your output must be a JSON array, where each element is an object containing:
        - "query": string (the search query)
        - "require_recency": boolean (true if high recency is required)

        Example output:
        [
          {{"query": "Statistics on AI automation replacing jobs", "require_recency": true}},
          {{"query": "Market share of AI recruitment tools", "require_recency": true}},
          {{"query": "Holland's theory of vocational interests", "require_recency": false}},
          {{"query": "General attitudes of employees toward AI monitoring tools", "require_recency": false}}
        ]
        """),
        ("human", "Please break down the following research topic: {topic}")
    ])

    master_chain = master_researcher_prompt_temporal | llm | StrOutputParser()
    response = master_chain.invoke({"topic": topic})

    try:
        queries_with_time = json.loads(response.strip())
        return queries_with_time
    except json.JSONDecodeError:
        print("主Agent响应不是有效JSON，尝试提取...")
        # 备用方案：如果LLM没有输出纯JSON，尝试从文本中提取列表
        # 这是一个简单的启发式方法，可能需要对提示词进行迭代优化
        import re
        pattern = r'\[.*\]'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            try:
                queries = json.loads(match.group())
                return queries
            except:
                pass
        # 如果全部失败，返回一个默认查询
        return [{"query": topic, "require_recency": True}] # 默认返回需要时效性的查询
