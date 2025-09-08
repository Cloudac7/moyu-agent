import os
import logging

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

# 获取当前模块的logger，会继承主模块的配置
logger = logging.getLogger(__name__)

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化一个LLM模型，这是所有Agent的大脑
# 这里使用DeepSeek作为示例
llm = ChatDeepSeek(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
    model="deepseek-chat"
)

logger.info("LLM和环境初始化成功！")
