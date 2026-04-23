import os
from langchain_openai import ChatOpenAI

# 🚨 修改点 1：导入现代化的智能体制造机 create_tool_calling_agent
from langchain.agents import tool, AgentExecutor, create_tool_calling_agent

# 🚨 修改点 2：导入现代化的聊天模板零件
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# ==========================================
# 模块 A：定义工具（不变）
# ==========================================
@tool
def query_calories(food_name: str) -> str:
    """查询常见食物的热量。输入食物名称，返回每100克的热量。"""
    food_db = {"苹果": "52千卡", "炸鸡": "300千卡", "西蓝花": "34千卡"}
    return food_db.get(food_name, "数据库暂无该食物热量信息。")

@tool
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """计算BMI（身体质量指数）。需要输入体重（公斤）和身高（米）。"""
    bmi = weight_kg / (height_m ** 2)
    return f"计算完成，BMI指数为: {bmi:.1f}"

tools = [query_calories, calculate_bmi]

# ==========================================
# 模块 B：定义记忆
# ==========================================
# 🚨 修改点 3：必须加上 return_messages=True
# 因为现代化的模板需要列表格式的对话，而不是一大串字符串文本
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ==========================================
# 模块 C：大模型与提示词
# ==========================================
llm = ChatOpenAI(
    api_key="sk-your_api_key_here",   # ⬅️ 请确保这里填入了您的智谱 Key
    base_url="https://open.bigmodel.cn/api/paas/v4",
    model="glm-4-flash",
    temperature=0.5
)

# 🚨 修改点 4：拼写修正为 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的AI私人营养师。"),
    MessagesPlaceholder(variable_name="chat_history"), # 秘书的记忆插槽
    ("user", "{input}"),                               # 老板的问题
    MessagesPlaceholder(variable_name="agent_scratchpad"), # 工具运行结果的插槽
])

# ==========================================
# 模块 D：组装流水线
# ==========================================
# 🚨 修改点 5：换用现代化的工具调用组装机！它底层走的是稳定的 JSON 通信！
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True  # 开启啰嗦模式，看模型思考过程
)

# ==========================================
# 执行入口
# ==========================================

if __name__ == "__main__":
    print("\n=============================================")
    print("🥗 欢迎来到 AI 私人营养师聊天室！(输入 '退出' 或 'q' 结束)")
    print("=============================================\n")

    # 开启一个无限循环，不断等待用户打字
    while True:
        # 1. 弹出输入框，让您（用户）在控制台敲字
        user_input = input("👤 您想问点什么：")

        # 2. 如果您输入了退出指令，就打破循环，下班！
        if user_input.lower() in ['退出', 'quit', 'q', 'exit']:
            print("🤖 营养师: 祝您身体健康，再见！")
            break

        # 3. 如果您啥也没输入就按了回车，防呆处理
        if not user_input.strip():
            continue

        # 4. 把您刚才打的字，塞给大模型去思考
        try:
            print("\n⏳ 营养师正在思考...")
            response = agent_executor.invoke({"input": user_input})

            # 5. 打印大模型给出的最终人话建议
            print(f"\n🤖 营养师回答: {response['output']}\n")
            print("-" * 40)  # 打印一条华丽的分割线

        except Exception as e:
            # 6. 万一网络卡了或者断网了，温柔地报错，不至于让程序崩溃
            print(f"\n❌ 抱歉，营养师开小差了，错误信息：{str(e)}\n")
