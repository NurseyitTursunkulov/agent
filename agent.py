from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from kleinanzeigen_parser import search_kleinanzeigen

load_dotenv()


# 🔧 Инструмент
@tool
def get_listings(input_text: str) -> str:
    """Получает список квартир с Kleinanzeigen в виде отформатированного текста."""
    listings = search_kleinanzeigen()
    if not listings:
        return "Объявлений не найдено."

    result = []
    for i, ad in enumerate(listings, 1):
        result.append(f"""{i}. {ad['title']}
Цена: {ad['price']}
Описание: {ad['description']}
Ссылка: {ad['url']}
""")
    return "\n\n".join(result)


# 🤖 Prompt с переменной agent_scratchpad
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(
        content="Ты агент по недвижимости. "
                "Ты умеешь использовать инструмент `get_listings`, чтобы получить список объявлений. "
                "Если тебе нужно узнать, какие объявления соответствуют запросу, сначала вызови `get_listings`, "
                "а затем отфильтруй их по критериям пользователя."
    ),
    HumanMessage(content="{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 🤖 Модель
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 🧠 Агент
agent = create_openai_functions_agent(llm=llm, tools=[get_listings], prompt=prompt)

# 🛠️ Executor
executor = AgentExecutor(agent=agent, tools=[get_listings], verbose=True)

# 🚀 Запрос
query = """
Покажи мне подходящие квартиры: тихий район, цена до 900€, минимум 2 комнаты.
Скажи, какие подходят, и почему.
"""

result = executor.invoke({"input": query})

print("\n🎯 Результат:")
print(result["output"])
