import logging

from moyu.decomposer import generate_research_queries_with_time
from moyu.research import run_all_workers
from moyu.synthesis import synthesize_reports
from moyu.architect import create_outline
from moyu.writer import write_article
from moyu.editor import edit_article

# 获取当前模块的logger，会继承主模块的配置
logger = logging.getLogger(__name__)

async def chief_editor_agent(topic, style="轻松有洞见", audience="白领人群", word_count="2000"):
    """
    总调度函数，模拟主编的工作流程。
    """
    logger.info(f"【开始处理选题】: {topic}")

    # 0. 首先，需要一个大纲来指导调研（这里有个循环依赖，需要调整）
    # 解决方案：先生成一个初步的、简单的大纲或直接基于选题生成研究查询
    # 或者，我们可以先运行一个快速调研来生成大纲，然后再深度调研
    # 这里我们采用一种简单方法：主Agent直接基于选题生成初始查询列表
    logger.info("主调研Agent开始分解研究任务...")
    initial_queries = generate_research_queries_with_time(topic) # 这里先直接用topic，而非outline
    logger.info(f"生成的研究子任务: {initial_queries}")
    
    # 1. 并发执行所有子调研任务
    logger.info("并发执行所有子调研任务...")
    worker_results = await run_all_workers(initial_queries)
    
    # 汇总子调研报告
    logger.info("调研汇总Agent开始整合报告...")
    research_report = synthesize_reports(topic, worker_results)
    logger.info("深度调研完成！")
    
    # 2. 生成大纲 (这里可以加入人工审核的停顿点)
    logger.info("大纲Agent开始工作...")
    article_outline = create_outline(topic, research_report, style, audience)
    logger.info("大纲生成完成！")
    logger.info("\n" + "="*50)
    logger.info("【生成的大纲预览】: ")
    logger.info(article_outline[:500] + "...") # 预览前500字符
    logger.info("="*50 + "\n")

    # 模拟人工审核，等待用户输入
    user_input = input("请审核大纲，按回车继续撰写，或输入'stop'终止：")
    if user_input.lower() == 'stop':
        return "用户终止了流程。"
    
    # 3. 撰写初稿
    logger.info("撰写Agent开始工作...")
    draft_article = write_article(article_outline, research_report, style, audience, word_count)
    logger.info("初稿完成！")

    # 4. 润色优化
    logger.info("润色Agent开始工作...")
    final_article = edit_article(draft_article, style)
    logger.info("润色完成！")
    
    # 5. 输出最终结果
    return final_article