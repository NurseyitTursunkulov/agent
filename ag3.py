from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0)

template = ChatPromptTemplate.from_template("""
Ты помощник по недвижимости.

У пользователя такие критерии:
{criteria}

Вот список квартир:
{listings}

Отметь подходящие и объясни почему.
""")

formatted_prompt = template.format_messages(
    criteria="до 900 евро, тихий район, минимум 2 комнаты, желательно балкон",
    listings="""
1. Ruhige Wohnung mit Balkon – 800€
2. Loft im Zentrum – 950€
3. Familienwohnung in ruhiger Lage – 880€
"""
)

response = llm.invoke(formatted_prompt)
print(response.content)
