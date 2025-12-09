import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
wiki_page = "https://en.wikipedia.org/wiki/Isaac_Newton"
def get_first_link(page_url):
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", id="mw-content-text")

    # пошук першого змістовного лінку
    for p in content.find_all("p"):
        links = p.find_all("a", href=True)
        if not links:
            continue

        for tag in links:
            href = tag["href"]

            # пропускаємо службові лінки
            if href.startswith("#"):
                continue
            if href.startswith("/wiki/File:"):
                continue

            # повертаємо повний URL
            return "https://en.wikipedia.org" + href

    return None

#цикл для пошуку лінків
for i in range(6):
    print(f"Крок {i+1}: {wiki_page}")

    next_link = get_first_link(wiki_page)

    if not next_link:
        print("Перший лінк не знайдено. Зупиняюсь.")
        break
    wiki_page = next_link

