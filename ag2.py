import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# 🤖 Инструмент
@tool
def get_listings() -> str:
    """Возвращает список квартир для анализа."""
    return """
1. Ruhige Wohnung in Köln
Цена: 800€
Описание: Ruhige Lage mit Balkon. 2 Zimmer. Nähe Park.

2. Lautes Loft im Zentrum
Цена: 950€
Описание: Offenes Loft mitten in der Innenstadt. Sehr laut.

3. Familienwohnung in ruhiger Gegend
Цена: 880€
Описание: 3 Zimmer. Ruhige Lage. Keine Haustiere erlaubt.
"""

# 🔧 Настройка LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 🎯 Prompt с обязательной переменной agent_scratchpad
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Ты помощник по поиску квартир."),
    HumanMessage(content="{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# ⚙️ Агент
agent = create_openai_functions_agent(
    llm=llm,
    tools=[get_listings],
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[get_listings],
    verbose=True
)

# 🚀 Ввод
user_input = "Покажи мне квартиры в тихом районе до 900 евро с минимум 2 комнатами"

# ✅ Запуск
result = agent_executor.invoke({"input": user_input})

print("\n🎯 Результат:")
print(result["output"])
