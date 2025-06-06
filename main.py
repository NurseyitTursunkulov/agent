from langchain_openai import ChatOpenAI


from kleinanzeigen_parser import search_kleinanzeigen
from prompt import create_filter_prompt
import os
from dotenv import load_dotenv

load_dotenv()


def format_listings_for_gpt(listings):
    formatted = []
    for i, ad in enumerate(listings, 1):
        formatted.append(f"""{i}. {ad['title']}
Цена: {ad['price']}
Описание: {ad['description']}
Ссылка: {ad['url']}
""")
    return "\n\n".join(formatted)


llm = ChatOpenAI(model="gpt-4", temperature=0)

listings = search_kleinanzeigen()  # Вся выборка
listings_text = format_listings_for_gpt(listings)
prompt = create_filter_prompt(listings_text)

response = llm.invoke(prompt)
print(response.content)

