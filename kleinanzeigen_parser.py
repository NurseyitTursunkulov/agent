import requests
from bs4 import BeautifulSoup

def search_kleinanzeigen():
    url = "https://www.kleinanzeigen.de/s-wohnung-mieten/koeln/wohnung-zu-vermieten/k0c203l945"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Ошибка при загрузке:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "lxml")

    print(response.text)
    # Находим <ul> по ID
    ul_ads = soup.find("ul", id="srchrslt-adtable")

    if not ul_ads:
        print("Контейнер с объявлениями не найден.")
        return

    # Объявления в <li>
    li_ads = ul_ads.find_all("li", recursive=False)
    if not li_ads:
        print("Объявления не найдены.")
        return

    results = []
    for li in li_ads:
        title_tag = li.find("a", class_="ellipsis")
        price_tag = li.find("p", class_="aditem-main--middle--price-shipping--price")
        desc_tag = li.find("p", class_="aditem-main--middle--description")
        script_tag = li.find("script", type="application/ld+json")
        if title_tag:
            title = title_tag.text.strip()
            url = "https://www.kleinanzeigen.de" + title_tag.get("href")
            price = price_tag.text.strip() if price_tag else "Нет цены"
            description = desc_tag.text.strip() if desc_tag else "Нет описания"
            results.append({
                "title": title,
                "url": url,
                "price": price,
                "description": description,
                "gen":script_tag
            })

    return results

# 👇 Проверка
ads = search_kleinanzeigen()
if ads:
    for ad in ads:
        print(f"\n🏠 {ad['title']}\n💶 {ad['price']}\n🔗 {ad['url']} {ad['gen']}")
else:
    print("Объявлений не найдено.")


