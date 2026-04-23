# 🥗 AI 私人营养师 (LangChain Agent 实战项目)

本项目是我从零开始，基于 **LangChain** 现代化 `create_tool_calling_agent` 架构，配合智谱 **GLM-4-Flash** 模型纯手搓的 AI 智能体。

## ✨ 核心亮点
* 🧠 **精准记忆与推理：** 能够跨轮次记住用户的身高体重等身体档案。
* 🛠️ **Function Calling 动态工具调用：** 内置 `calculate_bmi` (计算 BMI) 和 `query_calories` (查询热量) 工具，大模型完全自主决策并调用。
* ⚡ **国内网络直连：** 完美适配 OpenAI 接口标准，低成本、零延迟调用国内顶尖大模型。

## 🚀 快速启动
1. 安装依赖：`pip install langchain langchain-openai`
2. 在 `main.py` 中填入您的智谱 API Key。
3. 运行：`python main.py`，即可在控制台开启无限交互聊天！
