import os
import logging
import asyncio

from fire import Fire
from moyu.chief import chief_editor_agent

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
