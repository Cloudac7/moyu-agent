# 🐟 moyu-agent

> 在上班摸鱼的时间里撰写一篇高质量的微信公众号文章！

一个基于多智能代理协作的自动化内容创作工具，专为微信公众号文章生成而设计。通过调研、架构、撰写、编辑四个阶段的AI代理协作，自动化完成从选题到成文的全流程。

## ✨ 特性

- 🔍 **智能调研**: 基于Google搜索的实时信息收集
- 📝 **大纲规划**: 结构化的文章架构设计
- ✍️ **内容创作**: 风格化的文章撰写
- 🎨 **润色优化**: 专业的文案编辑和优化
- 🎯 **多样化定制**: 支持不同写作风格和目标受众
- 🔄 **人工干预**: 大纲审核节点，确保内容质量

## 🚀 快速开始

### 1. 环境准备

确保你的系统已安装Python 3.9+：

```bash
python --version
```

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd moyu-agent
```

### 3. 安装依赖

使用 `uv` (推荐) 或 `pip` 安装依赖：

```bash
# 使用 uv (更快)
uv install

# 或使用 pip
pip install -r requirements.txt
```

### 4. 环境配置

创建 `.env` 文件并配置必要的API密钥：

```bash
cp .env.example .env
```

在 `.env` 文件中填入你的API密钥：

```env
# DeepSeek API配置 (必需)
DEEPSEEK_API_KEY=your_deepseek_api_key

# Google搜索API配置 (必需)
SERPER_API_KEY=your_serper_api_key
```

#### API密钥获取方式：

- **DeepSeek API**: 访问 [DeepSeek官网](https://platform.deepseek.com/) 注册并获取API密钥
- **Serper API**: 访问 [Serper.dev](https://serper.dev/) 注册并获取Google搜索API密钥

### 5. 运行程序

使用命令行启动文章生成：

```bash
# 基础用法
python main.py "人工智能的发展趋势"

# 自定义参数
python main.py "人工智能的发展趋势" \
  --style="专业严谨" \
  --audience="技术从业者" \
  --word_count="3000" \
  --save_path="./articles/"
```

## 📋 使用说明

### 命令行参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `topic` | 文章主题(必需) | - | `"人工智能的发展趋势"` |
| `--style` | 写作风格 | `"轻松有洞见"` | `"专业严谨"`, `"幽默风趣"` |
| `--audience` | 目标读者 | `"白领人群"` | `"技术从业者"`, `"大学生"` |
| `--word_count` | 目标字数 | `"2000"` | `"1500"`, `"3000"` |
| `--print_to_console` | 是否打印到控制台 | `True` | `True`, `False` |
| `--save_to_file` | 是否保存为文件 | `True` | `True`, `False` |
| `--save_path` | 保存路径 | 当前目录 | `"./articles/"` |

### 工作流程

1. **📊 调研阶段**: Research Agent通过Google搜索收集相关信息和数据
2. **📋 大纲阶段**: Architect Agent基于调研结果生成文章大纲
3. **⏸️ 人工审核**: 显示大纲预览，用户可以审核或终止流程
4. **✍️ 撰写阶段**: Writer Agent根据大纲和调研材料撰写初稿
5. **🎨 编辑阶段**: Editor Agent对文章进行润色和优化
6. **📄 输出结果**: 生成最终文章并保存为Markdown文件

### 调整代理行为

每个代理的行为可以通过修改对应文件中的prompt来定制：

- `research.py`: 调整搜索策略和信息筛选
- `architect.py`: 修改大纲生成规则
- `writer.py`: 调整写作风格和结构
- `editor.py`: 定制编辑和润色标准

## 📁 输出示例

生成的文章将保存为Markdown格式，包含：

```markdown
# [文章标题]

[文章正文内容...]

---
生成时间: 2025-09-05
主题: 人工智能的发展趋势  
风格: 轻松有洞见
受众: 白领人群
字数: 约2000字
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LangChain](https://langchain.com/) - 强大的LLM应用开发框架
- [DeepSeek](https://deepseek.com/) - 高质量的中文大语言模型
- [Serper](https://serper.dev/) - 便捷的Google搜索API服务

## 📞 支持

如果你遇到任何问题或有建议，请：

1. 查看 [常见问题](docs/FAQ.md)
2. 提交 [Issue](https://github.com/cloudac7/moyu-agent/issues)
3. 联系维护者

---

**摸鱼创作，从此高效！** 🚀
