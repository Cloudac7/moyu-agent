from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from moyu.article_agent import llm

# 1. 创建搜索工具
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="使用谷歌搜索来获取关于当前时事、数据、观点的最新信息。输入应该是明确的搜索查询。"
    )
]

# 2. 获取一个ReAct风格的提示词模板
prompt = hub.pull("hwchase17/react")

# 3. 创建Research Agent
research_agent = create_react_agent(llm, tools, prompt)
research_agent_executor = AgentExecutor(
    agent=research_agent,
    tools=tools,
    handle_parsing_errors=True, # 优雅地处理解析错误
    verbose=True # 打印出详细执行过程，调试时非常有用
)

# 4. 定义一个运行调研的函数
def run_research(topic):
    import datetime

    current_year = datetime.datetime.now().year
    print(f"调研年份: {current_year}")

    research_query = f"""
    你是一名专业的研究员。今年是{current_year}年，请全面调研以下话题：'{topic}'。
    在调研过程中，请同时使用中文和英文进行搜索，以获取更全面的信息。
    请搜集：
    1. 最新的相关新闻、论文和发展。
    2. 权威的数据和统计报告。
    3. 不同的观点和争论点。
    4. 相关的案例研究或实例。
    5. 主要参考文献（请列出调研过程中引用的核心来源，包含新闻、论文、报告、权威网站等）。

    请用中文进行总结，最终生成一份结构清晰、内容详实、并附有主要参考文献的调研报告。
    """
    research_result = research_agent_executor.invoke({"input": research_query})
    return research_result["output"]
