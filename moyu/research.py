import asyncio
import logging

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from moyu.article_agent import llm

# 获取当前模块的logger
logger = logging.getLogger(__name__)

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


# 4. 定义一个异步运行子调研Agent的函数
async def run_worker_agent(query_info):
    """
    升级版的子调研Agent，接收一个包含时效性指令的字典。
    """
    import datetime

    base_query = query_info["query"]
    require_recency = query_info["require_recency"]
    
    # 动态构建搜索查询
    if require_recency:
        # 使用相对时间过滤，而不是绝对年份“2025”
        # get current date in YYYY-MM-DD format
        current_date = datetime.datetime.now()
        check_range = current_date - datetime.timedelta(days=365 * 2)
        search_query = f'{base_query} after:{check_range.strftime("%Y-%m-%d")}'
    else:
        search_query = base_query # 不添加时间过滤器

    research_task = f"""
    You are a professional researcher. Please conduct a focused and in-depth search specifically on: '{base_query}'.
    {'Note: The recency requirement for this query is evaluated as [High]' if require_recency else ''}
    {('Now is ' + current_date.strftime("%Y-%m-%d")) if require_recency else ''}
    {'Therefore, pay special attention to the latest information, data, and reports from the past two years.' if require_recency else ''}

    Please collect:
    1. Basic concepts, historical background, theories, and viewpoints.
    2. Relevant news, papers, research, trends, statistical reports, and authoritative data.
    3. Different perspectives and points of debate.
    4. Related case studies or examples.
    5. Main references (please list the core sources cited during your research, including news, papers, reports, and authoritative websites).

    Your search query is: {search_query}
    """
    result = await research_agent_executor.ainvoke({"input": research_task})
    return {
        "query": base_query,
        "search_query_used": search_query, # 记录实际使用的查询，用于调试
        "result": result["output"]
    }

async def run_all_workers(queries):
    """
    并发运行所有的子调研Agent。
    """
    tasks = [run_worker_agent(query) for query in queries]
    results = await asyncio.gather(*tasks)
    return results
