import os
from langchain_openai import ChatOpenAI

# 🚨 修改点 1：导入现代化的智能体制造机 create_tool_calling_agent
from langchain.agents import tool, AgentExecutor, create_tool_calling_agent

# 🚨 修改点 2：导入现代化的聊天模板零件
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import requests
import datetime

# ==========================================
# 模块 A：定义工具（不变）
# ==========================================


@tool
def query_calories(food_name: str) -> str:
    """
    当用户询问任何食物的热量时，必须调用此工具。
    输入食物名称，返回每100克的真实预估热量（千卡）。
    """
    print(f"\n[🔍 营养师正在联网查询 '{food_name}' 的热量...]")

    try:
        # 这里我们模拟调用一个公共的营养数据库 API (实际开发中可替换为如 FatSecret API)
        # 为了保证代码能直接跑通，这里用了一段稍微复杂的动态计算模拟（假设它是一个极简的本地自然语言估算引擎）

        # 常见高频词汇快速映射（模拟数据库的头部缓存）
        db = {
            "米饭": 116, "馒头": 223, "面条": 110, "红烧肉": 470, "鸡蛋": 144,
            "牛奶": 54, "香蕉": 53, "西瓜": 26, "牛肉": 288, "猪肉": 143,
            "可乐": 43, "薯片": 536, "奶茶": 60, "豆腐": 82, "包子": 223
        }

        # 如果能在缓存里找到，直接返回
        for key in db.keys():
            if key in food_name:
                return f"经数据库查询，100克【{key}】的大致热量为 {db[key]} 千卡。"

        # 如果找不到，我们用一个小小的算法模拟“大模型猜热量”兜底
        if "肉" in food_name or "炸" in food_name or "烤" in food_name:
            return f"未能精准查到【{food_name}】，但根据烹饪方式估算，每100克热量较高，约在 250-400 千卡之间。"
        elif "菜" in food_name or "瓜" in food_name or "果" in food_name:
            return f"未能精准查到【{food_name}】，但作为果蔬，每100克热量极低，约在 20-50 千卡之间。"
        else:
            return f"抱歉，营养数据库中暂未收录【{food_name}】的精准热量，建议避免过量食用。"

    except Exception as e:
        return f"查询热量接口失败: {str(e)}"
@tool
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """计算BMI（身体质量指数）。需要输入体重（公斤）和身高（米）。"""
    bmi = weight_kg / (height_m ** 2)
    return f"计算完成，BMI指数为: {bmi:.1f}"



@tool
def record_diet_diary(food_items: str, total_calories_estimate: str) -> str:
    """
    当用户明确表示今天吃了什么，或者要求打卡、记录饮食时，必须调用此工具。
    输入参数1 (food_items): 用户今天吃的食物清单（如：2个汉堡，1杯可乐）。
    输入参数2 (total_calories_estimate): 你估算出的这顿饭的总热量（如：约800千卡）。
    返回：记录成功的确认信息。
    """
    print(f"\n[✍️ 营养师正在为您记录饮食日记...]")

    # 获取今天的日期
    today_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 要写进文件里的内容
    record_content = f"[{today_str}] 进食记录：{food_items} | 估算总热量：{total_calories_estimate}\n"

    try:
        # 打开一个叫 diet_diary.txt 的文件（如果没有会自动创建），模式是 'a' (追加，不会覆盖以前的)
        with open("diet_diary.txt", "a", encoding="utf-8") as f:
            f.write(record_content)
        return "饮食记录已成功保存到您的专属健康档案中！"
    except Exception as e:
        return f"保存记录失败：{str(e)}"
tools = [query_calories, calculate_bmi, record_diet_diary]
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
