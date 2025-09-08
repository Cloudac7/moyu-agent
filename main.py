import os
import logging
import asyncio

from moyu.decomposer import generate_research_queries_with_time
from moyu.research import run_all_workers
from moyu.synthesis import synthesize_reports
from moyu.architect import create_outline
from moyu.writer import write_article
from moyu.editor import edit_article

logging.basicConfig(level=logging.INFO)


from fire import Fire

async def chief_editor_agent(topic, style="轻松有洞见", audience="白领人群", word_count="2000"):
    """
    总调度函数，模拟主编的工作流程。
    """
    logging.info(f"【开始处理选题】: {topic}")

    # 0. 首先，需要一个大纲来指导调研（这里有个循环依赖，需要调整）
    # 解决方案：先生成一个初步的、简单的大纲或直接基于选题生成研究查询
    # 或者，我们可以先运行一个快速调研来生成大纲，然后再深度调研
    # 这里我们采用一种简单方法：主Agent直接基于选题生成初始查询列表
    logging.info("> 主调研Agent开始分解研究任务...")
    initial_queries = generate_research_queries_with_time(topic) # 这里先直接用topic，而非outline
    logging.info(f"生成的研究子任务: {initial_queries}")
    
    # 1. 并发执行所有子调研任务
    print("> 并发执行所有子调研任务...")
    worker_results = await run_all_workers(initial_queries)
    
    # 汇总子调研报告
    print("> 调研汇总Agent开始整合报告...")
    research_report = synthesize_reports(topic, worker_results)
    print("深度调研完成！")
    
    # 2. 生成大纲 (这里可以加入人工审核的停顿点)
    logging.info("> 大纲Agent开始工作...")
    article_outline = create_outline(topic, research_report, style, audience)
    logging.info("大纲生成完成！")
    logging.info("\n" + "="*50)
    logging.info("【生成的大纲预览】: ")
    logging.info(article_outline[:500] + "...") # 预览前500字符
    logging.info("="*50 + "\n")

    # 模拟人工审核，等待用户输入
    user_input = input("请审核大纲，按回车继续撰写，或输入'stop'终止：")
    if user_input.lower() == 'stop':
        return "用户终止了流程。"
    
    # 3. 撰写初稿
    logging.info("> 撰写Agent开始工作...")
    draft_article = write_article(article_outline, research_report, style, audience, word_count)
    logging.info("初稿完成！")

    # 4. 润色优化
    logging.info("> 润色Agent开始工作...")
    final_article = edit_article(draft_article, style)
    logging.info("润色完成！")
    
    # 5. 输出最终结果
    return final_article

def main(
        topic, 
        style="轻松有洞见", 
        audience="白领人群", 
        word_count="2000", 
        print_to_console=True,
        save_to_file=True,
        save_path=None
):
    result = asyncio.run(chief_editor_agent(topic, style, audience, word_count))
    if print_to_console:
        logging.info("\n" + "🎉 【最终文章完成】 " + "🎉")
        logging.info("="*60)
        logging.info(result)

    # 可选：将结果保存为Markdown文件
    if save_to_file:
        # 展开用户路径，确保目录存在
        base_path = os.path.expanduser(save_path) if save_path else "."
        if not os.path.isdir(base_path):
            os.makedirs(base_path, exist_ok=True)
        filename = f"{topic.replace(' ', '_')}_article.md"
        save_path = os.path.join(base_path, filename)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(result)
    logging.info(f"\n文章已保存至：{save_path}")

# 运行整个流程！
if __name__ == "__main__":
    Fire(main)
